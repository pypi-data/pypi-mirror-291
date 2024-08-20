import asyncio
import inspect
from typing import Any, Dict, List, Optional, Callable
from openfinance.utils.singleton import singleton

class Executor:
    '''
        class for factor functions, support user defined
    '''
    def __init__(
        self,
        name: str,
        signature: str,
        description: str,        
        func: Callable,
        graph_node: bool = True,
        extend: Dict[str, Any] = {}
    ):
        self.name = name
        self.signature = signature
        self.func = func
        self.description = description
        self.graph_node = graph_node
        self.extend = extend

    @classmethod
    def create(
        cls,
        name,
        signature,
        description,
        func,
        graph_node,
        extend = {}
    ) -> 'Executor':
        return cls(
            name=name, 
            signature=signature, 
            description=description, 
            func=func,
            graph_node=graph_node,
            extend = extend
            )
    
    @classmethod
    def from_func(
        cls,
        func,
        description,
    ) -> 'Executor':
        return cls(
            name=func.__name__, 
            signature="default", 
            description = description, 
            func=func
            )

    def __call__(
        self,
        *args: Any,        
        **kwargs: Any        
    ) -> Any:
        # print("self.name: ", self.name)
        return self.func(*args, **kwargs)


    async def acall(
        self,
        *args: Any,        
        **kwargs: Any      
    ) -> Any:
        # print("kwargs", kwargs)
        if inspect.iscoroutinefunction(self.func):
            return await self.func(*args, **kwargs)
        else:
            return self.func(*args, **kwargs)


@singleton
class ExecutorManager:
    name_to_executor = {}
    name_to_config = {}

    @property
    def config(
        self
    ):
        return self.name_to_config

    @property
    def executors(
        self
    ):
        return self.name_to_executor

    def register(
        self, 
        name,
        signature,
        exe
    ):
        self.name_to_executor[name + "|" + signature] = exe

    def register(
        self, 
        name,
        func,
        description,
        signature="default",
        graph_node=True,
        **args,
    ):
        key = name + "|" + signature
        if key in self.name_to_executor:
            print(key)
            raise f"Key already occurs: {key}"

        self.name_to_executor[name + "|" + signature] = Executor.create(
            name,
            signature,
            description,
            func,
            graph_node,
            args
        )
    
    def register_config(
        self,
        name,
        config,
        signature="default",
        **args
    ):
        key = name + "|" + signature
        if key in self.name_to_config:
            # print(key)
            raise f"Key already occurs: {key}"
        self.name_to_config[name + "|" + signature] = config

    def get(
        self, 
        name, 
        signature="default"
    ):
        return self.name_to_executor.get(name + "|" + signature, None)

    def build_recall(
        self
    ):
        recall_to_exe = {}
        for name, exe in self.name_to_executor.items():
            if exe.name:
                recall_to_exe[exe.name] = exe
            if exe.description:
                recall_to_exe[exe.description] = exe
            if "zh" in exe.extend:
                if isinstance(exe.extend['zh'], list):
                    for item in exe.extend['zh']:
                        recall_to_exe[item] = exe
                else:
                    recall_to_exe[exe.extend["zh"]] = exe                
        return recall_to_exe