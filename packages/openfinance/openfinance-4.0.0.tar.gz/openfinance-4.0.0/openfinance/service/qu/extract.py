
from typing import Any, Dict

from openfinance.datacenter.knowledge.entity_graph.base import (
    EntityGraph, EntityEnum
)
from openfinance.config.macro import MLOG
from openfinance.agents.agent.manager import RoleManager
from openfinance.agents.workflow.manager import WorkflowManager
from openfinance.agents.plugin.tool.base import ToolBox

ENTITY = EntityGraph()

class QueryExtractor:
    @classmethod
    def process(
        cls,
        query: str,
        **kwargs
    ) -> Dict[str, Any]:
        
        if "company" in kwargs:
            kwargs["entity"] = kwargs.pop("company")

        entity = ENTITY.extract_entity(query)
        if entity:
            kwargs["entity"] = entity

        for t, v in RoleManager().name_to_roles.items():
            if query.lower().startswith("@" + t):
                kwargs["role"] = t
                kwargs["true_query"] = query[len(t)+1:]

        for t in WorkflowManager().flows.keys():
            if query.startswith("@" + t):
                kwargs["task"] = t
                kwargs["true_query"] = query[len(t)+1:]
        for t in ToolBox().tools.keys():
            if query.startswith("@" + t):
                kwargs["task"] = t
                kwargs["true_query"] = query[len(t)+1:]
          
        MLOG.debug(f"QueryExtractor kwargs: {kwargs}")
        return kwargs