import asyncio
import json
from typing import Dict
from openfinance.config import Config

from openfinance.agents.agent.base import Agent
from openfinance.agentflow.llm.manager import ModelManager 
from openfinance.agents.plugin.tool.factor_search import FactorSearchTool
from openfinance.agents.plugin.callback.base import CallbackManager

from openfinance.agents.plugin.skill.base import SkillBox

from openfinance.datacenter.echarts.base import ChartManager
from openfinance.agents.task.base import Task

class RankTask(Task):
    name = "rank"

    def __init__(
        self,
        **kwargs        
    ):
        agents = kwargs.get("agents", None)
        if agents and isinstance(agents, Agent):
            self.agent = agents
        else:        
            llm = ModelManager(Config()).get_model("aliyungpt")
            self.agent = Agent.from_scratch(
                llm = llm,
                role="Catherine Wood",
                goal="Try your best to provide professional and helpful financial advices",
                skills= SkillBox(llm=llm).skills
            )

    async def aexecute(
        self,
        text,
        callback_manager = CallbackManager.from_func({}),
        **kwargs
    ) -> Dict[str, str]:

        result = await self.agent.skills.get("rank").acall(
            text,
            **kwargs
        )
        print("result", result)
        if "websocket" not in kwargs:
            return {self.output: result["output"]}
        return 
if __name__ == '__main__':
    task = RankTask()
    result = asyncio.run(
        task.aexecute(
            "对于这些公司排序",
            # role="Catherine Wood"
            role = "Warren Buffett"
        )
    )
    #result = asyncio.run(task.aexecute("为什么最近一直在下跌", name="华工科技"))
    #result = asyncio.run(task.aexecute("为什么游戏公司股价下跌这么多", name="游戏"))
    print(result)
