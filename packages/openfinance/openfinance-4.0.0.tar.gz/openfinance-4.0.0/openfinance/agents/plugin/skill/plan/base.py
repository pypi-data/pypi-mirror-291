import asyncio
import json
from typing import (
    Any,
    Dict,
)

from openfinance.config.macro import MLOG
from openfinance.agents.plugin.flow.plan.base import PlanFlow
from openfinance.agentflow.skill.base import Skill
from openfinance.datacenter.echarts.base import ChartManager

class PlanSkill(Skill):
    name = "plan"
    description = "To plan a task"
    plans: Dict[str, Any] = {}

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    @classmethod
    def from_file(
        cls,
        llm,
        filepath: str = "openfinance/agents/plugin/skill/plan/plan.json",
        **kwargs: Any
    ) -> "PlanSkill":
        flow = PlanFlow.from_llm(
            llm,
            **kwargs
        )
        with open(filepath, "r") as infile:
            jsondata = json.load(infile)
            plans = jsondata.get("plan", {})

        return cls(flow=flow, plans=plans)

    def schema(
        self
    ):
        result = []
        for k, v in self.plans.items():
            result.append(
                {
                    "property": k, "type": "json", "value": json.dumps(v), "required": False
                }
            )
        return result

    async def acall(
        self, 
        content, 
        **kwargs
    ) -> Dict[str, str]:
        #print("enter async")
        role = kwargs.get("role", self.flow.prompt.get_defaults().get("role", ""))
        # print("role", role)
        # role = "Default"
        resp = self.plans.get(role, None) # defined plan according to role, and add joint mode later
        # print(content)
        if not resp:
            resp = await self.flow.acall(
                content,
                **kwargs
            )
            resp = resp.get("output", {})
        # print(resp)
        chart = ChartManager().get("tree")(resp)
        MLOG.debug(f"resp: {resp}")
        if "callback_manager" in kwargs:
            callback_manager = kwargs["callback_manager"]
            await callback_manager.trigger(
                content = "开始，请耐心等待...",
                chart = chart,
                **kwargs
            )
        subtasks = list(resp.keys())
        return {self.output: subtasks}