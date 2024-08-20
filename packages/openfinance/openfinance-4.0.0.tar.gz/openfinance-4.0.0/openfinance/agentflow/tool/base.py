import asyncio
from typing import (
    Any,
    Callable,
    Dict,
    Union,
    List
)

from dataclasses import dataclass
from openfinance.agentflow.base import Runnable

class Tool(Runnable):
    """
        Tool is not built-in ability
    """    
    name: str = "Tool"
    description: str = "External tool to solve defined problems"
    inputs: List[str] = ["content"]    
    func: Callable
    output: str = "output"

    def __call__(
        self,
        *args: Any,        
        **kwargs: Any        
    ) -> Any:
        return self.call(*args, **kwargs)

    def call(
        self,
        *args: Any,
        **kwargs: Any        
    ) -> Any:
        return self.func(*args, **kwargs)
    
    async def _acall(
        self,
        *args: Any,        
        **kwargs: Any        
    ) -> Any:
        return await self.acall(*args, **kwargs)

    async def acall(
        self,
        *args: Any,        
        **kwargs: Any        
    ) -> Any:
        return await self.func.acall(*args, **kwargs)

@dataclass
class Action:
    name: str = ""
    action_input: Union[str, Dict[str, Any]] = ""