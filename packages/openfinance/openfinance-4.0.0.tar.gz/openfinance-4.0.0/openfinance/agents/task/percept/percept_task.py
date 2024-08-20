import asyncio
import json
from typing import Dict
from openfinance.config import Config

from openfinance.agents.agent.base import Agent
from openfinance.agentflow.llm.manager import ModelManager 
from openfinance.agents.plugin.tool.percept import PerceptTool
from openfinance.agents.plugin.callback.base import CallbackManager

from openfinance.datacenter.echarts.base import ChartManager
from openfinance.agents.task.base import Task

class PerceptTask(Task):
    name = "percept"
    def __init__(
        self,
        **kwargs        
    ):
        agents = kwargs.get("agents", None)
        if agents and isinstance(agents, Agent):
            self.agent = agents
        else:
            self.agent = Agent.from_scratch(
                llm = ModelManager(Config()).get_model("aliyungpt"),
                role="Stock Analyst",
                goal="Provide professional and helpful advices",
                tools={"percept": PerceptTool.create()}
            )
 
    async def aexecute(
        self, 
        text, 
        callback_manager = CallbackManager.from_func({}),        
        **kwargs
    ) -> Dict[str, str]:
        
        result = await self.agent.tools["percept"].acall(
            text, **kwargs
        )

        if "websocket" not in kwargs:
            return {self.output: send_data}
        else:
            return {self.output: "小Q~为您找到以上信息~"} 