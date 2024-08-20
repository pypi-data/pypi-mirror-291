import asyncio
import aiohttp
import json
import traceback

from abc import ABC, abstractmethod
from functools import reduce

from typing import (
    Any,
    List,
    Dict
)
from pydantic import BaseModel, root_validator

from openfinance.config import Config
from openfinance.config.macro import MLOG
from openfinance.datacenter.database.base import DataBaseManager

from openfinance.strategy.model.base import Model

db = DataBaseManager(Config()).get("quant_db")

class Strategy(ABC, BaseModel):
    name: str
    desc: str
    name_to_features: Dict[str, Any]
    model: Model

    @classmethod
    @abstractmethod    
    def from_file(
        cls,
        filename: str
    ):
        pass

    def run(
        self,
        *args,
        **kwargs    
    ):
        """
            data: dict(feature -> {stock: val})
        """
        try:
            # print("Strategy kwargs1: ", kwargs)
            if "candidates" not in kwargs:
                cands = db.exec("select distinct SECURITY_NAME from t_stock_feature_map")
                kwargs["candidates"] = [i["SECURITY_NAME"] for i in cands]
            # print("Strategy kwargs2: ", kwargs)
            if "features" not in kwargs:
                # print(kwargs)
                for k, v in self.name_to_features.items():
                    if not v:
                        print(k, v)
                kwargs["latest"] = True
                kwargs["features"] = {k: v.run(*args, **kwargs).get("result") for k, v in self.name_to_features.items()}

            # print("Strategy kwargs3: ", kwargs)
            result = self.model.run(*args, **kwargs)

            result = sorted(result.items(), key=lambda x: x[1])

            if "return_all" not in kwargs:
                result = result[:10]
            return {x[0]: x[1] for x in result}
        except Exception as e:
            MLOG.debug(e)
            traceback.print_exc()  
            # 或者，如果你想要获取堆栈跟踪的字符串表示，可以使用traceback.format_exc()  
            traceback_str = traceback.format_exc()  
            print("堆栈跟踪字符串:\n", traceback_str)

    def features(
        self,
        *args,
        **kwargs    
    ):
        """
            data: dict(feature -> {stock: val})
        """
        if "candidates" not in kwargs:
            cands = db.exec("select distinct SECURITY_NAME from t_stock_feature_map")
            kwargs["candidates"] = [i["SECURITY_NAME"] for i in cands]

        # print(self.name_to_features)
        if "features" not in kwargs:
            kwargs["features"] = {k: v.run(*args, **kwargs) for k, v in self.name_to_features.items()}

        return kwargs["features"]

    def fetch(
        self,
        *args,
        **kwargs
    ) -> List[Any]:
        """
            Function to fetch candidates with restrictions
            format: params: list[key, mode, condition]
            ex: a.fetch(params=[("OperationGrow", "gt", 10), ("OperationSpeedAcc", "lt", 10)])
        """
        if "params" not in kwargs:
            raise  f"pls input restrictions"
        params = kwargs["params"]
    
        values = []
        for i in params:
            values.append(self.name_to_features[i[0]].fetch(
                mode=i[1],
                thresh=float(i[2]),
                from_db=True
            ))
        keys = reduce(lambda a,b: a&b, map(dict.keys, values)) 
        return keys