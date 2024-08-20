# flake8: noqa
import asyncio
from typing import (
    Any,
    Callable,
    Dict,
    Union,
    List
)
from openfinance.utils.recall.manager import IndexManager

from openfinance.agentflow.flow.base import BaseFlow
from openfinance.agentflow.llm.chatgpt import ChatGPT
from openfinance.agentflow.llm.base import BaseLLM
from openfinance.agents.plugin.flow.percept.prompt import MATCH_PROMPT
from openfinance.agentflow.prompt.base import PromptTemplate
from openfinance.datacenter.knowledge.entity_graph.base import EntityEnum


class MatchFlow(BaseFlow):
    name = "MatchFlow"
    inputs: List[str] = ["content"]
    channel: str = "channel"
    index_manager: IndexManager
    prompt: PromptTemplate = MATCH_PROMPT

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    @classmethod
    def from_llm(
        cls,
        llm: BaseLLM,
        index_manager : IndexManager,         
        **kwargs: Any        
    ) -> 'MatchFlow':
        return cls(llm=llm, index_manager=index_manager, **kwargs)

    async def acall(
        self,
        content: Dict[str, Any],
        **kwargs: Any        
    ) -> Dict[str, Any]:
        #result = []
        try:
            print("content: ", content)
            indicator_name = content["indicator"]
            #  match indicator
            docs = self.index_manager.search(
                kwargs[self.channel],
                indicator_name
                )

            indicators = ",".join(docs)
            print("indicators", indicators)

            #  match industry/company fetch the fisrt one in semantic match
            index = self.index_manager.get(content['level'])
            if index:
                entity = content["main_entity"]
                docs = self.index_manager.search(
                    content['level'],
                    entity
                    )
                content["main_entity"] = entity + "|"+ docs[0]

            resp = await self.llm.acall(
                self.prompt.prepare({"content" : indicator_name, "indicators": indicators[:-1]}))
            content["indicator"] = indicator_name + "|" + resp.content
            print(content)
            return {self.output: content}
        except:
            return {self.output: ""}