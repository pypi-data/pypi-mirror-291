from openfinance.agents.plugin.core.text_input import Input
from openfinance.agents.plugin.core.map import MapNode
from openfinance.agents.plugin.core.reduce import ReduceNode
from openfinance.agents.plugin.core.save_db import SaveDB
core_node = [
    Input,
    MapNode,
    ReduceNode,
    SaveDB
]