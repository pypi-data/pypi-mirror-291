from typing import Any, Dict

class QueryIntent:
    @classmethod
    def process(
        cls,
        query: str,
        **kwargs
    ) -> Dict[str, Any]:
        return kwargs
    
    