import asyncio
from typing import (
    Union,
    Dict,
    List,
    Any
)
from pydantic import BaseModel
from abc import ABC, abstractmethod
from openfinance.agentflow.flow.base import BaseFlow
from openfinance.agentflow.base import Runnable

class Skill(Runnable):
    """
        Skills is built-in ability
    """
    name: str = "Skill"
    description: str = "Self skill to solve defined problems"
    flow: Union[BaseFlow, None] = None
    inputs: List[str] = ["content"]    
    output: str = "output"

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    @classmethod
    def from_flow(
        cls,
        flow,
        **kwargs: Any
    ) -> "Skill":
        name = flow.name
        description = flow.description
        inputs = flow.inputs
        if "content" not in flow.inputs:
            inputs.append("content")
        return cls(name=name, description=description, flow=flow, inputs=inputs)

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
        pass
    
    async def _acall(
        self,
        *args: Any,        
        **kwargs: Any        
    ) -> Any:
        if self.flow:
            return await self.flow.acall(*args, **kwargs)
        else:
            return await self.acall(*args, **kwargs)

    async def acall(
        self,
        *args: Any,        
        **kwargs: Any        
    ) -> Any:
        if self.flow:
            return await self.flow.acall(*args, **kwargs)

    def update(
        self,
        **kwargs
    ):
        if self.flow:
            self.flow.update_prompt(**kwargs)        

    def schema(
        self,
    ):
        pass