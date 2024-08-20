import asyncio
import aiohttp
import json
from typing import (
    Any,
    List,
    Dict,
    Union
)
from openfinance.config import Config
from openfinance.strategy.feature.base import FeatureManager
from openfinance.datacenter.database.base import DataBaseManager

import openfinance.strategy.feature.company

db = DataBaseManager(Config()).get("quant_db")

class ProfileManager:
    tagid_to_profile: Dict[int, Any] = {}
    tagname_to_tagid: Dict[str, int] = {}

    def __init__(
        self,
        filepath="openfinance/strategy/profile/company/tags.json"
    ):
        with open(filepath, "r") as infile:
            jsondata = json.load(infile)
            candidates = jsondata["tags"]
            self.tagid_to_profile = {v["tagid"]: v for k,v in candidates.items()}
            for k, v in candidates.items():
                self.tagname_to_tagid[v["name"]] = v["tagid"]
                for alias in v["alias"]:
                    self.tagname_to_tagid[alias] = v["tagid"]

    @property
    def tags(
        self
    ):
        return self.tagid_to_profile


    @property
    def names(
        self
    ):
        return list(self.tagname_to_tagid.keys())

    def run(
        self
    ):
        def trans(tags):
            result = []
            for d in tags:
                result.append((d["feature_name"],d["operator"],d["val"]))
            return result
        results = {}
        for k, v in self.tagid_to_profile.items():
            params = trans(v["conditions"])
            stocks = FeatureManager().fetch(params=params)
            results[v["tagid"]] = stocks
        return results

    def fetch_by_tags(
        self,
        tags: Union[Union[int, str], Union[List[int], List[str]]]
    ):
        """
            Filter companies by tags
        """
        # tagids = [] 暂时不添加组合查询
        if isinstance(tags, int):
            tagids = tags
        else:
            tag_id = self.tagname_to_tagid.get(tags, "")
            tagids = tag_id
            result = db.select_more(
                "t_stock_profile_map",
                range_str=f"tagid={tagids}",
                field="SECURITY_NAME"
            )
            # print(result)
            if result:
                return [d["SECURITY_NAME"] for d in result]

    def fetch_by_company(
        self,
        companies: Union[Union[int, str], Union[List[int], List[str]]]
    ):
        """
            Get tags of company
        """    
        if isinstance(companies, str):
            result = db.select_more(
                "t_stock_profile_map",
                range_str=f"SECURITY_NAME='{companies}'",
                field="tagid"
            )
            # print(result)
            if result:
                ret = []
                for r in result:
                    ret.append(self.tagid_to_profile[r["tagid"]]["name"])
                return ret
    def add(
        self,
        candidate
    ):
        sid = candidate["id"]
        sname = candidate["name"]
        self.tagid_to_profile[sid] = candidate
        self.tagname_to_tagid[sname] = sid