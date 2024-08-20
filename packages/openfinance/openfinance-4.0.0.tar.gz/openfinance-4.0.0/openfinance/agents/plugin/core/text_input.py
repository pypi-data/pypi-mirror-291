import asyncio
from typing import (
    Any,
    Callable,
    Dict,
    Union,
    List
)
from openfinance.agentflow.base import Runnable

class Input(Runnable):
    """
        Base Runnable
    """
    name: str = "input"
    input_params: List[str] = ["argument_name"]
    output: str = "text" 
    description: str = "A simple text input entrance"

    async def acall(
        self,
        *args: Any,        
        **kwargs: Any        
    ) -> Any:
        if "argument_name" in kwargs and kwargs["argument_name"]:
            argument_name = kwargs["argument_name"]
            if argument_name in kwargs:
                result = kwargs[argument_name]
        else:
            # default is text
            result = kwargs["text"]
        if args:
            return {"output": {"text": args}}
        else:
            return {"output": {"text": result}}