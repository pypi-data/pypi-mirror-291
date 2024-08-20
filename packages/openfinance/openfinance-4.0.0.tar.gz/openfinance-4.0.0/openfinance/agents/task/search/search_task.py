import asyncio
import json
from typing import Dict
from openfinance.config import Config

from openfinance.agents.task.base import Task
from openfinance.agentflow.llm.manager import ModelManager 

from openfinance.agents.agent.base import Agent
# from openfinance.agents.plugin.tool.search import SearchTool
from openfinance.agents.plugin.tool.factor_search import FactorSearchTool

class SearchTask(Task):
    name = "search"
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
                tools={"search": FactorSearchTool.create()}
            )

    async def aexecute(
        self, 
        text,   
        **kwargs
    ) -> Dict[str, str]:
        
        result = await self.agent.tools["search"].acall(
            text, **kwargs
        )
        if "websocket" not in kwargs:
            return {self.output: result}
        else:
            return {self.output: "小Q~为您找到以上信息~"} 

if __name__ == '__main__':
    task = SearchTask() 
    # result = asyncio.run(task.aexecute("Get Company Analysis", name="杰普特"))
    # result = asyncio.run(task.aexecute("Brand Strength", name="贵州茅台", industry="酿酒行业"))
    # result = asyncio.run(
    #     task.aexecute(
    #         "Sustainability", name="贵州茅台", DATE="2023-11-11", industry='酿酒行业'
    #     )
    # ) 
    result = asyncio.run(
        task.aexecute(
            "Valuation Analysis", name="贵州茅台", DATE="2023-11-11"
        )
    )                
    # print(result)
    # result = asyncio.run(task.aexecute("市盈率是多少", name="贵州茅台", role="Catherine Wood"))
    print(result)