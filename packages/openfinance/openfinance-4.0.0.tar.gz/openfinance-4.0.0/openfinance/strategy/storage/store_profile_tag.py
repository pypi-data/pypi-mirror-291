import asyncio
import json
import time
import datetime

from typing import Dict
from openfinance.config import Config
from sqlalchemy.types import VARCHAR
from openfinance.datacenter.database.base import DataBaseManager
from openfinance.strategy.profile.base import ProfileManager
from openfinance.datacenter.knowledge.entity_graph.base import EntityGraph
from openfinance.datacenter.database.source.eastmoney.util import (
    get_current_date,
    get_previous_date
)

ENTITY = EntityGraph()
DATE = get_current_date()
db = DataBaseManager(Config()).get("quant_db")

manager = ProfileManager()

def init_table():
    db.create_table(
        table = "t_stock_profile_map",
        contents = {
            "SECURITY_NAME": "varchar(16)",
            "SECURITY_CODE": "varchar(16)",        
            "tagid": "int",
            "TIME": "varchar(16)"
        }
    )
    db.exec("alter table t_stock_profile_map add PRIMARY KEY(`SECURITY_NAME`, `TIME`, `tagid`)")

def store_company_profile(
    init=False
):
    if init:
        init_table()
    tag_to_companies = manager.run()
    for tag_id, v in tag_to_companies.items():
        # if tag_id != 10001:
        #     continue
        for company in v:
            db.insert(
                "t_stock_profile_map",
                {
                    "SECURITY_NAME": company,
                    "SECURITY_CODE": ENTITY.companies[company]["code"],
                    "tagid": tag_id,
                    "TIME": DATE
                }
            )
    db.exec(f"delete from t_stock_profile_map where TIME< '{DATE}'")

if __name__ == "__main__":
    store_company_profile(init=False)