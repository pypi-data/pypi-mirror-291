import asyncio
import json
import time
import datetime

from typing import Dict
from openfinance.config import Config
from sqlalchemy.types import VARCHAR
from openfinance.datacenter.database.base import DataBaseManager
from openfinance.agents.workflow.base import Workflow, WorkflowSession
from openfinance.strategy.llm_generator.llm_manager import StrategyLLMManager
from openfinance.datacenter.database.source.eastmoney.util import get_previous_date

strategy_llm_manager = StrategyLLMManager()
workflow = Workflow.from_file("./openfinance/agents/third_party/workflow/factorSummary.json")

db = DataBaseManager(Config()).get("db")
DATE = get_previous_date(1)

def init_table():
    db.create_table(
        "t_llm_factor_result",
        {
            "entity_type": "VARCHAR(16)",
            "name": "VARCHAR(16)",
            "factor_name": "VARCHAR(32)",
            "content": "TEXT",
            "TIME": "VARCHAR(16)"
        }
    )
    db.execute("alter table t_llm_factor_result add PRIMARY KEY(`entity_type`, `factor_name`, `name`)")

def store_factor_llm(
    init=False
):
    if init:
        init_table()
    session = WorkflowSession.from_workflow(workflow)
    name_to_params = strategy_llm_manager.get_entity_config(["Macro", "Market"])
    for k, param in name_to_params.items():
        result = asyncio.run(
            session.arun(
                DATE=DATE,
                **param      
            )
        )
        time.sleep(10)

if __name__ == "__main__":
    store_factor_llm(init=False)