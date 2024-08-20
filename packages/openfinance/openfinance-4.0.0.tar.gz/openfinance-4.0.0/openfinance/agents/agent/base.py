import asyncio
from typing import (
    Any,
    Dict
)

from openfinance.agentflow.llm.base import BaseLLM
from openfinance.agentflow.agent.agent_base import AgentBase
from openfinance.agentflow.base_parser import BaseParser

from openfinance.agents.agent.agent_prompt import AGENT_PROMPT
from openfinance.agents.agent.output_parser import SingleActionParser

class Agent(AgentBase):
    name: str = "agent"
    role: str = ""
    goal: str = ""
    parser: BaseParser = SingleActionParser()

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    @classmethod
    def from_scratch(
        cls,
        llm: BaseLLM,
        **kwargs: Any        
    ) -> "Agent":
        AGENT_PROMPT.add_default(kwargs)
        if "tools" in kwargs:
            tools = kwargs["tools"]
            AGENT_PROMPT.add_default({"tools": "\n".join([k + ": " + v.description for k, v in tools.items()])})
            AGENT_PROMPT.add_default({"tool_names": ",".join(list(tools.keys()))})

        # update inner skills according to inputs
        if "skills" in kwargs:
            for k, v in kwargs["skills"].items():
                v.update(**kwargs)

        return cls(
            llm=llm,
            prompt=AGENT_PROMPT,
            **kwargs
        )

    async def acall(
        self,
        content: str,
        **kwargs: Any 
    ) -> Dict[str, str]:
        inputs = {"content": content}
        for i in self.inputs:
            if i != "content":
                inputs[i] = kwargs[i]
        for k, v in inputs.items():
            if not isinstance(v, str):
                inputs[k] = str(v)

        if self.memory.history:
            inputs["chat_history"] = self.memory()

        resp = await self.llm.acall(self.prompt.prepare(inputs, include_default=True))
        if "tools" not in self.prompt.get_defaults():
            result = resp.content
        else:
            action = self.parser.parse(resp.content)
            print("action", action)
            if action.name == "Final":
                return {self.output: action.action_input, "finish": True}
            if action.name in self.tools:
                tool = self.tools[action.name] 

            result = await tool.acall(action.action_input, **kwargs)
            self.memory.add("Action", action.action_input)
            self.memory.add("Observation", result["output"])
        return result