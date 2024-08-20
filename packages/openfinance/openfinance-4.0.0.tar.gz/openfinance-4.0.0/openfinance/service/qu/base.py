from typing import Any, Dict
from openfinance.service.qu.parse import QueryParser
from openfinance.service.qu.extract import QueryExtractor
from openfinance.service.qu.intent import QueryIntent
from openfinance.service.qu.complete import QueryComplete

class QueryUnderstand:
    @classmethod    
    def process(
        cls,
        query,
        **kwargs
    ):
        results = QueryParser.process(query, **kwargs)
        results = QueryExtractor.process(query, **results)
        results = QueryIntent.process(query, **results)
        results = QueryComplete.process(query, **results)
        results["output_merge"] = True  # search result should merghe
        return results