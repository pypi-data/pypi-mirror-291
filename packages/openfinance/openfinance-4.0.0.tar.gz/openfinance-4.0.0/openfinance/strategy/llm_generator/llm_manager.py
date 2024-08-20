import os
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
from openfinance.datacenter.database.base import DataBaseManager
from openfinance.utils.singleton import singleton
from openfinance.service.error import StatusCodeEnum
db = DataBaseManager(Config()).get("db")

@singleton
class StrategyLLMManager:
    entity_to_roles : Dict[str, Any] = {}
    def __init__(
        self,
        filepath = "openfinance/strategy/llm_generator/conf/"
    ):
        name_to_files = [
            f"{filepath}{name}" for name in os.listdir(filepath)
        ]
        for file in name_to_files:
            with open(file, "r") as infile:
                jsondata = json.load(infile)
                self.entity_to_roles[jsondata["name"]] = jsondata["llm"]

    def get_entity_config(
        self,
        entity: Union[str, List[str]]
    ):
        if isinstance(entity, str):
            return self.entity_to_roles[entity]
        else:
            result = {}
            for i in entity:
                result.update(self.entity_to_roles[i])
            return result

    def get_llm_content(
        self,
        entity_type,
        role,
        name=None
    ):
        try:
            params = self.entity_to_roles[entity_type][role]
            if name:
                params["name"] = name
            range_str = " and ".join([k + "='" + v + "'" for k, v in params.items()])
            result = db.select_one("t_llm_factor_result", range_str=range_str, field="content")
            if result:
                return result["content"]
        except Exception as e:
            print(e)
        return StatusCodeEnum.DATA_LACK_ERROR.msg