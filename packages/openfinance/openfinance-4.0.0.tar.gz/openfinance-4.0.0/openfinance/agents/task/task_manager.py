from typing import  Dict, List
from openfinance.utils.singleton import singleton
from openfinance.agents.task.base import Task
from openfinance.agents.task import candidate_tasks

@singleton
class TaskManager():
    """
        A task could be solved by a group of Agents later
    """
    tasks: Dict[str, Task] = {}
    def __init__(
        self,
        config
    ):
        tasks = config.get('task')
        for task in candidate_tasks:
            if task.name in tasks:
                self.tasks[task.name] = task()
    
    def get_tasks(
        self
    ) -> List[str]:
        '''
            default is for non task chat
        '''
        return list(self.tasks.keys()) + ["default"]

    def get_task_by_name(
        self,
        name: str
    ) -> Task:
        return self.tasks.get(name, None)
