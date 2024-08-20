import json
import asyncio
import traceback
import copy
from openfinance.config import Config
from openfinance.config.macro import MLOG

from openfinance.datacenter.database.base import DataBaseManager
from openfinance.datacenter.knowledge.executor import ExecutorManager
from openfinance.datacenter.echarts import ChartManager
from openfinance.datacenter.knowledge.entity_graph.base import EntityGraph, EntityEnum
from openfinance.datacenter.knowledge.scope import ScopeCodeEnum

DBMG = DataBaseManager(Config())
ENTITY = EntityGraph()

class ExecutorGenerator:
    @classmethod
    def register(
        cls, 
        **kwargs
    ) -> None:
        # kwargs: name, desc, signature, graph_node, **extend
        try:
            func_config = kwargs.pop("func_config")
            
            async def run_single_process(
                name,
                source,
                **new_kwargs
            ):
                # print("source_: ", source)
                if not source:
                    return
                source_ = copy.deepcopy(source)
                if "source_config" in new_kwargs:
                    source_.update(new_kwargs["source_config"])
                table = source_.pop("table")
                if "condition" in source_:
                    condition = []
                    # print("table: ", table)
                    # print("condition: ", source["condition"])
                    for k, v in source_["condition"].items():
                        if v["value"] == "name":
                            condition.append(k + v.get("type", "=") + "'" + name + "'")
                        else:
                            condition.append(k + v.get("type", "=") + "'" + new_kwargs[v["value"]] + "'")
                    condition = " and ".join(condition)
                    if "where" in table:
                        table = table + " and " + condition
                    else:                            
                        table = table + " where " + condition
                # print("table: ", table, "source: ", source)
                data = await DBMG.get_data(
                    table,
                    source_,
                )
                # print("data: ", data)
                if data:
                    # print(data)
                    if source_.get("with_chart", False):
                        chart_config = source_["chart"]
                        data["chart"] = ChartManager().get(chart_config.get("chart_type"))(
                            data["chart"], 
                            chart_config["chart_label"]
                        )
                return data

            async def generate_func(
                name="",
                func_config = func_config,
                **new_kwargs
            ):
                """
                    Function to generate a function based on different config
                        a、entity_type Company ...
                        b、time_scope  Day ...
                    Argument: 
                        new_kwargs: real kwargs for generated function
                """
                # print("input_kwargs: ", new_kwargs)

                # update entity_type according to call sources                
                if "executor" in new_kwargs:
                    entity_type = ENTITY.get_type_from_graph_path(
                        new_kwargs['executor']
                    )
                    if entity_type:
                        new_kwargs['entity_type'] = entity_type

                # settings from inputs
                entity_type = new_kwargs.get("entity_type", "")
                time_scope = new_kwargs.get("time_scope", "")
                country = new_kwargs.get("country", "CHINA")
                # update company name to industry name
                if ENTITY.is_company(name) and ENTITY.is_industry_type(entity_type):
                    name = ENTITY.get_industry(name)

                # print("func_config1: ", func_config)
                # firstly update func_config based on entity_type, order matters
                if entity_type in func_config:
                    func_config.update(func_config[entity_type])
                # secondly update func_config based on entity_type, order matters                    
                if time_scope in func_config:
                    func_config.update(func_config[time_scope])
                # thirdly update func_config based on Country, order matters
                if country in func_config:
                    func_config.update(func_config[country])
                # print("func_config2: ", func_config)
                # update last effective setting
                func_entity_type = func_config.get("entity_type", entity_type)
                func_time_scope = func_config.get("time_scope", time_scope)
                country = func_config.get("country", country)
                # print("time_scope: ", func_time_scope)
                # print("func_time_scope: ", func_time_scope)
                # print("entity_type: ", entity_type)
                # print("func_entity_type: ", func_entity_type)                                                
                # both sides exsit settings and mismatch
                if entity_type and func_entity_type and entity_type != func_entity_type:
                    return
                if time_scope and func_time_scope and time_scope != func_time_scope:
                    return
                # begin to get function

                # common config
                source = func_config.get("source", {})
                # print("source1: ", source)                        
                # right now only support one dimention config to update source
                # source updated
                if entity_type in source:
                    source.update(source[entity_type])
                if country in source:
                    source.update(source[country])
                # print("source2: ", source)  
                try:
                    # time scope sources                    
                    if time_scope in source:
                        # print("before time_scope: ", time_scope, " source: ", source)
                        source.update(source[time_scope])
                        # print("after time_scope: ", time_scope, " source: ", source)                        
                    # run single choosed time_scope              
                    result = await run_single_process(
                        name,
                        source,
                        **new_kwargs                            
                    )
                    # if not input time_scope and there are multi timescope, run them all                  
                    if not time_scope:
                        time_scope_list = []
                        for ts in list(ScopeCodeEnum.__members__.keys()):
                            if ts in source:
                                time_scope_list.append(ts)
                        if len(time_scope_list):
                            result = [result]
                            for ts in time_scope_list:
                                source.update(source[ts])
                                ts_result = run_single_process(
                                    name,
                                    source,
                                    **new_kwargs                            
                                )
                                result.append(ts_result)
                    # print("result: ", result)                        
                    if result:
                        return result
                    return func_config.get("default", " ")
                except Exception as e:
                    print(e)
                    traceback.print_exc()  
                    traceback_str = traceback.format_exc()  
                    print("堆栈跟踪字符串:\n", traceback_str)
                    return func_config.get("default", " ")
 
            executor_config = kwargs["executor_config"]
            for econfig in executor_config:
                # get function name
                if "func_name" in econfig:
                    func_name = econfig.pop("func_name")
                else:
                    func_name = econfig["name"]
                    func_name = "get_" + func_name.replace(" ", "_").lower()
            
                generate_func.__name__ = func_name

                # registre function

                ExecutorManager().register(
                    func = generate_func,
                    **econfig
                )
                # registre config
                ExecutorManager().register_config(
                    **econfig,
                    config = func_config
                )                
        except Exception as e:
            raise e
    
    @classmethod
    def register_from_file(
        cls,
        file: str = "openfinance/datacenter/database/config/common.json"
    ):
        with open(file, "r") as infile:
            jsondata = json.load(infile)
            for d in jsondata["executors"]:
                cls.register(**d)

if __name__ == "__main__":
    ExecutorGenerator.register_from_file()