# flake8: noqa
import time
import asyncio
import json
from typing import (
    Any, Callable, Dict, Iterable, List, Optional, Tuple
)
from openfinance.utils.recall.base import RecallBase
from elasticsearch import AsyncElasticsearch
from elasticsearch import Elasticsearch
from elasticsearch import helpers

class ES(RecallBase):
    name = "es"
    max_num = 800
    client: Elasticsearch
    asyncClient: AsyncElasticsearch

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    @classmethod
    def from_config(
        cls,
        config
    ):
        name = "abi"
        host = config[name].get("host", "localhost")
        port = config[name].get("port", 9200)
        max_num = config[name].get("max_recall_num", 800)
        client = Elasticsearch(
            hosts=[{'host': host, 'port': port, 'scheme': 'http'}],
            http_auth=("elastic", "154fbadc8fbad2ed")
        )
        asyncClient = AsyncElasticsearch(          
            hosts=[{'host': host, 'port': port, 'scheme': 'http', 'use_ssl': False}],
            http_auth=("elastic", "154fbadc8fbad2ed")
        )
        setting = {
            "settings": {
                "index": {
                    "similarity": {
                        "my_custom_bm25": {
                            "type": "BM25",
                            "k1": 1.8,
                            "b": 0.01
                        },
                    }
                }
            },
            "mappings": {
                "properties": {
                    "title": {
                        "type": "text",
                        "fields": {
                            "coarse": {
                                "type": "text",
                                "analyzer": "ik_smart",
                                "similarity": "my_custom_bm25"
                            },
                            "fine": {
                                "type": "text",
                                "analyzer": "ik_max_word",
                                "similarity": "my_custom_bm25"                                
                            }
                        }
                    },
                    "brand_name": {
                        "type": "keyword",                     
                    },
                    "org_name": {
                        "type": "keyword",                     
                    },
                    "region_name": {
                        "type": "keyword",                     
                    }                   
                }
            }
        }

        client.indices.create(index=name, body=setting, ignore=400)
       
        return cls(name=name, max_num=max_num, client=client, asyncClient=asyncClient)

    def insert(
        self,
        docs: Dict[str, Any]
    ):
        """
            docs: {'id': { 'title': 'new_value1', 'doc': 'new_value2'} },
        """
        """批量写入"""
        actions = []
        for sid, docs in docs.items():
            action = {
                "_index": self.name,
                "_type": "_doc",
                "_id": sid,
                "_source": docs
            }
            # print(index)
            actions.append(action)
        ret = helpers.bulk(self.client, actions)
        print(ret)
        return ret
    
    def delete(
        self,
        query = {"match_all": {}}
    ):
        body = {  
            "query": query
        }
        return self.client.delete_by_query(index=self.name, body=body)

    def update(
        self,
        id_to_docs: Dict[str, str]
    ):
        """
            docs : {'doc': 'new_value1', 'score': 'new_value2'}
        """
        actions = []  
        
        # 为每个要更新的文档创建一个更新动作  
        for doc_id, doc in id_to_docs.items():
            action = {  
                '_op_type': 'update',  
                '_index': self.name,  
                '_id': doc_id,  
                'script': {  
                    'source': 'ctx._source = params',  
                    'lang': 'painless',  
                    'params': doc  
                }  
            }  
            actions.append(action)  
        
        # 使用helpers.bulk函数执行批量更新  
        try:  
            success, failed = bulk(es, actions, stats_only=True)  
            # print(f'成功更新的文档数: {success}')  
            # print(f'更新失败的文档数: {failed}')  
        except BulkIndexError as e:  
            # 处理批量更新中的错误  
            print('批量更新过程中发生错误:', e)  
            # 你可以从e.errors中获取每个失败操作的详细信息  
            # for error in e.errors:  
            #     print(error)        

    def similarity_search(
        self, 
        q,
        size=200,
    ):
        def must(
            q
        ):
            result = {
                "must": []
            }
            for k, v in q.items():
                if k == "query":
                    result["must"].append({"match": {"title.coarse": v}})
                else:
                    result["must"].append({"match": {k: v}})
            return result

        if isinstance(q, dict):  # support for complicated search
            body = {
                "query": {
                    "bool": must(q)
                },
                "size": size
            }         
        else:
            body = {
                "query": {
                    "match": {
                        "title.coarse": q
                    }
                },
                "size": size
            }
        # print("body: ", body)
        docs = self.client.search(index=self.name,  body=body)
        # print("docs: ", docs)        
        results = []                     
        for doc in docs.body["hits"]["hits"][:self.max_num]:
            results.append({
                "content": doc["_source"],
                "score": doc['_score']
            })

        if len(results) < size:
            if isinstance(q, dict):
                q = q["query"]
            body = {
                "query": {
                    "match": {
                        "title.fine": q
                    }
                },
                "size": size
            }
            docs = self.client.search(index=self.name,  body=body)
            for doc in docs.body["hits"]["hits"][:self.max_num]:
                exist = False
                # print("doc", doc)
                source_doc = json.loads(doc["_source"]["doc"])
                for d in results:
                    # print("d", d)
                    result_doc = json.loads(d["content"]["doc"])              
                    if source_doc["id"] == result_doc["id"]:
                        exist = True
                if not exist:
                    results.append({
                        "content": doc["_source"],
                        "score": doc['_score']
                    })
        return results

    async def asimilarity_search(
        self, 
        q,
        size=200,
    ):
        def must(
            q
        ):
            result = {
                "must": []
            }
            for k, v in q.items():
                if k == "query":
                    result["must"].append({"match": {"title.coarse": v}})
                else:
                    result["must"].append({"match": {k: v}})
            return result

        if isinstance(q, dict):  # support for complicated search
            body = {
                "query": {
                    "bool": must(q)
                },
                "size": size
            }         
        else:
            body = {
                "query": {
                    "match": {
                        "title.coarse": q
                    }
                },
                "size": size
            }
        print("body: ", body)              
        docs = await self.asyncClient.search(index=self.name,  body=body)
        print("docs: ", docs)          
        results = []                     
        for doc in docs.body["hits"]["hits"][:self.max_num]:
            results.append({
                "content": doc["_source"],
                "score": doc['_score']
            })

        if len(results) < size:
            if isinstance(q, dict):
                q = q["query"]
            body = {
                "query": {
                    "match": {
                        "title.fine": q
                    }
                },
                "size": size
            }
            docs = await self.asyncClient.search(index=self.name,  body=body)
            for doc in docs.body["hits"]["hits"][:self.max_num]:
                exist = False
                # print("doc", doc)
                source_doc = json.loads(doc["_source"]["doc"])
                for d in results:
                    # print("d", d)
                    result_doc = json.loads(d["content"]["doc"])              
                    if source_doc["id"] == result_doc["id"]:
                        exist = True
                if not exist:
                    results.append({
                        "content": doc["_source"],
                        "score": doc['_score']
                    })
        return results

if __name__ == "__main__":
    es = ES.from_config({"es": {}})