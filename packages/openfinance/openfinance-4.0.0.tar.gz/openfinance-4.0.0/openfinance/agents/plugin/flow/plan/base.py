import asyncio
import json
from typing import (
    Any,
    Dict,
    List
)
from openfinance.config.macro import MLOG
from openfinance.agentflow.flow.base import BaseFlow
from openfinance.agentflow.llm.chatgpt import ChatGPT
from openfinance.agentflow.llm.base import BaseLLM
from openfinance.agentflow.base_parser import BaseParser
from openfinance.agentflow.prompt.base import BasePromptTemplate
from openfinance.agents.agent.manager import RoleManager
from openfinance.agents.plugin.flow.plan.prompt import PLAN_PROMPT
from openfinance.agents.plugin.flow.plan.output_parser import TaskOutputParser

class PlanFlow(BaseFlow):
    name = "PlanFlow"
    description = "Divide a complicated task to subtasks"
    inputs: List[str] = ["content"]
    prompt: BasePromptTemplate = PLAN_PROMPT
    parser: BaseParser = TaskOutputParser()

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    @classmethod
    def from_llm(
        cls,
        llm: BaseLLM,
        **kwargs: Any        
    ) -> 'PlanFlow':
        if "role" in kwargs:
            role = kwargs["role"]            
            if RoleManager().get_role(role):
                PLAN_PROMPT.add_default(RoleManager().get_role_kwargs(role))
        PLAN_PROMPT.add_default(kwargs)
        return cls(llm=llm, prompt=PLAN_PROMPT, **kwargs)

    def update_prompt(
        self,
        **kwargs
    ):
        if "role" in kwargs:
            role = kwargs["role"]
            if RoleManager().get_role(role):
                self.prompt.add_default(RoleManager().get_role_kwargs(role))
        self.prompt.add_default(kwargs)

    async def acall(
        self,
        content: str,
        **kwargs: Any        
    ) -> Dict[str, str]:
        inputs = {"content": content}
        inputs.update(kwargs)
        MLOG.debug(f"plan_flow inputs: {inputs}")        
        resp = await self.llm.acall(self.prompt.prepare(inputs, include_default=True))
        MLOG.debug(f"plan_flow resp.content: {resp.content}")
        resp = self.parser.parse(resp.content)
        return {self.output: resp}

if __name__ == "__main__":
    model = ChatGPT(
        model = "gpt-3.5-turbo",
        api_key = "",
        base_url = ""
    )
    flow = PlanFlow.from_llm(model)
    result = asyncio.run(flow._acall(input="TSLA"))
    print(result)