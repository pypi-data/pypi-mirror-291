import asyncio

from typing import Dict, List

from openfinance.config import Config
from openfinance.agentflow.llm.manager import ModelManager 
from openfinance.utils.recall.manager import IndexManager
from openfinance.datacenter.database.channel import search

from openfinance.utils.recall.faiss import Faiss

from openfinance.datacenter.knowledge.executor import ExecutorManager
from openfinance.utils.embeddings.embedding_manager import EmbeddingManager

from openfinance.agents.plugin.flow.recall.base import RecallFlow
from openfinance.agents.plugin.flow.function.base import FuncFlow
from openfinance.agentflow.tool.base import Tool


class SearchTool(Tool):
    description = "Get result for explicit indicator or easy query"
    inputs: List[str] = ["content"] 
    recall: RecallFlow
    func: FuncFlow

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    @classmethod
    def create(cls) -> "SearchTool":
        name = "fsearch"
        config = Config()
        llm = ModelManager(config).get_model("aliyungpt")

        index_manager = IndexManager()
        db = Faiss.from_embedding(
            inputs = ExecutorManager().build_recall(),
            embedding = EmbeddingManager().get_embedding(
                config.get("index")[name]
            )
        )
        index_manager.register(name, db)
        recall = RecallFlow.from_llm(
            llm, 
            index_manager
        )
        func = FuncFlow.from_llm(
            llm
        )
        return cls(name=name, recall=recall, func=func)

    async def acall(
        self, 
        text, 
        **kwargs
    ) -> Dict[str, str]:
        #print("enter async")     
        recall_data = await self.recall.acall(**{
            "content": text, 
            "channel": self.name
            })
        # print("tools", recall_data)

        kwargs["tools"] = recall_data["output"]
        kwargs.pop("content")        
        result = await self.func.acall(
            text,
            **kwargs
        )
        return result

if __name__ == "__main__":
    tool = SearchTool.create()
    result = asyncio.run(tool.acall("地方债务规模"))
    print(result)