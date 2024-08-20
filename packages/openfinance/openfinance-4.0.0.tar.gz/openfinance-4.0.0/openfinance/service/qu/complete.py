from typing import Any, Dict
from openfinance.datacenter.knowledge.entity_graph.base import (
    EntityGraph, EntityEnum
)
from openfinance.agents.agent.manager import RoleManager
from openfinance.datacenter.database.source.eastmoney.util import get_current_date

ENTITY = EntityGraph()

class QueryComplete:
    @classmethod
    def process(
        cls,
        query: str,
        **kwargs
    ) -> Dict[str, Any]:

        name = kwargs.get("name", "")

        if ENTITY.is_company(name):
            kwargs["entity_type"] = EntityEnum.Company.type
            kwargs["industry"] = ENTITY.get_industry(name)
        elif ENTITY.is_industry(name):
            kwargs["entity_type"] = EntityEnum.Industry.type
        else:
            kwargs["entity_type"] = EntityEnum.Market.type

        if "DATE" not in kwargs:
            kwargs["DATE"] = get_current_date()

        if "role" in kwargs:
            role_kwargs = RoleManager().get_role_kwargs(kwargs["role"])
            if role_kwargs:
                kwargs.update(role_kwargs)
        return kwargs
    