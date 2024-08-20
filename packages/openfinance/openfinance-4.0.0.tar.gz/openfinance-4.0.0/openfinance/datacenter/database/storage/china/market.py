import time
import requests
import json
import pandas as pd

def market_loan_money(code=""):
    url = "http://query.sse.com.cn/commonSoaQuery.do"
    params = {
        "jsonCallBack": "jsonpCallback80463793",
        "isPagination": "true",
        "tabType": "",
        "pageHelp.pageSize": "100",
        "beginDate": "",
        "endDate": "",
        "sqlId": "RZRQ_HZ_INFO",
        "_": "1699521950794"
    }

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "Connection": "keep-alive",
        "Cookie": "ba17301551dcbaf9_gdp_user_key=; ba17301551dcbaf9_gdp_session_id=9d1865fc-9f7d-46e8-8909-1e5af0de7334; gdp_user_id=gioenc-badg420c%2C88a5%2C5199%2Cccge%2C4d2c8c3b38e9; ba17301551dcbaf9_gdp_session_id_9d1865fc-9f7d-46e8-8909-1e5af0de7334=true; JSESSIONID=E2061DC64EEC838D10AD23C837BFCF17; ba17301551dcbaf9_gdp_sequence_ids={%22globalKey%22:10%2C%22VISIT%22:2%2C%22PAGE%22:4%2C%22VIEW_CLICK%22:6}",
        "Host": "query.sse.com.cn",
        "Referer": "http://www.sse.com.cn/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.content.decode('utf8')[22:-1]
    data = json.loads(data)['pageHelp']['data']
    df = pd.DataFrame(data)
    cols = {
        "rzye": "Financing_Balance",
        "rqylje": "Financing_Purchase_Amount",
        "rqyl": "Margin_Trading_Balance",
        "rzmre": "Margin_Trading_Balance_Amount",
        "rzche": "Margin_Trading_Sell_Quantity",
        "rzrqjyzl": "Total_Financing_and_Margin_Trading_Balance",
        "opDate": "DATE",
        "rqmcl": "rqmcl"
    }
    df=df[list(cols.keys())].rename(columns=cols)
    df['DATE'] = pd.to_datetime(df['DATE'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
    return df

def market_north_money_flow(flag= "北上"):
    """## chinese: 获取外资流入情况|外资流入情况
    ## english: Get foreign money
    ## args: 
        flag: {"沪股通", "深股通", "北上"}
    ## extra:  
        http://data.eastmoney.com/hsgtcg/
    """
    url = "http://push2his.eastmoney.com/api/qt/kamt.kline/get"
    params = {
        "fields1": "f1,f3,f5",
        "fields2": "f51,f52",
        "klt": "101",
        "lmt": "300",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "cb": "jQuery18305732402561585701_1584961751919",
        "_": "1584962164273",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("{") : -2])
    result = {
        "DATE": [],
        "volume": []
    }
    for i in data_json['data']['s2n']:
        d = i.split(",")
        result['DATE'].append(d[0])
        result['volume'].append(d[1])

    df = pd.DataFrame(result)
    return df