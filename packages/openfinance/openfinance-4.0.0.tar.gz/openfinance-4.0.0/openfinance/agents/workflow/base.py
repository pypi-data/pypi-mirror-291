import asyncio
import json
from typing import (
    Any,
    Callable,
    Dict,
    Union,
    List
)
from pydantic import BaseModel

from openfinance.config.macro import MLOG
from openfinance.config import Config
from openfinance.utils.custom_copy import custom_copy
from openfinance.agents.workflow.node_base import Node, Edge

class Workflow(BaseModel):
    nodes: Dict[str, Node]
    edges: List[Edge]
    infos: Dict[str, Any]
    filename: str

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    @classmethod
    def from_file(
        cls,
        filename: str
    ):
        """
            Only support Single input node mode right now
        """
        nodes = {}
        edges = []
        infos = {}
        with open(filename, "r") as infile:
            print(filename)
            datajson = json.load(infile)
            if "flowData" in datajson: # user defined format
                flowData = datajson.pop("flowData")
                infos = datajson
                datajson = json.loads(flowData)
            nodes_data = datajson.pop("nodes", [])
            for node in nodes_data:
                node_instance = Node.from_config(node)
                nodes[node_instance.id] = node_instance

            edges_data = datajson.pop("edges", [])
            for edge in edges_data:
                edge_instance = Edge.from_config(edge)
                edges.append(edge_instance)
            if not infos:
                infos = datajson
        return cls(filename=filename, nodes=nodes, edges=edges, infos=infos)

    def update_graph(
        self,
        datajson,
        **kwargs
    ):
        self.nodes = {}
        self.edges = []
        flowData = datajson.pop("flowData")

        with open(self.filename, "r") as infile:
            olddata = json.load(infile)
        with open(self.filename, "w") as outfile:
            olddata["flowData"] = flowData
            json.dump(olddata, outfile, ensure_ascii=False, indent=2)  

        datajson = json.loads(flowData)
        nodes_data = datajson.pop("nodes", [])
        for node in nodes_data:
            node_instance = Node.from_config(node)
            self.nodes[node_instance.id] = node_instance

        edges_data = datajson.pop("edges", [])
        for edge in edges_data:
            edge_instance = Edge.from_config(edge)
            self.edges.append(edge_instance)

    def fetch_head(
        self,
    ):
        heads = []
        for k, item in self.nodes.items():
            if not item.inputAnchors:
                heads.append(k)
        return heads

    def fetch(
        self,
        node_id
    ):
        return self.nodes[node_id]

    async def arun(
        self,
        **kwargs
    ):
        session = WorkflowSession.from_workflow(self)
        return await session.arun(**kwargs)

class WorkflowSession(BaseModel):
    work_flow: Workflow
    node_data: Dict[str, Dict[str, Any]] = {}
    session_info: Dict[str, Any] = {}

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    @classmethod
    def from_workflow(
        cls,
        work_flow: Workflow
    ) -> 'WorkflowSession':
        return cls(work_flow=work_flow)

    async def arun(
        self,
        **kwargs        
    ):
        # step1: check inputAnchors' inputs are all completed
        # step2: call node
        # step3: call all childrens in outputAnchors
        heads = self.work_flow.fetch_head()
        for head in heads:
            MLOG.debug(f"head: {head}")
            result = await self.acall_node(node_id=head, **kwargs)
            self.node_data = {}
            # print("acall_node result: ", result)
            MLOG.debug(f"acall_node result: {result}")
            if result:
                return result

    async def acall_node(
        self,
        node_id,
        **kwargs
    ):
        """DFS"""
        MLOG.debug("*"*25)
        MLOG.debug(f"acall_node: {node_id}, init_kwargs: {kwargs}")
        node = self.work_flow.fetch(node_id)
        # new_kwargs = copy.deepcopy(kwargs)
        new_kwargs = custom_copy(kwargs)
        # Step 1: check all inputs are satisfied and mount inputs

        # print("self.node_data: ", self.node_data)        
        for term in self.work_flow.edges:
            # print("term: ", term)
            if node_id == term.target:
                # if params of sources is missing, then wait
                source_node_id = term.source
                if source_node_id not in self.node_data:
                    return
                else:
                    for inputAnchor in node.inputAnchors:
                        if inputAnchor["id"] == term.targetHandle:
                            source_data = self.node_data[source_node_id]
                            input_name = inputAnchor["name"]

                            for outputAnchor in self.work_flow.fetch(source_node_id).outputAnchors:
                                if outputAnchor["id"] == term.sourceHandle:
                                    # the match pair is node, then get the output name, only support unary parameter
                                    output_name = self.work_flow.fetch(source_node_id).output_name
                            # print("self.work_flow.fetch(source_node_id):", self.work_flow.fetch(source_node_id).outputAnchors)
                            # print("source_node_id: ", source_node_id)
                            # print("source_data: ", source_data)
                            # print("input_name: ", input_name, "output_name: ", output_name)
                            if output_name == "all":
                                new_kwargs[input_name] = source_data
                            elif output_name == "output":
                                new_kwargs[input_name] = source_data
                            elif not isinstance(source_data, dict):
                                new_kwargs[input_name] = source_data
                            elif output_name not in source_data:
                                new_kwargs[input_name] = source_data
                            else:
                                new_kwargs[input_name] = source_data[output_name]

        # Step 2: run it and cache result
        MLOG.debug(f"new_kwargs: {new_kwargs}")        
        result = await node.acall(**new_kwargs)
       
        if result:
            output = result.get("output")
            MLOG.info(f"output: {output}")       
            # Step 3: run iterately
            # if mapreduce then split tasks       
            if node.node.name == "map": 
                for subtask_kwargs in output:
                    # the value of map is value of subtask input, update in loop
                    self.node_data[node_id] = subtask_kwargs
                    for term in self.work_flow.edges:
                        if node_id == term.source:
                            result = await self.acall_node(term.target, **new_kwargs)
                            # reduce finished
                            if result:
                                return result
            else:
                self.node_data[node_id] = output                
                for term in self.work_flow.edges:
                    if node_id == term.source:
                        return await self.acall_node(term.target, **new_kwargs)
            return result