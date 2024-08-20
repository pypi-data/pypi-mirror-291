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
from openfinance.agentflow.flow.base import BaseFlow
from openfinance.agentflow.llm.chatgpt import ChatGPT
from openfinance.agentflow.llm.base import BaseLLM
from openfinance.agentflow.base_parser import BaseParser
from openfinance.agentflow.prompt.base import PromptTemplate
from openfinance.agentflow.tool.base import Tool
from openfinance.agentflow.tool.base import Action

from openfinance.config.macro import MLOG
from openfinance.agents.plugin.flow.function.prompt import FUNC_PROPMT
from openfinance.agents.plugin.flow.function.output_parser import FunctionOutParser

class FuncFlow(BaseFlow):
    name = "FuncFlow"
    inputs: List[str] = ["content"]
    channel: str = "channel"
    prompt: PromptTemplate = FUNC_PROPMT
    parser: BaseParser = FunctionOutParser()

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    def create_prompt(
        self,
        tools: List[Tool]
    ) -> Dict[str, str]:
        return {
            "tools": "\n".join([f"{tool.name}: {tool.description}" for tool in tools]),
            "tool_names": ", ".join([tool.name for tool in tools])
        }

    async def acall(
        self,
        content: str,
        **kwargs: Any        
    ) -> Dict[str, str]:

        inputs = {"content": content}
        tools = kwargs.pop("tools", [])

        match = False
        # direct match equal
        for tool in tools:
            if tool.func is not FunctionType: # class            
                if tool.func.name == content:
                    action = Action(tool.name, kwargs)
                    match = True
                    MLOG.debug(f"direct match: {content}")
                    break
        # match through llm
        if not match:
            for i in self.inputs:
                if i != "content":
                    inputs[i] = kwargs[i]
            inputs.update(self.create_prompt(tools))
            resp = await self.llm.acall(self.prompt.prepare(inputs))
            action = self.parser.parse(resp.content)

        result = ""
        for tool in tools:
            if tool.name == action.name:
                action_input = action.action_input
                if "entity" in kwargs:
                    action_input = kwargs["entity"]
                # print("tool: ", tool, tool.func, action_input)
                MLOG.debug(f"tool: {tool.name}, {action_input}")
                iscoroutine = False
                if hasattr(tool.func, "acall"): # check if it's a executor class
                    iscoroutine = True
                if inspect.iscoroutinefunction(tool.func):
                    iscoroutine = True
                if iscoroutine:
                    if isinstance(action_input, List): # to improve later
                        result = []
                        for i in action_input:
                            if isinstance(i, dict):
                                tmp_ret = await tool.acall(**i)
                            else:
                                tmp_ret = await tool.acall(i)
                            if isinstance(tmp_ret, str):
                                result.append({
                                    "result": tmp_ret
                                })
                            else:
                                result.append(tmp_ret)
                        return {self.output: result}
                    if isinstance(action_input, dict):
                        # print("action_input", action_input)
                        result = await tool.acall(**action_input)
                    else:
                        result = await tool.acall(action_input)  
                else:
                    if isinstance(action_input, List):
                        result = []
                        for i in action_input:
                            if isinstance(i, dict):
                                tmp_ret = tool(**i)
                            else:
                                tmp_ret = tool(i)
                            if isinstance(tmp_ret, str):
                                result.append({
                                    "result": tmp_ret
                                })
                            else:
                                result.append(tmp_ret)
                        return {self.output: result}
                    if isinstance(action_input, dict):
                        result = tool(**action_input)
                    else:
                        result = tool(action_input)
                break                  
        if isinstance(result, str):
            return {self.output: {"result": result}}
        else:
            return {self.output: result}

if __name__ == "__main__":
    model = ChatGPT(
        model = "gpt-3.5-turbo",
        api_key = "",
        base_url = ""
    )
    flow = FuncFlow.from_llm(model, [])
    result = asyncio.run(flow._acall(input="TSLA"))
    print(result)