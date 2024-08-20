import asyncio
import json
import time

from typing import Dict
from openfinance.config import Config

from openfinance.agents.task.analysis.analysis_task import AnalysisTask

class AntoAnalysis(AnalysisTask):
    name = "autoAnalysis"

if __name__ == '__main__':
    task = AntoAnalysis()
    while True:
        result = asyncio.run(
            task.agent.acall(
                "比较比亚迪和贵州茅台的财务数据，谁值得投资", 
                company=["比亚迪","贵州茅台"]
            )
        )
        print(result)
        if "finish" in result:
            break
        time.sleep(2)