import asyncio
import json
import os
from typing import (
    Any,
    Callable,
    Dict,
    Union,
    List
)

from openfinance.agentflow.llm.base import BaseLLM
from openfinance.agentflow.flow.base import BaseFlow
from openfinance.agentflow.prompt.base import DynamicPromptTemplate

from openfinance.utils.singleton import singleton

@singleton
class FlowManager:
    """
        third_parties flow without parser
    """
    name_to_flows: Dict[str, BaseFlow] = {}

    def __init__(
        self,
        llm: BaseLLM,
        filepath: str = "openfinance/agents/third_party/plugin/flow/",
        **kwargs: Any
    ):
        files = os.listdir(filepath)
        for filename in files:
            file = filepath + filename
            jsondata = json.load(open(file, "r"))
            prompt = DynamicPromptTemplate(
                prompt=jsondata["prompt"], 
                variables=jsondata["variables"]
            )
            name = jsondata["name"]
            self.name_to_flows[name] = BaseFlow.from_llm(
                name = name,
                llm = llm, 
                prompt=prompt
            )

    @property
    def flows(
        self,
    ):
        return self.name_to_flows

    def get_flow(
        self,
        name
    ):
        return self.name_to_flows.get(name, None)

if __name__ == "__main__":
    import asyncio
    from openfinance.config import Config
    from openfinance.agentflow.llm.manager import ModelManager
    llm = ModelManager(Config()).get_model("aliyungpt")
    a = FlowManager(llm=llm)
    b = a.flows['wx_article']
    asyncio.run(b.acall('我在哪里'))