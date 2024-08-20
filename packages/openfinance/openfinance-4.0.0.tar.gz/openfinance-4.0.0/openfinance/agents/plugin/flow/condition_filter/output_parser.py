import json
from typing import Union, Dict

from openfinance.agentflow.base_parser import BaseParser

class FunctionOutParser(BaseParser):
    def parse(
        self, 
        text: str
    ) -> str:
        print("TaskOutputParser input:\n ", text)
        result = []
        try:
            vret = text.split("Result:")
            if len(vret) > 1:
                jsondata = json.loads(vret[1])
                data = jsondata["result"]
            return data
        except:
            return result