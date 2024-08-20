# flake8: noqa
import asyncio
from types import FunctionType
from typing import (
    Any,
    Dict,
    List
)
from openfinance.utils.recall.manager import IndexManager

from openfinance.agentflow.flow.base import BaseFlow
from openfinance.agentflow.llm.chatgpt import ChatGPT
from openfinance.agentflow.llm.base import BaseLLM
from openfinance.agentflow.tool.base import Tool

class RecallFlow(BaseFlow):
    name = "RecallFlow"
    inputs: List[str] = ["content"]
    channel: str = "channel"
    index_manager: IndexManager

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    @classmethod
    def from_llm(
        cls,
        llm: BaseLLM,
        index_manager : IndexManager,         
        **kwargs: Any        
    ) -> 'RecallFlow':
        return cls(llm=llm, index_manager=index_manager, **kwargs)

    async def acall(
        self,
        content: str,
        **kwargs: Any        
    ) -> Dict[str, str]:
        factors = self.index_manager.search(
            kwargs[self.channel],
            content
            )
        tools = []
        tool_names = []
        for factor in factors:
            if factor is not FunctionType: # class
                if "Factor" in factor.__class__.__name__:
                    func_name = factor.executor.func.__name__
                    description = factor.executor.description
                else: # Executor
                    func_name = factor.func.__name__
                    description = factor.description
            else:
                func_name = factor.__name__
                description = factor.__doc__.replace("\n", "")
            print("The functions is :", func_name)
            if func_name in tool_names:
                continue
            tool_names.append(func_name)
            tools.append(Tool(
                name = func_name,
                func = factor,
                description = description
            ))
            # to add args to each function
        return {self.output: tools}

if __name__ == "__main__":
    model = ChatGPT(
        model = "gpt-3.5-turbo",
        api_key = "",
        base_url = ""
    )
    index_manager = IndexManager()
    flow = RecallFlow.from_llm(model, index_manager)
    result = asyncio.run(flow._acall(input="TSLA"))
    print(result)