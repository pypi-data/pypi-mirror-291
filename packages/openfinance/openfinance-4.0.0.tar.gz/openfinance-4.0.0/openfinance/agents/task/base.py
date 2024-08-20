import asyncio
from typing import (
    Union, List, Dict
)
from abc import ABC, abstractmethod

class Task(ABC):
    """
        A task could be solved by a group of Agents later
    """
    name = "task"
    output = "result"

    @abstractmethod
    def __init__(
        self,
        **kwargs        
    ):
        pass

    def from_file(
        self,
        filename: str       
    ):
        pass

    def execute(
        self, 
        text, 
        **kwargs
    ) -> Dict[str, str]:
        pass

    @abstractmethod
    async def aexecute(
        self, 
        text, 
        **kwargs
    ) -> Dict[str, str]:
        return self.execute(
            text,
            kwargs
        )        