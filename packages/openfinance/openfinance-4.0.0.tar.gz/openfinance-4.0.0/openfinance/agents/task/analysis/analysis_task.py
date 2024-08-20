import asyncio
import json
from typing import Dict
from openfinance.config import Config

from openfinance.agents.agent.base import Agent
from openfinance.agentflow.llm.manager import ModelManager 
from openfinance.agents.plugin.tool.factor_search import FactorSearchTool

from openfinance.agents.plugin.skill.base import SkillBox

from openfinance.datacenter.echarts.base import ChartManager
from openfinance.agents.task.base import Task

class AnalysisTask(Task):
    name = "analysis"

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
                tools={
                    "search": FactorSearchTool.create()           
                },
                skills= SkillBox(llm=llm).skills
            )

    async def aexecute(
        self,
        text,
        **kwargs
    ) -> Dict[str, str]:
        # plan
        plan_data = await self.agent.skills.get("plan").acall(
            text,
            **kwargs
        )

        plan_data = plan_data["output"]["result"]

        # analysis data
        summary_data = ""
        for item in plan_data:
            result = await self.agent.tools["search"].acall(
                item,
                **kwargs
            )
            print(detail_data)            
            detail_data = result["output"]
            analysis_result = await self.agent.skills.get("explain").acall(
                detail_data
            )
            summary_data += "Task(" + item + "):---\n"                    
            summary_data += analysis_result["output"] + "\n"
            summary_data += "---"
        # summary
        print("summary_data: ", summary_data)
        result = await self.agent.skills.get("summary").acall(**{
            "content": text,
            "document": str(summary_data)
        })
        print("result: ", result)
        return {self.output: result['output']}

if __name__ == '__main__':
    task = AnalysisTask()
    result = asyncio.run(
        task.aexecute(
            "是否可以买入贵州茅台的股票",
            role="Catherine Wood",
            name="贵州茅台",
            DATE="2023-11-11", 
            industry='酿酒行业'
        )
    )
    #result = asyncio.run(task.aexecute("为什么最近一直在下跌", name="华工科技"))
    #result = asyncio.run(task.aexecute("为什么游戏公司股价下跌这么多", name="游戏"))
    print(result)
