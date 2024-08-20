import asyncio

from typing import Dict, List, Callable

from openfinance.config import Config
from openfinance.config import MLOG
from openfinance.utils.recall.faiss import Faiss
from openfinance.agentflow.llm.manager import ModelManager 
from openfinance.strategy.profile.base import ProfileManager
from openfinance.strategy.feature.base import FeatureManager
from openfinance.utils.recall.manager import IndexManager
from openfinance.utils.embeddings.embedding_manager import EmbeddingManager
import openfinance.strategy.feature.company

from openfinance.agents.plugin.flow.condition_filter.base import CompanyPicFlow
from openfinance.agentflow.tool.base import Tool

FM = FeatureManager()
PM = ProfileManager()

class CompanyPickTool(Tool):
    description = "根据预定的条件筛选公司的工具"
    inputs: List[str] = ["content"]
    func: CompanyPicFlow
    index: IndexManager

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    @classmethod
    def create(cls) -> "CompanyPickTool":
        name = "pick"
        config = Config()
        llm = ModelManager(config).get_model("aliyungpt")
        func = CompanyPicFlow.from_llm(llm)
        tag_db = Faiss.from_embedding(
            inputs = PM.names,
            embedding = EmbeddingManager().get_embedding(
                Config().get("index")[name]
            )
        )
        feat_db = Faiss.from_embedding(
            inputs = FM.names,
            embedding = EmbeddingManager().get_embedding(
                Config().get("index")[name]
            )
        )
        index_manager = IndexManager()        
        index_manager.register("tag", tag_db)
        index_manager.register("feat", feat_db)
        return cls(name=name, func=func, index=index_manager)

    async def acall(
        self, 
        text, 
        **kwargs
    ) -> Dict[str, str]:
        data = await self.func.acall(text)
        strategy = data.get("output", "")
        # strategy = [{"indicator": "RSI", "symbol": "gt", "value": 70}, {"indicator": "毛利率", "symbol": "gt", "value": 0.1}]
        result = []
        if len(strategy):
            mode = 0
            for s in strategy:
                if len(s) == 1:
                    feat_ret = self.index.search("tag", s["label"], top_k=1)
                    if len(feat_ret):
                        mode = 1
                        result = feat_ret[0]
                        break
                if len(s) == 3:
                    feat_ret = self.index.search("feat", s["indicator"], top_k=1)
                    feat_name = FM.get_key_by_desc(feat_ret[0])
                    if feat_name:
                        result.append((feat_name, s["symbol"], s["value"]))
                        mode = 3
            MLOG.debug(f"result: {result}")                        
            if mode == 1:
                result = PM.fetch_by_tags(result)
            elif mode == 3:
                result = FM.fetch(params=result)
            # print("result: ", result)

            if "callback_manager" in kwargs and len(result):
                callback_manager = kwargs["callback_manager"]
                table_data = FM.fetch_by_company(
                    candidates = list(result),
                    from_db=True,
                    type="company",
                    latest=True
                )
                columns = ["公司"]
                new_tabledata = {}
                # print("table_data: ", table_data)
                for k, v in table_data.items():
                    columns.append(k)
                    for ik, iv in v["result"].items():
                        if ik in new_tabledata:
                            new_tabledata[ik][k] = iv
                        else:
                            new_tabledata[ik] = {k: iv}
                tabledata = [{**v, "公司": k} for k, v in new_tabledata.items()]
                # print("tabledata: ", tabledata)
                table = {
                    "columns": columns,
                    "tabledata": tabledata
                }                
                # print("table: ", table)
                await callback_manager.trigger(
                    content = "",
                    table = table,
                    **kwargs     
                )
        return {self.output: str(result)}

if __name__ == "__main__":
    tool = CompanyPickTool.create()
    result = asyncio.run(tool.acall("挑选出RSI大于70, 毛利率高于0.1的股票", callback_manager=None))
    # result = asyncio.run(tool.acall("趋势反转的股票有哪些"))
    print(result)