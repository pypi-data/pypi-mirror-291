import asyncio
from typing import Dict, List

from openfinance.config import Config
from openfinance.config.macro import MLOG
from openfinance.agentflow.llm.manager import ModelManager 
from openfinance.utils.recall.manager import IndexManager
from openfinance.datacenter.database.channel import analysis
from openfinance.datacenter.knowledge.graph import Graph

from openfinance.utils.recall.faiss import Faiss

from openfinance.datacenter.knowledge.executor import ExecutorManager
from openfinance.utils.embeddings.embedding_manager import EmbeddingManager

from openfinance.agents.plugin.flow.recall.base import RecallFlow
from openfinance.agents.plugin.flow.function.base import FuncFlow
from openfinance.agentflow.tool.base import Tool

class FactorSearchTool(Tool):
    description = "Get result for indicator or query"
    input_params: List[str] = ["output_merge"]    
    inputs: List[str] = ["text"]
    recall: RecallFlow
    func: FuncFlow

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    @classmethod
    def create(cls) -> "FactorSearchTool":
        name = "search"
        config = Config()
        llm = ModelManager(config).get_model("aliyungpt")
        Graph().assemble(ExecutorManager())
        index_manager = IndexManager()
        save_local = False
        if not save_local:        
            db = Faiss.from_embedding(
                inputs = Graph().get_available_factors(),
                embedding = EmbeddingManager().get_embedding(
                    config.get("index")[name]
                )
            )
            # db.save("openfinance/datacenter/local_data", "search")            
        else:
            db = Faiss.load(
                embedding = EmbeddingManager().get_embedding(
                    config.get("index")[name]),
                folder_path = "openfinance/datacenter/local_data", 
                index_name = "search"                
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
        MLOG.debug(f"search kwargs: {kwargs}")

        recall_data = await self.recall.acall(**{
            "content": text, 
            "channel": self.name
            })
        # print("tools", recall_data)
        
        kwargs["tools"] = recall_data["output"]
        
        if "content" in kwargs:
            kwargs.pop("content")

        result = await self.func.acall(
            text,
            **kwargs  
        )
        result = result["output"]
        MLOG.debug(f"search result: {result}")
        if "callback_manager" in kwargs:
            callback_manager = kwargs["callback_manager"]
            await callback_manager.trigger(
                content = result,
                **kwargs
            )
        if "output_merge" in kwargs and kwargs["output_merge"]:
            if isinstance(result, list):
                result = "\n-\n".join([r["result"] for r in result])
                return {self.output: result}

        if isinstance(result, dict):
            return {self.output: result["result"]}
        else:
            return {self.output: result}

if __name__ == "__main__":
    tool = FactorSearchTool.create()
    result = asyncio.run(tool.acall("地方债务规模"))
    print(result)