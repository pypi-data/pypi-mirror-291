import copy
import json

from functools import reduce
from abc import ABC, abstractmethod
from pydantic import BaseModel, root_validator
from typing import (
    List,
    Any,
    Dict,
    Union
)

from openfinance.config import Config
from openfinance.config.macro import MLOG
from openfinance.utils.singleton import singleton
from openfinance.datacenter.database.base import DataBaseManager
from openfinance.datacenter.knowledge.entity_graph.base import EntityGraph
from openfinance.strategy.operator.base import OperatorManager
from openfinance.strategy.feature.data_adaptor import DataAdaptor

db = DataBaseManager(Config()).get("quant_db")

class Feature(BaseModel):
    name: str = ""
    fid: int = 0
    desc: str = ""
    source: Dict[str, Any] = {}
    operator: Dict[str, Any] = {}
    childrens: List[Dict[str, Any]] = []

    @classmethod
    def from_source(
        cls,
        *args,
        **kwargs
    ) -> "Feature":
        return cls(
            name=kwargs.get("name"),
            fid=kwargs.get("id"),
            desc=kwargs.get("desc"),
            source=kwargs.get("source", {}),
            operator=kwargs.get("operator", {}),
            childrens=kwargs.get("childrens", [])
        )

    def update(
        self,
        feature: Any
    ) -> None:
        self.name = feature.name
        self.fid = feature.fid
        self.desc = feature.desc
        self.source = feature.source
        self.operator = feature.operator
        self.childrens = feature.childrens

    def run(
        self,
        *args,
        **kwargs
    ):
        """
            Function to run all stocks
            data: {
                "name": {
                    "time": [],
                    "data": []
                }
            }
        """
        try:
            # print("kwargs: ", kwargs)
            MLOG.debug(f"self.source: {self.source}")
            candidates = kwargs.get("candidates", None)
            # third party feature directly
            if self.source.get("type", "") == "direct_single_value":
                data_adaptor = DataAdaptor().get("direct_single_value")
                data = data_adaptor(candidates, **self.source)
                # print("result: ", data)
                return {"result": data}
            # use feature from database                          
            elif kwargs.get("from_db", False):        
                data_adaptor = DataAdaptor().get(kwargs.get("type", ""))
                data, keys = data_adaptor(candidates, fid=self.fid)
                # print("data: ", data)
                # print("keys: ", keys)                
                if self.operator.get("latest", False) or kwargs.get("latest", False):
                    new_result = {k: v[-1] for k, v in data.items()}
                    new_key = {k: v[-1] for k, v in keys.items()}
                    # print("result: ", new_result)
                    return {"result": new_result, "TIME": new_key}
                return {"result": data, "TIME": keys}
            # fetch data to store feature              
            else:
                data_adaptor = DataAdaptor().get(self.source.get("type", ""))            
                if data_adaptor:
                    # print(self.source)
                    data = data_adaptor(candidates, **self.source)
                else:
                    if isinstance(candidates, str):
                        candidates = [candidates]     
                    data = {}
                    for name in candidates:
                        data[name] = self._user_source(name)
                
                result = {}
                key = {}
                for name, d in data.items():
                    # print(data)
                    try:
                        if isinstance(d, dict) and self.source.get("key", "") in d:
                            k = d[self.source.get("key", "")]
                            key[name] = k            
                        if isinstance(d, dict) and "data" in d:
                            d = d["data"]              
                        result[name] = self.eval(name=name, data=d)
                    except Exception as e:
                        print(name, e)
                return {"result": result, self.source.get("key", "TIME"): key}
        except Exception as e:
            print("name: ", self.name, " source: ", self.source, e)
            return

    def _user_source(
        self,
        name
    ):
        pass

    # @abstractmethod
    def eval(
        self,
        *args,
        **kwargs
    ):
        """
            Function to evaluate specific stocks
        """
        data = kwargs.get("data")
        op = self.operator.get("name", "")
        if OperatorManager().get(op):
            return OperatorManager().get(op)(data, **self.operator)
        return data

    def fetch(
        self,
        *args,
        **kwargs
    ) -> List[Any]:
        """
            Function to filter candidates with restrictions
            mode: "lt le eq ge gt in"
        """
        # print(kwargs)
        thresh = kwargs.get("thresh", 0)
        mode = kwargs.get("mode", "*")
        
        if self.source.get("type", "") == "direct_single_value": # fetch data from source
            kwargs["from_db"] = False 

        if kwargs.get("from_db", False):
            data = db.select_more(
                "t_stock_feature_map",
                range_str=f"fid={self.fid}",
                field="SECURITY_NAME,TIME,val"
            )
            result = {}
            name_to_TIME = {}
            # print("data: ", data)
            for d in data:
                name = d["SECURITY_NAME"]
                val = d["val"]
                t = d["TIME"]
                if name not in name_to_TIME or name_to_TIME[name] < t:
                    name_to_TIME[name] = t
                    if mode == "*":
                        result[name] = val
                    elif mode == "gt" and val > thresh:
                        result[name] = val
                    elif mode == "lt" and val < thresh:
                        result[name] = val
                    elif mode == "eq" and val == thresh:
                        result[name] = val
                    elif name in result:
                        result.pop(name)
                    else:
                        pass           
                # if mode == "gt":
                #     if val > thresh:
                #         if name not in name_to_TIME or name_to_TIME[name] > t:
                #             result[name] = val
                # elif mode == "lt":
                #     if val < thresh:
                #         if name not in name_to_TIME or name_to_TIME[name] > t:
                #             result[name] = val           
                # elif mode == "in":
                #     pass
                # elif mode == "eq":
                #     if val == thresh:
                #         result[name] = val
                # else: # choose all
                #     if name not in name_to_TIME or name_to_TIME[name] > t:
                #         result[name] = val             
            return result             
        else:
            data = self.run().get("result")
            if mode == "gt":
                return dict(filter(lambda x: x[1] > thresh, data.items()))
            elif mode == "lt":
                return dict(filter(lambda x: x[1] < thresh, data.items()))
            elif mode == "in":
                return # to do
            elif mode == "eq":
                return dict(filter(lambda x: x[1] == thresh, data.items()))              
            else:
                return data

@singleton
class FeatureManager:
    name_to_features: Dict[str, Feature] = {}

    def _add(
        self, 
        feature: Feature 
    ) -> None:
        try:
            if feature.name not in self.name_to_features:
                self.name_to_features.update({feature.name: feature})
            else:
                self.name_to_features[feature.name].update(feature)
        except Exception as e:
            raise e

    @property
    def features(
        self
    ):
        return self.name_to_features

    @property
    def names(
        self
    ):
        return [v.desc for v in self.name_to_features.values()]

    @property
    def stored_features(
        self
    ):
        """
            Get features should store into db
        """
        children_features = []
        result = {}
        for k, v in self.name_to_features.items():
            for child in v.childrens:
                children_features.append(child["name"])

        for k, v in self.name_to_features.items():
            if v.source.get("type", "") == "direct_single_value":
                continue
            if k in children_features:
                continue
            result[k] = v
        return result

    def register(
        self, 
        feature : Union[List[Feature], Feature, Dict[str, Any]]
    ) -> None:
        
        if isinstance(feature, list):
            for i in feature:
                self._add(i())
        elif isinstance(feature, dict):
            self._add(
                Feature.from_source(**feature)
            )
            if "childrens" in feature:
                chilrens = feature.pop("childrens")
                newfeature = copy.deepcopy(feature)
                for child in chilrens:
                    newfeature.update(child)
                    self._add(
                        Feature.from_source(**newfeature)
                    )
        else:
            self._add(feature())

    def register_from_file(
        self,
        file: str
    ):
        with open(file, "r") as infile:
            jsondata = json.load(infile)
            for d in jsondata["data"]:
                self.register(d)

    def get(
        self, 
        name: str
    ):
        if name in self.name_to_features:
            return self.name_to_features[name]
        return None

    def get_key_by_desc(
        self, 
        desc: str
    ):
        for v in self.name_to_features.values():
            if desc == v.desc:
                return v.name
        return None

    def get_feature_by_id(
        self,
        id: int
    ):
        for feat in self.name_to_features.values():
            if feat.fid == id:
                return feat

    def fetch_by_company(
        self,
        *args,
        **kwargs
    ):
        # print("kwargs: ", kwargs)
        return {v.desc: v.run(*args, **kwargs) for k, v in self.name_to_features.items() if v.fid < 100 and "SERIES" not in k}

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
        def relative_cmp(head_feature, tail_feature, mode):
            """
                two feature compare
            """
            head_data = self.name_to_features[head_feature].fetch(mode="*", from_db=True)
            tail_data = self.name_to_features[tail_feature].fetch(mode="*", from_db=True)
            # print("head_data: ", head_data)
            # print("tail_data: ", tail_data)
            results = {}
            for k, v in head_data.items():
                if k in tail_data:
                    if mode == "gt" and v > tail_data[k]:
                        results[k] = 0
                    elif mode == "lt" and v < tail_data[k]:
                        results[k] = 0
                    elif mode == "eq" and v == tail_data[k]:
                        results[k] = 0            
                    else:
                        pass
            return results

        if "params" not in kwargs:
            raise  f"pls input restrictions"

        params = kwargs["params"]

        values = []
        for i in params:
            try:
                # print("i: ", i)
                thresh = float(i[2])
                # print("thresh: ", thresh)
                values.append(self.name_to_features[i[0]].fetch(
                    mode=i[1],
                    thresh=thresh,
                    from_db=True
                ))
            except:
                values.append(relative_cmp(
                    i[0], i[2], i[1]
                ))
        keys = reduce(lambda a,b: a&b, map(dict.keys, values)) 
        return keys