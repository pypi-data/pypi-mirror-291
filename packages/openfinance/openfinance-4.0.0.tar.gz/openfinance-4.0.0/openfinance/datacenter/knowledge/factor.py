import asyncio
import copy
from typing import Any, Dict, List, Optional, Callable

from openfinance.config.macro import MLOG
from openfinance.datacenter.knowledge.executor import Executor
from openfinance.datacenter.knowledge.wrapper import wrapper

class Factor:
    '''
        class for factor, used in graph
    '''    
    def __init__(
        self,
        name: str,
        description: str,
        paths: List[List[str]],
        parents: List['Factor'] = [],
        childrens: Dict[str, 'Factor'] = {}, # childrens for different roads
        executor: Executor = None,
    ):
        self.name = name
        self.description = description
        self.paths = paths
        self.parents = parents
        self.childrens = childrens
        self.executor = executor

    @classmethod
    def create(
        cls,
        name: str,
        description: str
    ) -> 'Factor':
        return cls(name=name, description=description)

    def __call__(
        self,
        *args: Any,        
        **kwargs: Any        
    ) -> Any:
        """
            Args:
                    rootNode: original rootNode for choosing path
            Return:
                    list of dict
        """
        # print(self.name)
        # print(kwargs)
        pre_exes = kwargs.get("executor", []) # get existed function
        if self.executor.name in pre_exes:
            return 
        exes = copy.deepcopy(pre_exes)
        exes.append(self.executor.name)
        kwargs["executor"] = exes
        # print(self.childrens)
        # print(self.parents)
        # print("kwargs1: ", kwargs)
        result = self.executor(*args, **kwargs)
        if result:           
            if len(self.childrens):
                result = [result]
                for path, child in self.childrens.items():
                    # print("path: ", path, child.name)
                    if "-".join(exes) in path and child.executor: # if no excutor, drop it
                        # print(path, child.name)
                        child_ret = child(*args, **kwargs)
                        if child_ret: # if empty response, drop it
                            result.append(child_ret)
                return wrapper(result)
        return wrapper(result)

    async def acall(
        self,
        *args: Any,        
        **kwargs: Any        
    ) -> Any:
        """
            Args:
                    rootNode: original rootNode for choosing path
            Return:
                    list of dict
        """
        # print(self.name)
        # print(kwargs)
        pre_exes = kwargs.get("executor", [])
        funcs = kwargs.get("func", set())# get existed function

        # routine executor already activated previously
        if self.executor.name in pre_exes:
            return 
        # routine func already activated previously
        if self.executor.func.__name__ in funcs:
            return
        
        exes = copy.deepcopy(pre_exes)
        exes.append(self.executor.name)
        kwargs["executor"] = exes
        MLOG.debug(f"kwargs1: {kwargs}, self.name: {self.name}")
        result = await self.executor.acall(*args, **kwargs)
        if result:
            funcs.add(self.executor.func.__name__)
            kwargs["func"] = funcs            
            if len(self.childrens):
                result = [result]          
                for path, child in self.childrens.items():
                    MLOG.debug(f"children: {path}, exes: {exes}")
                    if "-".join(exes) in path and child.executor: # if no excutor, drop it
                        child_ret = await child.acall(*args, **kwargs)
                        if child_ret: # if empty response, drop it
                            result.append(child_ret)
                return wrapper(result)
        return wrapper(result)


    def add_path(
        self, 
        paths
    ):
        self.paths.append(paths)

    def register_func(
        self, 
        func: Executor
    ):
        self.executor = func
    
    def add_parents(
        self, 
        parent: 'Factor'
    ):
        if parent not in self.parents:
            self.parents.append(parent)

    def get_parents(
        self
    ) -> List['Factor']:
        return self.parents

    def add_childrens(
        self, 
        paths,
        child: 'Factor'
    ):
        name = "-".join(paths)
        if name not in self.childrens:
            self.childrens[name] = child

    def get_childrens(
        self
    ) -> Dict[str, 'Factor']:
        return self.childrens