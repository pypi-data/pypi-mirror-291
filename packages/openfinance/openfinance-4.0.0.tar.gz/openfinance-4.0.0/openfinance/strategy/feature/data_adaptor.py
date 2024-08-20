from typing import (
    List,
    Any,
    Dict,
    Union,
    Callable
)
import json
from abc import ABC, abstractmethod
from pydantic import BaseModel, root_validator

from openfinance.utils.singleton import singleton
from openfinance.config import Config
from openfinance.datacenter.database.base import DataBaseManager
from openfinance.datacenter.database.source.eastmoney.trade import (
    stock_realtime,
    market_realtime
)
from openfinance.datacenter.knowledge.entity_graph.base import EntityGraph
from openfinance.strategy.operator.base import OperatorManager

db = DataBaseManager(Config()).get("db")
quant_db = DataBaseManager(Config()).get("quant_db")

@singleton
class DataAdaptor:
    """
        Translate different sources to standard format datatype
        {
            "name": {
                "time": []
                "data": []
            }
        }
    """
    name: str = "adaptor"
    name_to_sources: Dict[str, Callable] = {}

    def add(
        self, 
        name: str,
        func: Callable 
    ) -> None:
        try:
            if name not in self.name_to_sources:
                self.name_to_sources.update({name: func})
            else:
                self.name_to_sources[name].update(func)
        except Exception as e:
            raise e

    def get(
        self, 
        name: str
    ):
        if name in self.name_to_sources:
            return self.name_to_sources[name]
        return None

def _realtime(
    candidates,
    **kwargs
):
    if not candidates:
        candidates = list(EntityGraph().companies.keys())
    if isinstance(candidates, str):
        candidates = [candidates]
    # print(candidates)
    pd = stock_realtime(candidates)            
    
    result = {}
    for i in range(len(pd)):
        d = pd.iloc[i]
        result[d[kwargs["key"]]] = d[kwargs["value"]]
    return result

DataAdaptor().add("realtime", _realtime)

def _db_obj(
    candidates,
    **kwargs
):
    obj = kwargs.get("obj", "SECURITY_NAME")
    if candidates and len(candidates) < 10:
        if isinstance(candidates, list):
            range_str = f"{obj} in ('" + "','".join(candidates) + "')"
        else:
            range_str = f"{obj}='" + candidates[0] + "'"
        data = db.select_more(
            table = kwargs["table"],
            range_str = range_str,
            field = kwargs["field"]
        )            
    else:
        data = db.select_more(
            table = kwargs["table"],
            field = kwargs["field"]
        )
        if len(candidates):
            data = [d for d in data if d[obj] in candidates]
    # print("kwargs: ", kwargs)
    # print("range_str: ", range_str)


    # groupby and only consider single value case , to update later
    name_to_sources = {}
    if isinstance(kwargs["value"], str):
        for i in data:
            if i[kwargs["value"]] is None:
                continue
            if i[obj] in name_to_sources:
                name_to_sources[i[obj]][i[kwargs["key"]]] = i[kwargs["value"]]
            else:
                if "key" in kwargs:
                    name_to_sources[i[obj]] = {i[kwargs["key"]]: i[kwargs["value"]]}
                else:
                    name_to_sources[i[obj]] = i[kwargs["value"]]
    elif isinstance(kwargs["value"], list): # case for multi value
        for i in data:
            if i[obj] in name_to_sources:
                new_val = [i[j] for j in kwargs["value"]]
                name_to_sources[i[obj]][i[kwargs["key"]]] = new_val
            else:
                new_val = [i[j] for j in kwargs["value"]]
                if "key" in kwargs:
                    name_to_sources[i[obj]] = {i[kwargs["key"]]: new_val}
                else:
                    name_to_sources[i[obj]] = new_val
    result = {}
    for k, v in name_to_sources.items():
        #print(k, v)
        if "key" in kwargs:     
            v = sorted(v.items(), key=lambda x:x[0])
            dates = [x[0] for x in v]
            values = [x[1] for x in v]
            result[k] = {
                kwargs["key"]: dates,
                "data": values
            }
        else:
            result[k] = {
                "data": v
            }
    # print("result: ", result)        
    return result

DataAdaptor().add("db", _db_obj)

def _db_all(
    candidates="上证指数",
    **kwargs
):
    # print("db_all kwargs: ", kwargs)
    if candidates: 
        if isinstance(candidates, list):
            candidates = candidates[0]
    else:
         candidates = "上证指数"
    range_str = kwargs.get("filter", "")
    data = db.select_more(
        table = kwargs["table"],
        range_str = range_str,
        field = kwargs["field"]
    )
    # print("kwargs: ", kwargs)
    # groupby and only consider single value case , to update later
    key_to_features = {}
    if isinstance(kwargs["value"], str):
        for i in data:
            if i[kwargs["value"]] is None:
                continue
            key_to_features[i[kwargs["key"]]] = i[kwargs["value"]]
    elif isinstance(kwargs["value"], list): # case for multi value
        for i in data:
            new_val = [i[j] for j in kwargs["value"]]
            key_to_features[i[kwargs["key"]]] = new_val          

    v = sorted(key_to_features.items(), key=lambda x:x[0])
    dates = [x[0] for x in v]
    values = [x[1] for x in v]
    return {
        candidates: {
            kwargs["key"]: dates,
            "data": values
        }
    }

DataAdaptor().add("db_all", _db_all)

def _company(
    candidates,
    fid,
    **kwargs
):
    if candidates and len(candidates) < 10:
        if isinstance(candidates, list):
            range_str = f"SECURITY_NAME in ('" + "','".join(candidates) + f"') and fid={fid} order by TIME"
        else:
            range_str = f"SECURITY_NAME='" + candidates + f"') and fid={fid} order by TIME"
        data = quant_db.select_more(
            table = "t_stock_feature_map",
            range_str = range_str
        )            
    else:
        data = quant_db.select_more(
            table = "t_stock_feature_map",
            range_str=f"fid={fid} order by TIME"
        )
        if candidates:
            data = [d for d in data if d["SECURITY_NAME"] in candidates]

    # print("data: ", data)
    result = {}
    keys = {}
    for d in data:
        company = d["SECURITY_NAME"]
        if company not in result:
            result[company] = []
            keys[company] = []
        result[company].append(d["val"])
        keys[company].append(d["TIME"])
    return result, keys

DataAdaptor().add("company", _company)


def _market(
    candidates,
    fid,
    **kwargs
):
    # print("_market fid: ", fid)
    if not candidates:
        candidates = "上证指数"
    if isinstance(candidates, list):
        candidates = candidates[0]

    data = quant_db.select_more(
        "t_market_feature_map",
        range_str=f"fid={fid} order by TIME"
    )
    # print("_market data: ", data)
    result = []
    keys = []
    for d in data:
        result.append(d['val'])
        keys.append(d['TIME'])
    return {candidates: result}, {candidates: keys}

DataAdaptor().add("market", _market)


def _feature_obj(
    candidates,
    **kwargs
):
    """
        Fetch single feature from db
    """
    obj = kwargs.get("obj", "SECURITY_NAME")
    if candidates:
        if len(candidates) > 1:
            range_str = f"{obj} in ('" + "','".join(candidates) + "')"
        else:
            range_str = f"{obj}='" + candidates[0] + "'"
    else:
        range_str = ""
    # print("_feature_obj kwargs: ", kwargs)
    # print("range_str: ", range_str)
    data = db.select_more(
        table = kwargs["table"],
        range_str = range_str,
        field = kwargs["field"]
    )
    # print("_feature_obj data: ", data)
    name_to_sources = {}
    if isinstance(kwargs["value"], str):
        for i in data:
            if i[kwargs["value"]] is None:
                continue
            name_to_sources[i[obj]] = i[kwargs["value"]]
    elif isinstance(kwargs["value"], list): # case for multi value
        for i in data:
            new_val = [i[j] for j in kwargs["value"]]
            name_to_sources[i[obj]] = new_val
    return name_to_sources

DataAdaptor().add("direct_single_value", _feature_obj)