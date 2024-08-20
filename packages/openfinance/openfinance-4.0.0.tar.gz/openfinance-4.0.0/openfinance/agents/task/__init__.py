# Self plan self run Agent Task or Multi Agent Task

from openfinance.agents.task.analysis.analysis_task import AnalysisTask
from openfinance.agents.task.search.search_task import SearchTask
from openfinance.agents.task.compare.compare_task import CompareTask
from openfinance.agents.task.search_sql.search_sql_task import SearchSqlTask
from openfinance.agents.task.percept.percept_task import PerceptTask
from openfinance.agents.task.percept.online_percept_task import OnlinePerceptTask
from openfinance.agents.task.rank.rank_task import RankTask

candidate_tasks = [
    AnalysisTask,
    SearchTask,
    CompareTask,
    SearchSqlTask,
    PerceptTask,
    OnlinePerceptTask,
    RankTask
]
