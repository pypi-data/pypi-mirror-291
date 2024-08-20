import asyncio
import json
from typing import Dict, List
from openfinance.config import Config
from openfinance.agentflow.llm.manager import ModelManager 
from openfinance.utils.recall.manager import IndexManager
from openfinance.datacenter.database.channel import analysis

from openfinance.datacenter.knowledge.graph import Graph
from openfinance.utils.recall.faiss import Faiss
from openfinance.datacenter.knowledge.executor import ExecutorManager
from openfinance.utils.embeddings.embedding_manager import EmbeddingManager
from openfinance.datacenter.knowledge.entity_graph.base import EntityGraph, EntityEnum

from openfinance.agents.plugin.flow.percept.opinion import PercepFlow
from openfinance.agents.plugin.flow.percept.match import MatchFlow

from openfinance.agentflow.tool.base import Tool


class PerceptTool(Tool):
    description = "To extract useful information from text"
    inputs: List[str] = ["content"]
    perceptflow: PercepFlow
    func: MatchFlow

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    @classmethod
    def create(cls) -> "PerceptTool":
        name = "percept"
        config = Config()
        llm = ModelManager(config).get_model("aliyungpt")

        index_manager = IndexManager()
        save_local = True
        if not save_local:
            graph = Graph(
                "openfinance/datacenter/knowledge/schema.md"
            )
            graph.assemble(ExecutorManager())
            db = Faiss.from_embedding(
                inputs = list(graph.factors.keys()), 
                embedding = EmbeddingManager().get_embedding(
                    config.get("index")[name]
                )
            )
            db.save("openfinance/datacenter/local_data", "factor")
            industry_db = Faiss.from_embedding(
                inputs = list(EntityGraph().industries),
                embedding = EmbeddingManager().get_embedding(
                    config.get("index")[name]
                )
            )
            industry_db.save("openfinance/datacenter/local_data", "industry")            
            company_db = Faiss.from_embedding(
                inputs = list(EntityGraph().companies.keys()),
                embedding = EmbeddingManager().get_embedding(
                    config.get("index")[name]
                )
            )
            company_db.save("openfinance/datacenter/local_data", "company")            
        else:
            db = Faiss.load(
                embedding = EmbeddingManager().get_embedding(
                    config.get("index")[name]),
                folder_path = "openfinance/datacenter/local_data", 
                index_name = "factor"                
            )
            industry_db = Faiss.load(
                embedding = EmbeddingManager().get_embedding(
                    config.get("index")[name]),
                folder_path = "openfinance/datacenter/local_data", 
                index_name = "industry"                
            )
            company_db = Faiss.load(
                embedding = EmbeddingManager().get_embedding(
                    config.get("index")[name]
                ),
                folder_path = "openfinance/datacenter/local_data", 
                index_name = "company"                
            )
        index_manager.register(name, db)
        index_manager.register(EntityEnum.Industry.type, industry_db)
        index_manager.register(EntityEnum.Company.type, company_db)

        perceptflow = PercepFlow.from_llm(
            llm
        )
        matchflow = MatchFlow.from_llm(
            llm,
            index_manager            
        )
        return cls(name=name, perceptflow=perceptflow, func=matchflow)

    async def acall(
        self, 
        text, 
        **kwargs
    ) -> Dict[str, str]:
        #print("enter async")
        percept_data = await self.perceptflow.acall(**{
            "content": text
        })
        # print("percept_data: ", percept_data)
        result = await self.func.acall(**{
            "content": percept_data["output"], 
            "channel": self.name,      
        })
        
        return {self.output: result['output']}

if __name__ == "__main__":
    tool = PerceptTool.create()
    result = asyncio.run(tool.acall("地方债务规模"))
    print(result)