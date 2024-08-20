import pandas as pd
import traceback
import time, datetime
from openfinance.config import Config
from sqlalchemy.types import VARCHAR
from openfinance.datacenter.database.base import DataBaseManager
from openfinance.strategy.feature.base import FeatureManager
from openfinance.datacenter.database.source.eastmoney.trade import index_member
from openfinance.datacenter.database.source.eastmoney.util import (
    get_current_date,
    get_previous_date
)

a = index_member('中证500')
b = index_member('沪深300')
stock_code = pd.concat([a, b], ignore_index=True)

DATE = get_current_date()
PRE_DATE = get_previous_date(7)
db = DataBaseManager(Config()).get("quant_db")
# print(db.exec("show databases"))

def init_table():
    db.create_table(
        table = "t_stock_feature_map",
        contents = {
            "SECURITY_NAME": "varchar(16)",
            "SECURITY_CODE": "varchar(16)",        
            "fid": "int",
            "val": "double",
            "fname": "varchar(32)",
            "TIME": "varchar(16)"
        }
    )
    db.exec("alter table t_stock_feature_map add PRIMARY KEY(`SECURITY_CODE`, `fid`)")


def delate_data(
    fname,
    keep_latest=False
):
    # print(fname)
    dates = db.select_more(
        "t_stock_feature_map", range_str=f"fname='{fname}' order by TIME desc limit 2", field='distinct TIME'
    )
    # print(dates)
    if len(dates) == 2:
        date0 = datetime.datetime.strptime(dates[0]["TIME"], "%Y-%m-%d")
        date1 = datetime.datetime.strptime(dates[1]["TIME"], "%Y-%m-%d")
        deltadays = abs((date1-date0).days)
        if deltadays == 1:
            if keep_latest:
                db.exec(f"delete from t_stock_feature_map where fname='{fname}' and TIME< '{date0}'")
            else:
                db.exec(f"delete from t_stock_feature_map where fname='{fname}' and TIME< '{PRE_DATE}'")

def store_company_features(init=False):
    if init:
        init_table()    
    code_list = stock_code['股票代码'].tolist()
    name_list = stock_code['股票名称'].tolist()

    # code_list = ["600519"]
    # name_list = ["贵州茅台"]

    FeatureManager().name_to_features.clear()
    try:
        import importlib
        import openfinance.strategy.feature.company as companyimport
        importlib.reload(companyimport)
        print(FeatureManager().name_to_features)
    except:
        pass

    for k, v in FeatureManager().stored_features.items():
        print(k)
    # if True:
    #     k = "DividentSpeed"
    #     v = FeatureManager().stored_features[k]

        keep_latest = v.operator.get("latest", False)
        try:
            result = v.run(candidates=name_list)
            # print(f"{k} result: ", result)
            TIMEKEY = v.source.get("key", "TIME")
            ftime = result.get(TIMEKEY, {})
            fresult = result.get("result")
            for i in range(len(name_list)):
                SECURITY_NAME = name_list[i]
                # if empty value then pass it
                if SECURITY_NAME not in fresult:
                    continue
                dict_val = fresult.get(SECURITY_NAME, 0) # childmode is dict
                t = ftime.get(SECURITY_NAME, [DATE])[-1] 
                try:
                    if len(v.childrens):                       
                        for child in v.childrens:
                            val = dict_val[child["indicator"]]
                            data = {
                                "SECURITY_NAME": SECURITY_NAME,
                                "SECURITY_CODE": code_list[i],        
                                "fid": child["id"],
                                "val": val,
                                "fname": child["name"],
                                "TIME": t
                            }
                            db.insert(
                                "t_stock_feature_map",
                                data,
                                dup_key = ["val", "TIME"]
                            )
                    else:
                        data = {
                            "SECURITY_NAME": SECURITY_NAME,
                            "SECURITY_CODE": code_list[i],        
                            "fid": v.fid,
                            "val": dict_val,
                            "fname": v.name,
                            "TIME": t
                        }
                        db.insert(
                            "t_stock_feature_map",
                            data,
                            dup_key = ["val", "TIME"]
                        )
                except Exception as e:
                    print(k, e)
                    traceback.print_exc()  
                    traceback_str = traceback.format_exc()  
                    print("堆栈跟踪字符串:\n", traceback_str)                    
                
                # if len(v.childrens):
                #     for child in v.childrens:
                #         # delate_data(child["name"], keep_latest)
                #         pass
                # else:
                #     # delate_data(k, keep_latest)
                #     pass

        except Exception as e:
            print(k, e)
            traceback.print_exc()  
            traceback_str = traceback.format_exc()  
            print("堆栈跟踪字符串:\n", traceback_str)            

if __name__== "__main__":
    store_company_features(init=False)
    #pass