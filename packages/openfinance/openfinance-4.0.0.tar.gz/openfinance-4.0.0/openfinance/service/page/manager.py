import json
import os
from typing import Any, Dict

from openfinance.service.page.base import Page


class PageManager:
    name_to_pages: Dict[str, Page] = {}

    def __init__(
        self,
        filedir: str = "openfinance/service/page/config/"
    ):
        super().__init__()    
        for filename in os.listdir(filedir):
            instance = Page(filedir + filename)
            self.name_to_pages[instance.name] = instance
        print(self.name_to_pages)

    def get(
        self,
        name
    ):
        return self.name_to_pages.get(name, None)