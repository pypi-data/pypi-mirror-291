import os
import json
from typing import  Dict, List

from openfinance.config.macro import MLOG
from openfinance.utils.singleton import singleton
from openfinance.agents.workflow.base import Workflow

name_to_files = []
THIRD_PATH = "openfinance/agents/third_party/workflow/"
name_to_files += [
    f"{THIRD_PATH}{name}" for name in os.listdir(THIRD_PATH)
]

class WorkflowManager():
    """
        A Workflow could be solved by a group of Agents later
    """
    name_to_flows: Dict[str, Workflow] = {}
    def __init__(
        self
    ):
        for v in name_to_files:
            workflow = Workflow.from_file(v)
            self.name_to_flows[workflow.infos["name"]] = workflow    
    
    def add(
        self,
        filepath
    ):
        workflow = Workflow.from_file(filepath)
        self.name_to_flows[workflow.infos["name"]] = workflow

    def delete(
        self,
        sid
    ):
        return self.name_to_flows.pop(sid)

    @property
    def flows(
        self
    ) -> List[str]:
        '''
            default is for non Workflow chat
        '''
        return self.name_to_flows

    def get_flow_by_name(
        self,
        name: str
    ) -> Workflow:
        # print("get_flow_by_name: ", name)
        MLOG.info(f"get_flow_by_name: {name}")
        return self.name_to_flows.get(name, None)

    def get_flow_by_id(
        self,
        sid: str
    ) -> Workflow:
        MLOG.info(f"get_flow_by_id: {sid}")
        for k, v in self.name_to_flows.items():
            # print(v.infos, id, id ==  v.infos["id"], v.filename)
            if "id" in v.infos and str(sid) == v.infos["id"]:
                return v

    def save(
        self,
        name,
        data
    ):
        filename = "openfinance/agents/workflow/" + name + ".json"
        infile = open(filename, "w")
        json.dump(infile, data)