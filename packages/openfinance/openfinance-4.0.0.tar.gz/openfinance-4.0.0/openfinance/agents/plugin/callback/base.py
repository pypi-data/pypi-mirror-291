import asyncio
from pydantic import BaseModel
from typing import (
    Dict,
    Callable
)

class CallbackManager(BaseModel):
    name_to_callbacks: Dict[str, Callable]

    @classmethod
    def from_func(
        cls,
        name_to_callbacks: Dict[str, Callable]
    ) -> "CallbackManager":
        name_to_callbacks = name_to_callbacks
        return cls(name_to_callbacks=name_to_callbacks)

    def register(
        self, 
        name, 
        callback
    ):  
        """注册回调函数"""  
        if callable(callback):
            self.name_to_callbacks.append(callback)
            if name not in self.name_to_callbacks:
                self.name_to_callbacks[name] = callback
        else:  
            raise ValueError("Callback must be callable.")  
  
    def unregister(
        self, 
        name
    ):  
        """注销回调函数"""  
        try:  
            self.name_to_callbacks.pop(name)
        except ValueError:  
            pass  # 如果回调函数不存在，则不执行任何操作  
    
    async def trigger(
        self,
        **kwargs           
    ):
        if "callback_name" in kwargs:
            callback_name = kwargs["callback_name"]
            if callback_name in self.name_to_callbacks:
                await self.name_to_callbacks[callback_name](**kwargs)
        else:
            result = []
            for k, v in self.name_to_callbacks.items():
                result.append(v(**kwargs))
            await asyncio.gather(*result)
        return