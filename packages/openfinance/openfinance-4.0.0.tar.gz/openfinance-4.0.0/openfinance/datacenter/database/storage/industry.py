import pandas
import time
import pandas as pd

from openfinance.config import Config
from sqlalchemy.types import VARCHAR
from openfinance.datacenter.database.base import DataBaseManager
from openfinance.datacenter.knowledge.entity_graph.base import EntityGraph, EntityEnum
from openfinance.datacenter.database.source.eastmoney.util import get_previous_date
from openfinance.datacenter.database.storage.china.industry import *

from openfinance.datacenter.database.source.eastmoney.util import report_date

config = Config()
quant_db = DataBaseManager(Config()).get("quant_db")
DATE = get_previous_date(360)
ENTITY = EntityGraph()

db = DataBaseManager(Config()).get("db")

report_dates = report_date()["报告日期"].tolist()[0:12]

def store_north_money_to_sector(
    date = [None],
    init=False
):
    idx = 0
    if init:
        date = report_dates
    for v in date:
        try:
            data = north_money_to_sector(v)
            print(idx, v)
            time.sleep(0.5)
            db.insert_data_by_pandas(
                data, 
                "t_industry_north_money_to_sector",
                {
                    "INDUSTRY_NAME": VARCHAR(16),
                    "DATE": VARCHAR(32),
                    "INTERVAL_TYPE": VARCHAR(8)
                },
                single=True                
                )
            idx += 1
        except:
            print(v, idx)
            continue
    if init:
        db.execute("alter table t_industry_north_money_to_sector add PRIMARY KEY(`INDUSTRY_NAME`, `INTERVAL_TYPE`)")

def store_industy_all_valuation(
    init=False
):
    try:
        data = industy_all_valuation()
        time.sleep(0.5)
        db.insert_data_by_pandas(
            data, 
            "t_industy_all_valuation",
            {
                "INDUSTRY_NAME": VARCHAR(16),
            },
            single=True                
            )
    except Exception as e:
        print(e)

    if init:
        db.execute("alter table t_industy_all_valuation add PRIMARY KEY(`INDUSTRY_NAME`)")

def store_industry_quant_data(
    init=False
):
    if init:
        quant_db.create_table(
            "t_basic_industy_daily_kline",
            {
                "DATE":"varchar(16)",
                "SECURITY_NAME": "varchar(32)",
                "SECURITY_CODE": "text",
                "value": "double",
                "turnover": "double",
                "turnover_rate": "double",        
            })
        quant_db.execute("alter table t_basic_industy_daily_kline add PRIMARY KEY(`SECURITY_NAME`, `DATE`)")
    else:
        quant_db.execute(f'delete from t_basic_industy_daily_kline where DATE < {DATE}')    
    
    ind_to_coms = ENTITY.get_industry_company()
    all_data = quant_db.exec("select DATE, SECURITY_NAME, turnover, turnover_rate from t_basic_daily_kline")
    DATE_to_COM_TO_VAL = {}
    for d in all_data:
        try:        
            if d["DATE"] not in DATE_to_COM_TO_VAL:
                DATE_to_COM_TO_VAL[d["DATE"]] = {}
            DATE_to_COM_TO_VAL[d["DATE"]][d["SECURITY_NAME"]] = {
                "value": d["turnover"] / d["turnover_rate"] * 100.,
                "turnover": d["turnover"]
            }
        except Exception as e:
            print(f"Error: {e}")

    idx = 0
    for k, cmps in ind_to_coms.items():
        try:
            dates_to_vals = {}
            for vad_date, companies_values in DATE_to_COM_TO_VAL.items():
                for iv in cmps:
                    if iv in companies_values:
                        c_data = companies_values[iv]
                        if vad_date in dates_to_vals:
                            dates_to_vals[vad_date]["value"] += c_data["value"]
                            dates_to_vals[vad_date]["turnover"] += c_data["turnover"]
                        else:
                            dates_to_vals[vad_date] = {
                                "value": c_data["value"],
                                "turnover": c_data["turnover"]
                        }
                    else:
                        print(f"miss company {iv}")
                        pass
            # print("dates_to_vals: ", dates_to_vals)
            for date, vals in dates_to_vals.items():
                quant_db.insert(
                    "t_basic_industy_daily_kline",                
                    val_obj = {
                        "DATE": date,
                        "SECURITY_NAME": k,
                        "value": vals["value"],
                        "turnover": vals["turnover"],
                        "turnover_rate": (100.* vals["turnover"]) / vals["value"]
                    },
                    dup_key=["DATE"]
                )
            idx += 1
        except Exception as e:
            print(k, e)
            continue

if __name__== "__main__":
    store_industry_quant_data(init=False)
    # store_north_money_to_sector(["2023-09-06"])
    # store_industy_all_valuation(init=True)
    #alter table t_industry_north_money_to_sector add PRIMARY KEY(`INDUSTRY_NAME`, `INTERVAL_TYPE`);
