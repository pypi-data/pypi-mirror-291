import asyncio
import json
from typing import (
    Any,
    Dict,
)

from openfinance.strategy.policy.manager import StrategyManager
from openfinance.agentflow.skill.base import Skill

strategy = StrategyManager()

class RankSkill(Skill):
    name = "rank"
    description = "To rank stocks"
    ranks: Dict[str, Any] = {}
   
    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    @classmethod
    def from_file(
        cls,
        filepath: str = "openfinance/agents/plugin/skill/rank/rank.json",
        **kwargs: Any
    ) -> "PlanSkill":

        with open(filepath, "r") as infile:
            jsondata = json.load(infile)
            ranks = jsondata["fetch"]
        return cls(ranks=ranks)

    def schema(
        self
    ):
        result = []
        for k, v in self.ranks.items():
            result.append(
                {
                    "property": k, "type": "string", "value": v["strategy"], "required": False
                }
            )
        return result

    async def acall(
        self,
        content,
        **kwargs
    ) -> Dict[str, str]:
        #print("enter async")
        role = kwargs.get("role", "")
        candidates = kwargs.get("name", "")
        if candidates:
            if isinstance(candidates, str):
                candidates = [candidates]
            resp = strategy.get(name=role).run(
                candidates=candidates,
                from_db=True,
                type="company"           
            )
        else:
            resp = strategy.get(name=role).run(
                from_db=True,
                type="company"           
            )

        if resp:
            chart = ChartManager().get("bar")(
                resp,
                labels={"x": "Company", "y": "Score", "title": "模型打分排序"}
            )

            table = {
                "columns": ["公司", "分数"],
                "tabledata": [{"公司": k, "分数": v} for k, v in result["output"].items()]
            }
        else:
            chart = {}
            table = {}

        if "callback_manager" in kwargs:
            callback_manager = kwargs["callback_manager"]
            await callback_manager.trigger(
                content = text,
                chart = chart,
                table = table,            
                **kwargs
            )

        return {self.output: resp}