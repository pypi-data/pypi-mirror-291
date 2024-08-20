import os
import json

from typing import (
    Dict, Any, Union
)
from pydantic import BaseModel

from openfinance.utils.singleton import singleton
from openfinance.agents.agent.agent_prompt import prompt

@singleton
class RoleManager:
    name_to_roles: Dict[str, Dict] = {}

    def __init__(
        self,
        filepath="openfinance/agents/agent/config/"
    ):
        files = os.listdir(filepath)
        for filename in files:
            file = filepath + filename
            jsondata = json.load(open(file, "r"))
            name = jsondata.get("name")
            self.name_to_roles[name] = jsondata

    @property
    def roles(
        self
    ):
        return self.name_to_roles

    def get_role(
        self, 
        name: str
    ):
        return self.name_to_roles.get(name, None)

    def get_role_by_id(
        self, 
        id: int
    ):
        for k, v in self.name_to_roles.items():
            if v["id"] == id:
                return v

    def get_role_kwargs(
        self,
        name: str
    ):
        if name in self.name_to_roles:
            return self.name_to_roles[name]["kwargs"]            

    def plugins(
        self,
        name: str
    ):
        schema = []
        if name in self.name_to_roles:
            for k, v in self.name_to_roles[name]["plugins"].items():
                for iv in v:
                    schema.append({
                        "name": iv,
                        "type": k,
                        "description": iv,
                        "required": True
                    })
        return schema

    def prompt(
        self,
        name: str
    ):
        return prompt