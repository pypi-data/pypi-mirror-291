import pandas as pd
import time
from openfinance.config import Config
from sqlalchemy.types import VARCHAR
from openfinance.datacenter.database.base import DataBaseManager
from openfinance.datacenter.database.source.eastmoney.trade import index_member
from openfinance.datacenter.database.storage.china.trade import (
    quant_data,
    web_data
)

from openfinance.datacenter.database.source.eastmoney.util import get_previous_date

config = Config()
db = DataBaseManager(Config()).get("quant_db")
# print(db.exec("show databases"))
DATE = get_previous_date(360)
IN_DATE = DATE.replace("-", "")

a = index_member('中证500')
b = index_member('沪深300')
stock_code = pd.concat([a, b], ignore_index=True)
names = {
    "name": "SECURITY_NAME",
    "date": "DATE",
    "code": "SECURITY_CODE"
}
def store_quant_data(init=False):
    idx = 0
    for i in range(len(stock_code)):
        try:
            k = stock_code.iloc[i]['股票名称']
            # k = "五粮液"
            print(k,)
            data = web_data(k, start=IN_DATE)
            data = data.rename(columns=names)
            # print(data)
            time.sleep(0.4)
            db.insert_data_by_pandas(
                data, 
                "t_basic_daily_kline",
                {
                    "SECURITY_NAME": VARCHAR(16),
                    "SECURITY_CODE": VARCHAR(8),
                    "DATE": VARCHAR(32),              
                },
                single=True
                )
            idx += 1
            # break
            #if idx == 3:
            #    break
        except:
            print(stock_code.iloc[i])
            continue
    if init:
        db.execute("alter table t_basic_daily_kline add PRIMARY KEY(`SECURITY_CODE`, `DATE`)")
    else:
        db.execute(f'delete from t_basic_daily_kline where DATE < {DATE}')


def store_market_quant_data(init=False):
    idx = 0
    stocks = ["上证指数", "399300", "399905"]
    for k in stocks:
        try:   
            data = quant_data(k, start=IN_DATE)
            time.sleep(0.4)
            db.insert_data_by_pandas(
                data, 
                "t_market_basic_daily_kline",
                {
                    "SECURITY_NAME": VARCHAR(16),
                    "DATE": VARCHAR(32),              
                },
                single=True
                )
            idx += 1
            #if idx == 3:
            #    break
        except:
            print(k)
            continue
    if init:
        db.execute("alter table t_market_basic_daily_kline add PRIMARY KEY(`SECURITY_NAME`, `DATE`)")
    else:
        db.execute(f'delete from t_market_basic_daily_kline where DATE < {DATE}')

if __name__== "__main__":
    store_quant_data()
    # store_market_quant_data()
    #pass