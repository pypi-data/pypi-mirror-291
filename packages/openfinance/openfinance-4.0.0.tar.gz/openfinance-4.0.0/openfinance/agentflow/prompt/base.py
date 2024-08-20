from typing import (
    Any,
    Callable,
    Dict,
    Union,
    List
)
from abc import abstractmethod, ABC
from pydantic import BaseModel
from jinja2 import Template

class BasePromptTemplate(BaseModel, ABC):
    prompt: str
    variables: List[str]
    defaults: Dict[str, str] = {}

    def get_variables(
        self
    ) -> List[str]:
        return self.variables

    def get_defaults(
        self
    ) -> Dict[str, str]:
        return self.defaults

    def add_default(
        self,
        kv: Dict[str, str]
    ):
        for k, v in kv.items():
            if k in self.variables:
                self.defaults[k] = v

    @abstractmethod
    def prepare(
        self,
        inputs: Dict[str, str],
        include_default=False   
    ):
        pass

    def __add__(
        self,
        strs: str
    ):
        self.prompt += strs

    def __iadd__(
        self,
        strs: str
    ):
        self.prompt += strs
        return self    

class PromptTemplate(BasePromptTemplate):
    def prepare(
        self,
        inputs: Dict[str, str],
        include_default=False    
    ):
        if include_default:
            inputs = {**self.defaults, **inputs}
        return self.prompt.format(**inputs)

class DynamicPromptTemplate(BasePromptTemplate):
    def prepare(
        self,
        inputs: Dict[str, str],
        include_default=False        
    ):
        if include_default:
            inputs = {**self.defaults, **inputs}        
        return Template(self.prompt).render(inputs)