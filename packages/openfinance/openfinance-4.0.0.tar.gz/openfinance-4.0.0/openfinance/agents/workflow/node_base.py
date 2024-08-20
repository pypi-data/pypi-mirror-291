import asyncio
import json
import copy
from typing import (
    Any,
    Callable,
    Dict,
    Union,
    List
)
from pydantic import BaseModel
from openfinance.config import Config
from openfinance.agentflow.base import Runnable
from openfinance.agents.plugin.manager import RunnableManager

runnable_manager = RunnableManager()

class Node:
    id: str        
    node: Runnable 
    inputParams: List[Any]
    inputAnchors: List[Any]
    outputAnchors: List[Any]
    params: Dict[str, Any]
    inputs: Dict[str, Any] = {}    
    outputs: Dict[str, Any] = {}

    def __init__(
        self,
        node,        
        sid = None,
        inputParams = None,
        inputAnchors = None,
        inputs = None,
        outputAnchors = None,
        outputs = None,
        params = None
    ):
        if not sid:
            self.node = node
            self.id = node.name + "_0"
            self.params()
            self.inputParams()
            self.outputAnchors()
            self.inputAnchors()
            self.inputs()
        else:
            self.id = sid
            self.node = node
            self.inputParams = inputParams
            self.inputAnchors = inputAnchors
            self.inputs = inputs
            self.outputAnchors = outputAnchors
            self.outputs = outputs
            self.params = params  

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    def params(
        self,
    ):
        def get_baseClasses(node):
            classname = type(node)
            classes = [classname.__name__]
            while classname.__name__ != "Runnable":
                classname = classname.__base__
                classes.append(classname.__name__)
            return classes

        def get_type(baseClasses):
            if "Tool" in baseClasses:
                return "Tool"
            elif "Skill" in baseClasses:
                return "Skill"
            else:
                return "Runnable"

        baseClasses = get_baseClasses(self.node)
        classType = get_type(baseClasses)
        self.params = {
            "label": self.node.name.capitalize(),
            "version": 1,
            "name": self.node.name,
            "type": classType,
            "baseClasses": baseClasses,
            "category": classType,
        }

    def inputParams(
        self,
    ):
        self.inputParams = []
        for k, v in self.node.__dict__.items():
            if not callable(v) and k not in ["output", "inputs", "input_params"]:
                stype = "string" if isinstance(v, str)  else "number"
                v = json.dumps(v) if isinstance(v, dict) else v
                self.inputParams.append({
                    "label": k.capitalize(),
                    "name": k,
                    "type": stype,
                    "default": v,
                    "description": "",
                    "id": "-".join([self.id, "input", k, stype])
                })
        for k in self.node.input_params:
            self.inputParams.append({
                "label": k.capitalize(),
                "name": k,
                "type": "string",
                "default": "",
                "description": "",
                "id": "-".join([self.id, "input", k, "string"])
            })            

    def inputs(
        self,
    ):
        self.inputs = []
        for k, v in self.node.__dict__.items():
            if not callable(v) and k not in ["output", "inputs", "input_params"]:
                stype = "string" if isinstance(v, str) else "number"
                self.inputs.append({
                    "label": k.capitalize(),
                    "name": k,
                    "type": stype,
                    "placeholder": v
                })
            elif "inputs" == k:
                for i in self.node.__dict__["inputs"]:
                    self.inputs.append({
                        "label": i.capitalize(),
                        "name": i,
                        "type": "Runnable"
                        # "list": true,
                        # "optional": true,
                    })
        for k in self.node.input_params:
            self.inputs.append({
                "label": k.capitalize(),
                "name": k,
                "type": "string"
            })                     

    def inputAnchors(
        self,
    ):
        self.inputAnchors = []
        if "inputs" in self.node.__dict__:
            for i in self.node.__dict__["inputs"]:
                self.inputAnchors.append({
                    "label": i.capitalize(),
                    "name": i,
                    "type": "Runnable",
                    "description": "",
                    # "list": true,
                    # "optional": true,
                    "id": "-".join([self.id, "input", i, "Runnable"])
                })


    def outputAnchors(
        self,
    ):
        self.outputAnchors = []
        if "output" in self.node.__dict__:
            output = self.node.__dict__["output"]
            # if isinstance(output, str):
            #     output = [output]
            # for i in output:
            # print(self.node.name, self.node.__dict__["output"], output)
            self.outputAnchors.append({
                "id": "-".join(
                    [self.id, "output", self.node.name, "|".join(self.params["baseClasses"])] # to do 确定是output还是node.name
                ),
                "name": output,
                "label": output.capitalize(),
                "description": "",
                "type": " | ".join(self.params["baseClasses"])
            })

    @classmethod
    def from_config(
        cls,
        config: Dict[str, Any]
    ) -> "Node":
        data = config.pop("data", {})
        node_type = data.get("name","")
        node_instance = runnable_manager.get_node(node_type)
        sid = data.pop("id", "")
        # print("node_type: ", node_type)
        # print("node_instance: ", node_instance)
        inputParams = data.pop("inputParams")
        inputAnchors = data.pop("inputAnchors")
        inputs = data.pop("inputs")
        outputAnchors = data.pop("outputAnchors")
        outputs = data.pop("outputs")
        # print("data: ", data)
        return cls(
            sid = sid,
            node = node_instance,
            inputParams = inputParams,
            inputAnchors = inputAnchors,
            inputs = inputs,
            outputAnchors = outputAnchors,
            outputs = outputs,
            params = data
        )
        # return cls(node_instance)

    async def acall(
        self,
        **kwargs        
    ):
        for i in self.node.input_params:
            if i in self.inputs:
                if self.inputs[i]:
                    kwargs.update({i: self.inputs[i]})
            else:
                raise f"""{i} is not in {kwargs}"""
        return await self.node.acall(**kwargs)

    @property
    def output_name(
        self
    ):
        return self.node.__dict__["output"]

class Edge(BaseModel):
    source: str
    target: str
    stype: str = "buttonedge"
    targetHandle: str = ""    
    sourceHandle: str = ""
    id: str = ""
    
    @classmethod
    def from_config(
        cls,
        config: Dict[str, Any]
    ):
        return cls(**config)