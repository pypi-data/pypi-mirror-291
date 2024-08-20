import asyncio
from typing import (
    Dict,
    Union,
    Any,
    List
)
from openfinance.service.error import StatusCodeEnum, wrapper_return

async def websocket_send(
    content = Union[List[Any], str, Dict[str, Any]],
    **kwargs  
):
    # print("websocket_send", input, kwargs)
    websocket = kwargs.get("websocket", None)
    if websocket:
        if websocket.open:
            if isinstance(content, list):
                for i in content:
                    await websocket.send(wrapper_return(
                        result=i, is_func=True, **kwargs
                    ))
            else:
                await websocket.send(wrapper_return(
                    result=content, is_func=True, **kwargs
                ))
        else:
            raise f"websocket lost"    