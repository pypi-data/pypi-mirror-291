from typing import Dict

from openfinance.agentflow.tool.base import Tool
from openfinance.agents.plugin.tool import sources
from openfinance.utils.singleton import singleton

@singleton
class ToolBox:
    name_to_tools: Dict[str, Tool] = {}

    def __init__(
        self,
        **kwargs
    ):
        name_to_tools = {}
        for s in sources:
            tool = s.create()
            if tool.name not in name_to_tools:
                self.name_to_tools[tool.name] = tool

    @property
    def tools(
        self,
    ):
        return self.name_to_tools

    def get_tool(
        self,
        name
    ):
        return self.name_to_tools.get(name, None)