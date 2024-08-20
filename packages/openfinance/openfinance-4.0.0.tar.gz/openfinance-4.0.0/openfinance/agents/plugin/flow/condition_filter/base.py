# flake8: noqa
import asyncio
import inspect
from types import FunctionType
from typing import (
    Any,
    Callable,
    Dict,
    Union,
    List
)
from openfinance.config.macro import MLOG

from openfinance.agentflow.flow.base import BaseFlow
from openfinance.agentflow.llm.chatgpt import ChatGPT
from openfinance.agentflow.llm.base import BaseLLM
from openfinance.agentflow.base_parser import BaseParser
from openfinance.agentflow.prompt.base import PromptTemplate

from openfinance.agents.plugin.flow.condition_filter.prompt import FUNC_PROPMT
from openfinance.agents.plugin.flow.condition_filter.output_parser import FunctionOutParser

class CompanyPicFlow(BaseFlow):
    name = "CompanyPicFlow"
    inputs: List[str] = ["content"]
    prompt: PromptTemplate = FUNC_PROPMT
    parser: BaseParser = FunctionOutParser()

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    async def acall(
        self,
        content: str,
        **kwargs: Any
    ) -> Dict[str, str]:

        inputs = {"content": content}
        resp = await self.llm.acall(self.prompt.prepare(inputs))
        print(resp)
        result = self.parser.parse(resp.content)
        return {self.output: result}

if __name__ == "__main__":
    model = ChatGPT(
        model = "gpt-3.5-turbo",
        api_key = "",
        base_url = ""
    )
    flow = CompanyPicFlow.from_llm(model, [])
    result = asyncio.run(flow._acall(input="TSLA"))
    print(result)