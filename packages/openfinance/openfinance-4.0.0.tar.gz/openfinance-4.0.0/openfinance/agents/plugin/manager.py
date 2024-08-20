from typing import Dict
from openfinance.config import Config
from openfinance.agentflow.base import Runnable
from openfinance.utils.singleton import singleton
from openfinance.agentflow.llm.manager import ModelManager

from openfinance.agents.plugin.core import core_node
from openfinance.agents.plugin.skill.base import SkillBox
from openfinance.agents.plugin.tool.base import ToolBox


llm = ModelManager(Config()).get_model("aliyungpt")

skillbox = SkillBox(llm=llm)
toolbox = ToolBox()

@singleton
class RunnableManager:
    name_to_nodes: Dict[str, Runnable] = {}

    def __init__(
        self,
        **kwargs
    ):
        for node in core_node:
            node_instance = node()
            self.name_to_nodes[node_instance.name] = node_instance
        self.name_to_nodes.update(skillbox.skills)
        self.name_to_nodes.update(toolbox.tools)
        # print(self.name_to_nodes)

    @property
    def nodes(
        self,
    ):
        return self.name_to_nodes

    def get_node(
        self,
        name
    ):
        return self.name_to_nodes.get(name, None)