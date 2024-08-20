import time
import asyncio

from typing import Any

from openfinance.config import Config
from openfinance.datacenter.database.base import DataBaseManager
from openfinance.datacenter.knowledge.decorator import register
from openfinance.datacenter.database.wrapper import wrapper
from openfinance.datacenter.knowledge.entity_graph.base import EntityGraph, EntityEnum
from openfinance.datacenter.database.source.eastmoney.technical import get_price_volume_status

from openfinance.datacenter.database.source.eastmoney.industry import (
    get_industry_by_company,
    industry_index_trend
)
from openfinance.datacenter.database.source.eastmoney.news import (
    industry_institutional_rating,
    stock_institutional_rating,
    get_company_news
)

ENTITY = EntityGraph()
db = DataBaseManager(Config()).get("db")

@register(name="Volume Analysis", description="Get volume analysis of Company", zh="量价分析")
async def get_volume_analysis(name="贵州茅台", entity_type=EntityEnum.Company.type, **kwargs: Any):
    if ENTITY.is_company(name) and ENTITY.is_company_type(entity_type):
        return get_price_volume_status(name)

@register(name="Forward Price/Earning Ratio", description="Get Forward Price/Earning Ratio of company", zh="远期市盈率")
async def get_forward_pe(name="贵州茅台", entity_type=EntityEnum.Company.type, **kwargs: Any):
    if entity_type == EntityEnum.Company.type and ENTITY.is_company(name):
        try:
            stock_price = db.select_one(
                table = "quantdata.t_basic_daily_kline",
                range_str = "SECURITY_NAME='" + name + "' order by DATE desc limit 1",
                field = "close"              
            )
            eps = db.select_one(
                table = "t_stock_eps_forecast",
                range_str = "SECURITY_NAME='" + name + "'",
                field = "EPS3"
            )
            if len(stock_price) and len(eps) and stock_price["close"] and eps["EPS3"]:
                return f"""Forward Price/Earning is {round(stock_price["close"]/eps["EPS3"], 2)}"""
        except:
            return "No Forward PE found"
    return

@register(name="Industry Analysis", description="Get Industry Trend Analysis", zh="行业趋势")
async def get_industry_analysis(name= "贵州茅台", entity_type=EntityEnum.Company.type, **kwargs: Any):
    # print(name, entity_type)
    if ENTITY.is_company(name) and ENTITY.is_industry_type(entity_type):
        name = ENTITY.get_industry(name)
    if ENTITY.is_industry(name): 
        return wrapper([
            industry_index_trend(name) 
        ])
    return "Industry Analysis"

@register(name="Research Report Analysis", description="Get Research Report Analysis", zh="近期研报分析")
async def get_research_report_analysis(name="", entity_type=EntityEnum.Company.type, **kwargs: Any):
    data = db.get_key_list_column_merge_summary(
        table = "t_eastmoeny_report_content where STOCK_NAME = '" + name + "'", 
        order_str = "DATE",
        limit_num = 3,
        columns_to_names = {
            "RATING": "Research report rating",
            "TITLE": "Research report title",
            "CONTENT_SUMMARY": "Research report summary"
        },
        with_chart=False
    )
    return data

@register(name="Government policies", description="Get Government policies changements", zh="政府监管政策")
@register(name="Recent News", description="Get recent news", zh="公司新闻")
async def get_lastest_news(name=None, entity_type=EntityEnum.Company.type, **kwargs: Any):
    # print(name, entity_type)
    if not name:
        return
    if ENTITY.is_company(name) and ENTITY.is_industry_type(entity_type):
        industry = ENTITY.get_industry(name)
        return get_recent_news(name=industry, entity_type=entity_type)
    elif ENTITY.is_industry(name):
        return get_recent_news(name=name, entity_type=EntityEnum.Industry.type)
    elif ENTITY.is_company_type(entity_type):
        return get_company_news(name)        
    elif ENTITY.is_economy_type(entity_type):
        return get_recent_news(entity_type=entity_type)
    elif ENTITY.is_market_type(entity_type):
        return get_recent_news(entity_type=entity_type)
    return "No Recent News"

def get_gov_stat(name="房地产", entity_type=EntityEnum.Industry.type, **kwargs: Any):
    # "select * from t_news_percept where entity_type='Industry' and entity like '%%房%%' limit 100"
    sql = f"select * from t_gov_stat_hgyd where Datename like '%%{name}%%' limit 20"
    data = db.exec(sql)
    res_str = ""
    for item in data:
        name = item.get('Datename', '')
        res_str += name + ": "
        tmp_dict = dict()
        for key, value in item.items():
            if 'name' not in key:
                tmp_dict[key] = value
        tmp_dict_sort = sorted(tmp_dict.items(), key=lambda x: x[0])
        for info in tmp_dict_sort:
            res_str += 'time: ' + info[0][4:] + ' value: ' + str(info[1]) + ' '
        res_str += '\n'

    return res_str

def get_recent_news(name="", entity_type=""):
    table = f"graph.t_news_percept where entity_type='{entity_type}'"
    if name:
         table += f" and entity like '%{name}%'"
    fields = "indicator, effect, src, TIME"
    order_column = "TIME"
    data = db.select_limit_asc_order(
        table=table,
        order_column = order_column,
        field = fields,
        limit_num = 5
    )
    delta = 3600
    
    result = ""
    if data:
        for d in data:
            unix_ts = int(d["TIME"].timestamp())
            deltahours = (int(time.time()) - unix_ts) // delta
            result += f"""a {d["effect"]} news about {d["src"]} before {deltahours} hours\n"""
    return result