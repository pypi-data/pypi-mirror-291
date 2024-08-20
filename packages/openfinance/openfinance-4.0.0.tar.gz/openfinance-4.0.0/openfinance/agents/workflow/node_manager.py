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

from openfinance.agents.plugin.manager import RunnableManager
from openfinance.agents.workflow.node_base import Node
from openfinance.utils.singleton import singleton

runnable_manager = RunnableManager()

@singleton
class NodeManager:
    name_to_nodes = {}    
    def __init__(
        self
    ):
        for k, v in runnable_manager.nodes.items():
            self.name_to_nodes[k] = Node(node=v)

    @property
    def nodes(
        self
    ):
        return self.name_to_nodes

    def get(
        self,
        name
    ):
        return self.name_to_nodes.get(name, None)