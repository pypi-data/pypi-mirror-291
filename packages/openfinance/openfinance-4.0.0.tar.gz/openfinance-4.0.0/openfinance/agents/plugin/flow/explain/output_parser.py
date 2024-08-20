import re
import json

from typing import Dict

from openfinance.agentflow.base_parser import BaseParser

class TaskOutputParser(BaseParser):
    def parse(
        self, 
        text: str
    ) -> Dict[str, str]:
        print("TaskOutputParser input:\n ", text)
        try:
            vret = text.split("Analysis:")
            if len(vret) > 1:
                result = vret[-1].replace("*", "").replace("Based on the content,", "")
                return result
            return ""
        except:
            return ""