import json
import copy
import time
import asyncio
from typing import Any, Dict


from openfinance.datacenter.knowledge.executor import ExecutorManager
from openfinance.datacenter.database.channel import analysis 
from openfinance.datacenter.knowledge.entity_graph.base import EntityGraph, EntityEnum
from openfinance.datacenter.knowledge.scope import ScopeCodeEnum

EMG = ExecutorManager()

class Page:
    name = ""
    pages = []

    def __init__(
        self,
        filename: str = "openfinance/service/page/config/company.json"
    ):
        super().__init__()
        with open(filename, "r") as infile:
            jsondata = json.load(infile)
            self.name = jsondata["name"]
            self.pages = jsondata["pages"]

    async def fetch(
        self,
        **kwargs
    ):
        results = {}
        # print(EMG.name_to_executor)
        # print("kwargs: ", kwargs)
        # print("self.pages: ", self.pages)
        for page in self.pages:
            inner = {}
            # a_time = time.time()
            new_kwargs = copy.deepcopy(kwargs)
            new_kwargs.update(page["kwargs"])
            # print("inner: ", inner)
            tasks = [asyncio.create_task(EMG.get(e)(**new_kwargs)) for e in page["indicators"]]
            inner["indicator"] = await asyncio.gather(*tasks)
            # print("inner: ", inner)
            # b_time = time.time()
            # print("indicator time: ", b_time - a_time)            
            new_kwargs["source_config"] = {
                "limit_num": 120,
                "with_text": False
            }
            tasks = [asyncio.create_task(EMG.get(e)(**new_kwargs)) for e in page["charts"]]
            inner["charts"] = await asyncio.gather(*tasks)
            # print("inner: ", inner)
            # c_time = time.time()
            # print("charts time: ", c_time - b_time) 

            inner["docs"] = [{
                "title": "?",
                "doc": f"{e}的解释文字，使用llm分析展示",
                "source": "?"
            }]
            results[page["name"]] = inner
        return results
