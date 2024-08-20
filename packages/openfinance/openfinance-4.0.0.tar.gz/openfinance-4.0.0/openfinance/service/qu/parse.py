from typing import Any, Dict

class QueryParser:
    @classmethod
    def process(
        cls,
        query: str,
        **kwargs
    ) -> Dict[str, Any]:
        return kwargs
    