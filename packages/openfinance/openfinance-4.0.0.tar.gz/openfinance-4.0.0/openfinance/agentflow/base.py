import asyncio
from typing import (
    Any,
    Callable,
    Dict,
    Union,
    List
)
from pydantic import BaseModel
from abc import ABC, abstractmethod

class Runnable(ABC, BaseModel):
    """
        Base Runnable
    """    
    name: str
    input_params: List[str] = [] # params used in acall, different based on Node
    description: str = ""

    @abstractmethod
    async def acall(
        self,
        *args: Any,        
        **kwargs: Any        
    ) -> Any:
        pass