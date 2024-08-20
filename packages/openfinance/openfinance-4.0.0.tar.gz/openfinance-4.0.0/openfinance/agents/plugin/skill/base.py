from typing import Dict

from openfinance.agentflow.skill.base import Skill
from openfinance.agentflow.flow.base import BaseFlow
from openfinance.agents.plugin.skill import sources
from openfinance.utils.singleton import singleton

@singleton
class SkillBox:
    name_to_skills: Dict[str, Skill] = {}

    def __init__(
        self,
        **kwargs
    ):
        # name_to_skills = {}
        for s in sources:
            if issubclass(s, BaseFlow):
                self.from_flow(flow=s, **kwargs)
            else:
                skill = s.from_file(**kwargs)
                if skill.name not in self.name_to_skills:
                    self.name_to_skills[skill.name] = skill

    def from_flow(
        self,
        flow,
        **kwargs
    ):
        flow = flow.from_llm(**kwargs)
        if flow.name not in self.name_to_skills:
            self.name_to_skills[flow.name] = Skill.from_flow(flow, **kwargs)
    
    @property
    def skills(
        self,
    ):
        return self.name_to_skills

    def get_skill(
        self,
        name
    ):
        return self.name_to_skills.get(name, None)