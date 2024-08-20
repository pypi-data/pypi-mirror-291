import pandas
import time
from openfinance.config import Config
from sqlalchemy.types import VARCHAR
from openfinance.datacenter.database.base import DataBaseManager

from openfinance.datacenter.database.source.eastmoney.news import get_eastmoney_report

db = DataBaseManager(Config()).get("db")

def store_eastmoney_report():
    # 存储前一日的行业报告和公司报告
    try:
        # 1 行业报告
        data_df = get_eastmoney_report(1, 1, 100)
        print(data_df.head())
        print(data_df.count())
        time.sleep(0.5)
        if not data_df.empty:
            db.insert_data_by_pandas(
                data_df, 
                "t_eastmoeny_report_content",
                {
                    "STOCK_CODE": VARCHAR(16),
                    "STOCK_NAME": VARCHAR(16),
                    "DATE": VARCHAR(32),
                },
                #single=True                
                )

        # 0 公司报告
        data_df = get_eastmoney_report(1, 0, 100)
        print(data_df.head())
        print(data_df.count())
        time.sleep(0.5)
        if not data_df.empty:
            db.insert_data_by_pandas(
                data_df, 
                "t_eastmoeny_report_content",
                {
                    "STOCK_CODE": VARCHAR(16),
                    "STOCK_NAME": VARCHAR(16),
                    "DATE": VARCHAR(32),
                },
                #single=True                
                )
    except:
        print("error in store_eastmoney_report")

if __name__== "__main__":
    store_eastmoney_report()