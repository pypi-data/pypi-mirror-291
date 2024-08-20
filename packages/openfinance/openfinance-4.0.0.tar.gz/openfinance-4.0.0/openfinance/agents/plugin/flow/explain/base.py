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
from openfinance.agentflow.base_parser import BaseParser
from openfinance.agentflow.prompt.base import BasePromptTemplate
from openfinance.agents.agent.manager import RoleManager

from openfinance.agents.plugin.flow.explain.output_parser import TaskOutputParser
from openfinance.agents.plugin.flow.explain.prompt import PROMPT

class ExplainFlow(BaseFlow):
    name = "explain"
    description = "Analysis Data information to answer questions"
    inputs: List[str] = ["content"]
    prompt: BasePromptTemplate = PROMPT
    parser: BaseParser = TaskOutputParser()

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
        resp = await self.llm.acall(self.prompt.prepare(inputs, include_default=True))
        resp = self.parser.parse(resp.content)        
        return {self.output: resp}

if __name__ == "__main__":
    model = ChatGPT(
        model = "gpt-3.5-turbo",
        api_key = "",
        base_url = ""
    )
    flow = ExplainFlow.from_llm(model)
    result = asyncio.run(flow._acall(input="TSLA"))
    print(result)