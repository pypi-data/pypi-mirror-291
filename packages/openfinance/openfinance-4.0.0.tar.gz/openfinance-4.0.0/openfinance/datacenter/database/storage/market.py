import pandas
import time
import json
from openfinance.config import Config
from sqlalchemy.types import VARCHAR, TEXT
from openfinance.datacenter.database.base import DataBaseManager
from openfinance.utils.time import get_previous_date
from openfinance.datacenter.database.storage.china.market import (
    market_loan_money,
    market_north_money_flow
)

from openfinance.datacenter.database.source.event.jin10 import (
    get_event,
    get_economic
)

db = DataBaseManager(Config()).get("db")

def save_economic(
    init=False
):
    if init:
        db.exec(
            """
                CREATE TABLE t_daily_event(
                    id INT PRIMARY KEY,
                    data TEXT NOT NULL,
                    type VARCHAR(8),
                    DATE VARCHAR(16)
                );
            """
        )
    for idx in range(-5, 5, 1):
        DATE = get_previous_date(idx)
        events = get_economic(DATE)
        # print(events)
        for event in events:
            if event["star"] > 3:
                sid = event.pop("id")
                data = {
                    "DATE": DATE,
                    "id": sid,
                    "data": json.dumps(event, ensure_ascii=False),
                    "type": "data"
                }
                db.insert(
                    "t_daily_event",
                    data,
                    dup_key=["id"]
                )
        events = get_event(DATE)
        # print(events)
        for event in events:
            if event["star"] > 2:
                sid = event.pop("id")                
                data = {
                    "DATE": DATE,
                    "id": sid,                    
                    "data": json.dumps(event, ensure_ascii=False),
                    "type": "event"
                }
                db.insert(
                    "t_daily_event",
                    data,
                    dup_key=["id"]
                )

def call_func(
    func,
    init=False
):
    idx = 0
    try:
        data = func()
        time.sleep(0.5)
        db.insert_data_by_pandas(
            data, 
            "t_" + func.__name__,
            {
                "DATE": VARCHAR(32)
            },
            single=True
            )
        idx += 1
    except:
        print(func.__name__, idx)
    if init:
        db.execute("alter table t_" + func.__name__ + " add PRIMARY KEY(`DATE`)")

def build_market(init=False):
    call_func(market_loan_money, init=init)
    call_func(market_north_money_flow, init=init)

if __name__== "__main__":
    # build_market()
    save_economic()
    # alter table t_market_loan_money add PRIMARY KEY(`DATE`);