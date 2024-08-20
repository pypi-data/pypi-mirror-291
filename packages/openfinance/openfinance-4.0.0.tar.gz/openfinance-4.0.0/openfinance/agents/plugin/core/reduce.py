import asyncio
from typing import (
    Any,
    Callable,
    Dict,
    Union,
    List
)
from openfinance.agentflow.base import Runnable

class ReduceNode(Runnable):
    """
        Base Runnable
    """
    name: str = "reduce"
    output: str = "output"
    description: str = "End point to split a task into subtask and collect result"
    inputs: List[str] = ["tasks", "subtask"]
    tasks: List[str] = []
    task_results: List[Any] = [] 

    async def acall(
        self,     
        **kwargs: Any        
    ) -> Any:
        """
            tasks and task_results match check
        """
        if "tasks" in kwargs:
            self.tasks = kwargs.get("tasks")
        if "subtask" in kwargs:
            task_result = kwargs.get("subtask", "")
            self.task_results.append(task_result)
        # print("ReduceNode: tasks", self.tasks)
        # print("ReduceNode: task_results", self.task_results)
     
        if len(self.task_results) == len(self.tasks):
            summary_data = ""
            for i in range(len(self.task_results)):
                summary_data += "Task(" + self.tasks[i] + "):---\n"                    
                summary_data += self.task_results[i] + "\n"
                summary_data += "---" 
            self.tasks = []
            self.task_results = []
            return {self.output: summary_data}
        return