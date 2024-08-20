from typing import Any, Dict, List
from openfinance.utils.singleton import singleton
from openfinance.utils.embeddings import EMDEDDINGS

@singleton
class EmbeddingManager:
    def __init__(
        self
    ):
        self.name_to_embeddings = {
            k: v() for k, v in EMDEDDINGS.items()
        }
        # print("name_to_embeddings", self.name_to_embeddings)
        
    def get_embedding(
        self,
        config
    ):
        # print("config", self.name_to_embeddings)
        embedding = config.get("faiss", {}).get("embedding", "")
        try:
            self.name_to_embeddings[embedding]
        except:
            pass    
        return self.name_to_embeddings["cn"]