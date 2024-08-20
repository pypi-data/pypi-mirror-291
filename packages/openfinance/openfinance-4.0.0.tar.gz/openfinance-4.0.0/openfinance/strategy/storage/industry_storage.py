import pandas
import time
from openfinance.config import Config
from sqlalchemy.types import VARCHAR
from openfinance.datacenter.database.base import DataBaseManager
from openfinance.strategy.feature.base import FeatureManager
from openfinance.datacenter.knowledge.entity_graph.base import EntityGraph, EntityEnum

from openfinance.datacenter.database.source.eastmoney.util import (
    get_current_date,
    get_previous_date
)

ENTITY = EntityGraph()

DATE = get_current_date()
PRE_DATE = get_previous_date(7)
db = DataBaseManager(Config()).get("quant_db")
# print(db.exec("show databases"))

def init_table():
    db.create_table(
        table = "t_industry_feature_map",
        contents = {
            "SECURITY_NAME": "varchar(16)",
            "SECURITY_CODE": "varchar(16)",        
            "fid": "int",
            "val": "double",
            "fname": "varchar(32)",
            "TIME": "varchar(16)"
        }
    )

    db.exec("alter table t_industry_feature_map add PRIMARY KEY(`SECURITY_NAME`, `TIME`, `fid`)")


def delate_data():
    db.exec(f"delete from t_industry_feature_map where TIME< '{PRE_DATE}'")

def store_industry_features(init=False):
    if init:
        init_table()    

    FeatureManager().name_to_features.clear()
    try:
        import importlib
        import openfinance.strategy.feature.industry as industryimport
        importlib.reload(industryimport)
    except:
        pass
    # for (k, v) in [("Company_RSI_DAY", FeatureManager().get("Company_RSI_DAY"))]:
    for k, v in FeatureManager().stored_features.items():
        # print(k)
        result = v.run(candidates={}).get("result")
        print(result)
        for ind_name, ind_code in ENTITY.industries.items():
            val = result.get(ind_name, 0)
            data = {
                "SECURITY_NAME": ind_name,
                "SECURITY_CODE": ind_code,        
                "fid": v.fid,
                "val": val,
                "fname": v.name,
                "TIME": DATE            
            }
            print("data: ", data)
            db.insert(
                "t_industry_feature_map",
                data,
                dup_key = ["val", "TIME"]
            )
    delate_data()

if __name__== "__main__":
    store_industry_features(init=False)
    #pass