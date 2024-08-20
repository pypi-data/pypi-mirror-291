# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 13:53:48 2022

"""
import pandas as pd
import requests
import json
from typing import Any
from datetime import datetime
from jsonpath import jsonpath
from tqdm import tqdm
from bs4 import BeautifulSoup
from openfinance.datacenter.database.base import EMPTY_DATA
from openfinance.datacenter.database.source.eastmoney.industry import (
    get_industry_by_company
)
from openfinance.datacenter.database.source.eastmoney.util import (
    trans_num,
    get_code_id,
    get_current_date,
    get_previous_date,
    get_recent_workday,
    report_summary
)
from openfinance.config import Config
from openfinance.agentflow.llm.manager import ModelManager
from openfinance.datacenter.database.base import DataBaseManager

config = Config()
model_manager = ModelManager(config=config)
llm = model_manager.get_model("chatgpt")

db = DataBaseManager(Config()).get("db")

def industry_institutional_rating(code):
    """## chinese: 获取行业的机构评级|行业评级
    ## english: Get institutional rating of industry|industry institutional rating
    ## args:
        code: 股票名称
    ## http://reportapi.eastmoney.com/report/list?cb=callback7187406&beginTime=2021-06-18&endTime=2023-06-18&pageNo=1&pageSize=5&qType=1&industryCode=1029&fields=orgCode%2CorgSName%2CemRatingName%2CencodeUrl%2Ctitle%2CpublishDate&_=1687091682364
    """
    try:
        code = code.strip()
        url = "http://reportapi.eastmoney.com/report/list"
        params = {
            "beginTime": get_previous_date(30),
            "endTime": get_current_date(),
            "pageNo": 1,
            "qType": 1,
            "pageSize": 2,
            "industryCode": code,
            "fields": "orgSName,emRatingName,title",
            "_": 1687091239523,
        }
        res = requests.get(url, params=params)
        #print(res.text, code_id, get_previous_date(30), get_current_date())
        result = ""
        res = json.loads(res.text)
        art_list = res['data']
        for i in art_list:
            result += i["orgSName"] + " " + i["emRatingName"] + " " + i["title"] + "\n"
        return result
    except:
        return EMPTY_DATA

# need to improve for single company
def stock_institutional_rating(code, **kwargs: Any):
    """## chinese: 获取公司的机构评级|机构评级
    ## english: get institutional rating of company|company institutional rating
    ## args:
        code: 股票名称
    ## 
    """
    try:
        code = code.strip()
        code_id = get_code_id(code)[2:]
        url = "http://reportapi.eastmoney.com/report/list"
        params = {
            "beginTime": get_previous_date(30),
            "endTime": get_current_date(),
            "pageNo": 1,
            "qType": 1,
            "pageSize": 2,
            "code": code_id,
            "fields": "orgSName,emRatingName,title",
            "_": 1687091239523,
        }
        res = requests.get(url, params=params)
        #print(res.text, code_id, get_previous_date(30), get_current_date())
        result = ""
        res = json.loads(res.text)
        art_list = res['data']
        if len(art_list):
            for i in art_list:
                result += i["orgSName"] + " " + i["emRatingName"] + " " + i["title"] + "\n"
        else:
            industryCode = get_industry_by_company(code)
            return industry_institutional_rating(industryCode)
        return result
    except:
        return EMPTY_DATA

def get_company_news(name):
    try:
        name = name.strip()
        code_id = get_code_id(name)
        url = "http://np-listapi.eastmoney.com/comm/web/getListInfo"
        params = {
            "cfh": 1,
            "client": "web",
            "mTypeAndCode": code_id,
            "type": 1,
            "pageSize": 5,
            "traceId": 479298450,
            "_": 1687091239523
        }
        res = requests.get(url, params=params)
        # print(res.text)
        result = ""
        res = json.loads(res.text)
        if res['message'] == "success":
            art_list = res['data']['list']
            print(art_list)
            for i in art_list:
                result += i["Art_Title"] + "\n"
        return result
    except:
        return EMPTY_DATA 

def eastmoney_report_crawler(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    # title = soup.select(".title")[0].text.strip()
    content = soup.select(".ctx-content")[0].text.strip()
    pdf_link = soup.select(".pdf-link")[0]["href"]
    return content, pdf_link


def get_eastmoney_report(pageNo, qType, pageSize=100):
    '''
    https://reportapi.eastmoney.com/report/list?cb=datatable6176985&pageSize=50&beginTime=2024-01-01&endTime=2024-01-27&pageNo=1&fields=&qType=0&orgCode=&author=&_=1625747785207
    '''
    '''
    https://reportapi.eastmoney.com/report/list?cb=callback7187406&beginTime=2024-01-01&endTime=2024-01-27&pageNo=1&pageSize=5&qType=1&industryCode=&fields=orgCode%2CorgSName%2CemRatingName%2CencodeUrl%2Ctitle%2CpublishDate&_=1687091682364
    '''

    http_url_prefix = "https://data.eastmoney.com/report/zw_macresearch.jshtml?encodeUrl="

    url = "http://reportapi.eastmoney.com/report/list"
    params = {
        # "beginTime": get_previous_date(30),
        "beginTime": get_previous_date(1),
        "endTime": get_previous_date(1),
        "pageNo": pageNo,
        "qType": qType, ## 0: 公司报告 1: 行业报告
        "pageSize": pageSize,  # max=100 every page
        "code": "",
        "fields": "",
        "_": 1625747785207,
    }
    # try:
    res = requests.get(url, params=params)
    res = json.loads(res.text)
    # 获取当前日期已经存在数据库的key
    sql = "select * from t_eastmoeny_report_content"
    sql_data = db.exec(sql)
    cur_data = list()
    for item in sql_data:
        if item.get("DATE") == get_previous_date(1):
            cur_data.append([item.get("STOCK_NAME"), item.get("STOCK_CODE"), item.get("DATE")])

    result = list()
    for item in res.get('data'):
        encode_url = item.get('encodeUrl')
        stock_name = item.get('stockName') if item.get('stockName') != "" else item.get('industryName')
        stock_code = item.get('stockCode') if item.get('stockCode') != "" else item.get('industryCode')
        rating = item.get('emRatingName')
        title = item.get('title')
        pub_date = item.get('publishDate')
        pub_date = pub_date[:10]
        http_url = http_url_prefix + encode_url
        # 存在则跳过
        if [stock_name, stock_code, pub_date] in cur_data:
            print(f"crawler data exist: {stock_name} {stock_code} {pub_date}")
            continue
        try:
            content, pdf_link = eastmoney_report_crawler(http_url)
            content_summary = report_summary(content, llm)
            content_summary = content_summary.content
        except exception as e:
            print("crawler error: ", e)
            # summaty调用出错直接返回现有数据
            return pd.DataFrame(result, columns=["STOCK_CODE", "STOCK_NAME", "RATING", "TITLE", "CONTENT", "CONTENT_SUMMARY", "PDF_LINK", "DATE", "QTYPE"])
        # print(f"stock_code: {stock_code}\nstock_name: {stock_name}\nrating: {rating}\ntitle: {title}\ncontent: {content}\npdf_link: {pdf_link}\n")
        result.append([stock_code, stock_name, rating, title, content, content_summary, pdf_link, pub_date, qType])
    return pd.DataFrame(result, columns=["STOCK_CODE", "STOCK_NAME", "RATING", "TITLE", "CONTENT", "CONTENT_SUMMARY", "PDF_LINK", "DATE", "QTYPE"])

def stock_news_em(name: str = "贵州茅台") -> pd.DataFrame:
    """
    东方财富-个股新闻-最近 10 条新闻
    https://so.eastmoney.com/news/s?keyword=%E4%B8%AD%E5%9B%BD%E4%BA%BA%E5%AF%BF&pageindex=1&searchrange=8192&sortfiled=4
    :param symbol: 股票代码
    :type symbol: str
    :return: 个股新闻
    :rtype: pandas.DataFrame
    """
    url = "http://search-api-web.eastmoney.com/search/jsonp"

    symbol = get_code_id(name)[2:]
    # print("symbol: ", symbol)
    params = {
        "cb": "jQuery3510875346244069884_1668256937995",
        "param": '{"uid":"",'
        + f'"keyword":"{symbol}"'
        + ',"type":["cmsArticleWebOld"],"client":"web","clientType":"web","clientVersion":"curr",'
        '"param":{"cmsArticleWebOld":{"searchScope":"default","sort":"default","pageIndex":1,'
        '"pageSize":10,"preTag":"<em>","postTag":"</em>"}}}',
        "_": "1668256937996",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    # print("data_text: ", data_text)
    data_json = json.loads(
        data_text.strip("jQuery3510875346244069884_1668256937995(")[:-1]
    )
    return data_json
    # temp_df = pd.DataFrame(data_json["result"]["cmsArticleWebOld"])
    # temp_df.rename(
    #     columns={
    #         "date": "发布时间",
    #         "mediaName": "文章来源",
    #         "code": "-",
    #         "title": "新闻标题",
    #         "content": "新闻内容",
    #         "url": "新闻链接",
    #         "image": "-",
    #     },
    #     inplace=True,
    # )
    # temp_df["关键词"] = symbol
    # temp_df = temp_df[
    #     [
    #         "关键词",
    #         "新闻标题",
    #         "新闻内容",
    #         "发布时间",
    #         "文章来源",
    #         "新闻链接",
    #     ]
    # ]
    # temp_df["新闻标题"] = (
    #     temp_df["新闻标题"]
    #     .str.replace(r"\(<em>", "", regex=True)
    #     .str.replace(r"</em>\)", "", regex=True)
    # )
    # temp_df["新闻标题"] = (
    #     temp_df["新闻标题"]
    #     .str.replace(r"<em>", "", regex=True)
    #     .str.replace(r"</em>", "", regex=True)
    # )
    # temp_df["新闻内容"] = (
    #     temp_df["新闻内容"]
    #     .str.replace(r"\(<em>", "", regex=True)
    #     .str.replace(r"</em>\)", "", regex=True)
    # )
    # temp_df["新闻内容"] = (
    #     temp_df["新闻内容"]
    #     .str.replace(r"<em>", "", regex=True)
    #     .str.replace(r"</em>", "", regex=True)
    # )
    # temp_df["新闻内容"] = temp_df["新闻内容"].str.replace(r"\u3000", "", regex=True)
    # temp_df["新闻内容"] = temp_df["新闻内容"].str.replace(r"\r\n", " ", regex=True)
    # return temp_df

if __name__ == "__main__":
    res_df = get_eastmoney_report(1, 1, 100)
    print(res_df.count())
