import pandas
import time
from openfinance.config import Config
from sqlalchemy.types import VARCHAR
from openfinance.datacenter.database.base import DataBaseManager
from openfinance.datacenter.database.storage.china.macro import (
    gdp,
    pmi,
    ppi,
    lpr,
    money_supply,
    cpi,
    consumer_faith,
    treasury_bond_yield,
    international_trade
)

db = DataBaseManager(Config()).get("db")

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
            "t_macro_" + func.__name__,
            {
                "TIME": VARCHAR(32),
                "DATE": VARCHAR(32)
            },
            single=True
            )
        idx += 1
    except:
        print(func.__name__, idx)
    if init:
        if func.__name__ == "treasury_bond_yield":
            db.execute("alter table t_macro_" + func.__name__ + " add PRIMARY KEY(`DATE`)")
        else:
            db.execute("alter table t_macro_" + func.__name__ + " add PRIMARY KEY(`TIME`)")

def build_marco(init=False):

    call_func(gdp, init=init)
    # alter table t_macro_gdp add PRIMARY KEY(`TIME`);

    call_func(pmi, init=init)
    # alter table t_macro_pmi add PRIMARY KEY(`TIME`);

    call_func(ppi, init=init)
    # alter table t_macro_ppi add PRIMARY KEY(`TIME`);

    call_func(lpr, init=init)
    # alter table t_macro_lpr add PRIMARY KEY(`TIME`);

    call_func(money_supply, init=init)
    # alter table t_macro_money_supply add PRIMARY KEY(`TIME`);

    call_func(cpi, init=init)
    # alter table t_macro_cpi add PRIMARY KEY(`TIME`);

    call_func(consumer_faith, init=init)
    # alter table t_macro_consumer_faith add PRIMARY KEY(`TIME`);

    call_func(treasury_bond_yield, init=init)
    # alter table t_macro_treasury_bond_yield add PRIMARY KEY(`DATE`);

    call_func(international_trade, init=init)
    
if __name__== "__main__":
    build_marco()