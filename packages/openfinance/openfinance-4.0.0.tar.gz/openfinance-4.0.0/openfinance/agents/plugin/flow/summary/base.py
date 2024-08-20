import asyncio
from typing import (
    Any,
    Callable,
    Dict,
    Union,
    List
)
from openfinance.agentflow.flow.base import BaseFlow
from openfinance.agentflow.llm.chatgpt import ChatGPT
from openfinance.agentflow.prompt.base import BasePromptTemplate

from openfinance.agents.plugin.flow.summary.prompt import PROMPT

class SummaryFlow(BaseFlow):
    name = "summary"
    description = "Summary Informations to answer questions"
    inputs: List[str] = ["content", "document"]
    prompt: BasePromptTemplate = PROMPT

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    def update_prompt(
        self,
        **kwargs
    ):
        for var in self.prompt.variables:
            if var in kwargs:
                self.prompt.add_default({var: kwargs[var]})

    async def acall(
        self,
        content: str,
        **kwargs: Any        
    ) -> Dict[str, str]:

        inputs = {"content": content}
        inputs.update(kwargs)
        for i in self.inputs:
            if i not in inputs:
                return {self.output: "Input variable needed"}

        resp = await self.llm.acall(self.prompt.prepare(inputs, include_default=True))
        return {self.output: resp.content}

if __name__ == "__main__":
    model = ChatGPT(
        model = "gpt-3.5-turbo",
        api_key = "",
        base_url = ""
    )
    flow = SummaryFlow.from_llm(model)
    result = asyncio.run(flow._acall(input="TSLA"))
    print(result)