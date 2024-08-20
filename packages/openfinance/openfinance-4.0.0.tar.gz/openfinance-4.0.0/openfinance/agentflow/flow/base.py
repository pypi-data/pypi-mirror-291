import asyncio
from typing import (
    Any,
    Callable,
    Dict,
    Union,
    List
)
from dataclasses import dataclass

from openfinance.agentflow.llm.base import BaseLLM
from openfinance.agentflow.prompt.base import BasePromptTemplate
from openfinance.agentflow.base_parser import BaseParser
from openfinance.agentflow.base import Runnable

class BaseFlow(Runnable):
    name: str
    llm: BaseLLM
    prompt: Union[BasePromptTemplate, None] = None
    parser: Union[BaseParser, None] = None
    inputs: List[str] = ["content"]    
    output: str = "output"

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    @classmethod
    def from_llm(
        cls,
        llm: BaseLLM,
        **kwargs: Any        
    ) -> 'BaseFlow':
        return cls(llm=llm, **kwargs)

    def update_prompt(
        self,
        **kwargs
    ):
        for var in self.prompt.variables:
            if var in kwargs:
                self.prompt.add_default({var: kwargs[var]})

    def __call__(
        self,
        **kwargs: Any        
    ) -> Dict[str, str]:
        return self.call(**kwargs)

    def call(
        self,
        **kwargs: Any        
    ) -> Dict[str, str]:
        pass

    async def _acall(
        self,
        **kwargs: Any        
    ) -> Dict[str, str]:
        return await self.acall(**kwargs)

    async def acall(
        self,
        *args: Any,        
        **kwargs: Any        
    ) -> Dict[str, str]:
        """async func for flowCall"""
        if args:
            inputs = {"content": args[0]}
            inputs.update(kwargs)
        else:
            inputs = kwargs
        if self.prompt:
            llm_input = self.prompt.prepare(inputs, include_default=True)
        else:
            llm_input = kwargs["content"]
        resp = await self.llm.acall(llm_input)
        if self.parser:
            resp = self.parser.parse(resp.content)
        else:
            resp = resp.content
        return {self.output: resp}        