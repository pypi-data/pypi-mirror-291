import asyncio
import copy
from typing import (
    Any,
    Callable,
    Dict,
    Union,
    List
)
from openfinance.agentflow.base import Runnable

class MapNode(Runnable):
    """
        Base Runnable
    """
    inputs: List[str] = ["tasks"]
    name: str = "map"
    description: str = "Start point to split a task into subtask"
    output: str = "output" 

    async def acall(
        self,    
        **kwargs: Any        
    ) -> Any:
        tasks = kwargs.pop("tasks", [])
        if isinstance(tasks, dict):
            tasks = list(tasks.keys())
        return {self.output: tasks}