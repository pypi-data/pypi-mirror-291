#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Date    ：2022/9/29 20:27 
'''

import json
import re
import signal
import requests
import pandas as pd
import numpy as np
import multitasking

from tqdm import tqdm

from jsonpath import jsonpath
from datetime import datetime, timedelta

from openfinance.datacenter.database.source.eastmoney.util import (
    request_header, 
    session, 
    market_num_dict,
    get_code_id, 
    trans_num, 
    trade_detail_dict, 
    latest_report_date,
    market_dict,
    latest_trade_date    
)


# 获取股票、债券、期货、基金历史K线数据
def quant_data(code, start='19000101', end=None, freq='d', fqt=1):
    """
    获取股票、指数、债券、期货、基金等历史K线行情
    code: 可以是股票或指数（包括美股港股等）代码或简称
    start、end: 起始和结束日期，年月日
    freq: 时间频率，默认日, 60 : 60 分钟；101或'D'或'd'：日；102或‘w’或'W'：周; 103或'm'或'M': 月
    fqt: 复权类型，0：不复权，1：前复权；2：后复权，默认前复权
    """
    standard = {
        "open": [],
        "close": [],
        "high": [],
        "low": [],
        "volume": []
    }
    try:
        if end in [None,'']:
            end=latest_trade_date()
        start = ''.join(start.split('-'))
        end = ''.join(end.split('-'))

        if type(freq) == str:
            freq = freq.lower()
            if freq == 'd':
                freq = 101
            elif freq == 'w':
                freq = 102
            elif freq == 'm':
                freq = 103
            else:
                print('时间频率输入有误')
        
        code_id = get_code_id(code)

        kline_field = {
            'f51': 'DATE',
            'f52': 'open',
            'f53': 'close',
            'f54': 'high',
            'f55': 'low',
            'f57': 'volume',
        }

        fields = list(kline_field.keys())
        columns = list(kline_field.values())

        fields2 = ",".join(fields)

        params = (
            ('fields1', 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13'),
            ('fields2', fields2),
            ('beg', start),
            ('end', end),
            ('rtntype', '6'),
            ('secid', code_id),
            ('klt', f'{freq}'),
            ('fqt', f'{fqt}'),
        )

        url = 'https://push2his.eastmoney.com/api/qt/stock/kline/get'
        # 多线程装饰器
        json_response = session.get(
            url, headers=request_header, params=params).json()
        
        klines = jsonpath(json_response, '$..klines[:]')

        # date = []
        # for line in json_response["data"]["klines"]:
        #     tmp = line.split(",")
        #     #print(tmp)
        #     standard["open"].append(tmp[1])
        #     standard["close"].append(tmp[2])
        #     standard["high"].append(tmp[3])
        #     standard["low"].append(tmp[4])
        #     standard["volume"].append(tmp[5])
        #     date.append(tmp[0])

        if not klines:
            columns.insert(0, 'SECURITY_CODE')
            columns.insert(0, 'SECURITY_NAME')
            return pd.DataFrame(columns=columns)

        rows = [k.split(',') for k in klines]
        name = json_response['data']['name']
        code = code_id.split('.')[-1]
        df = pd.DataFrame(rows, columns=columns)

        df.insert(0, 'SECURITY_CODE', code)
        df.insert(0, 'SECURITY_NAME', name)
        ignore_cols = ['SECURITY_NAME', 'SECURITY_CODE', 'DATE']
        df = trans_num(df, ignore_cols)
        return df
    except Exception as e:
        print (e)
        # result = {k: np.asarray(v, dtype='double') for k, v in standard.items()}
        # result["date"] = date
        # return result


# 获取股票、债券、期货、基金历史K线数据
def web_data(code, start='19000101', end=None, freq='d', fqt=1):
    """
    获取股票、指数、债券、期货、基金等历史K线行情
    code可以是股票或指数（包括美股港股等）代码或简称
    start和end为起始和结束日期，年月日
    freq:时间频率，默认日，1 : 分钟；5 : 5 分钟；15 : 15 分钟；30 : 30 分钟；
    60 : 60 分钟；101或'D'或'd'：日；102或‘w’或'W'：周; 103或'm'或'M': 月
    注意1分钟只能获取最近5个交易日一分钟数据
    fqt:复权类型，0：不复权，1：前复权；2：后复权，默认前复权
    """
    if end in [None,'']:
        end=latest_trade_date()
    if freq == 1:
        return get_1min_data(code)
    start = ''.join(start.split('-'))
    end = ''.join(end.split('-'))
    if type(freq) == str:
        freq = freq.lower()
        if freq == 'd':
            freq = 101
        elif freq == 'w':
            freq = 102
        elif freq == 'm':
            freq = 103
        else:
            print('时间频率输入有误')
    kline_field = {
        'f51': '日期',
        'f52': '开盘',
        'f53': '收盘',
        'f54': '最高',
        'f55': '最低',
        'f56': '成交量',
        'f57': '成交额',
        'f58': '振幅',
        'f59': '涨跌幅',
        'f60': '涨跌额',
        'f61': '换手率'}
    fields = list(kline_field.keys())
    columns = list(kline_field.values())
    cols1 = ['日期', '名称', '代码', '开盘', '最高', '最低', '收盘', '成交量', '成交额', '换手率']
    cols2 = ['date', 'name', 'code', 'open', 'high', 'low', 'close', 'volume', 'turnover', 'turnover_rate']
    fields2 = ",".join(fields)
    code_id = get_code_id(code)
    params = (
        ('fields1', 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13'),
        ('fields2', fields2),
        ('beg', start),
        ('end', end),
        ('rtntype', '6'),
        ('secid', code_id),
        ('klt', f'{freq}'),
        ('fqt', f'{fqt}'),
    )

    url = 'https://push2his.eastmoney.com/api/qt/stock/kline/get'
    # 多线程装饰器

    json_response = session.get(
        url, headers=request_header, params=params).json()
    klines = jsonpath(json_response, '$..klines[:]')
    if not klines:
        columns.insert(0, '代码')
        columns.insert(0, '名称')
        return pd.DataFrame(columns=cols2)

    rows = [k.split(',') for k in klines]
    name = json_response['data']['name']
    code = code_id.split('.')[-1]
    df = pd.DataFrame(rows, columns=columns)

    df.insert(0, '代码', code)
    df.insert(0, '名称', name)

    df = df.rename(columns=dict(zip(cols1, cols2)))
    # print(df)
    # df.index = pd.to_datetime(df['date'])
    # df = df[cols2[1:]]
    df = df[cols2]
    df['name'] = df['name'].str.replace('XD', '', regex=False)
    df['name'] = df['name'].str.replace('XR', '', regex=False)
    df['name'] = df['name'].str.replace('DR', '', regex=False)
    df['name'] = df['name'].str.replace('-', '', regex=False)
    df['name'] = df['name'].str.replace('W', '', regex=False)
    df['name'] = df['name'].str.replace('D', '', regex=False)
    df['name'] = df['name'].str.replace('U', '', regex=False)
    df['name'] = df['name'].str.replace(' ', '', regex=False)              
    # print(df)    
    # 将object类型转为数值型
    ignore_cols = ['name', 'code', 'date']
    df = trans_num(df, ignore_cols)
    return df

# 获取单只或多只证券（股票、基金、债券、期货)的收盘价格dataframe
def get_price(code_list, start='19000101', end=None, freq='d', fqt=1):
    '''code_list输入股票list列表
    如code_list=['中国平安','贵州茅台','工业富联']
    '''
    if isinstance(code_list, str):
        code_list = [code_list]
    
    if end is None:
        end=latest_trade_date()

    @multitasking.task
    def run(code):
        try:
            temp = web_data(code, start, end, freq, fqt)
            temp[temp.name[0]]=temp.close
            data_list.append(temp[temp.name[0]])
        except:
            pass

    data_list = []
    for code in tqdm(code_list):
        try:
            run(code)
        except:
            continue
    multitasking.wait_for_tasks()
    # 转换为dataframe
    df = pd.concat(data_list, axis=1)
    return df

# 获取单只或多只证券（股票、基金、债券、期货)的历史K线数据
def get_data(code_list, start='19000101', end=None, freq='d', fqt=1):
    '''code_list输入股票list列表
    如code_list=['中国平安','贵州茅台','工业富联']
    返回多只股票多期时间的面板数据
    '''
    if isinstance(code_list, str):
        code_list = [code_list]
    if end is None:
        end=latest_trade_date()

    data_list = []

    @multitasking.task
    def run(code):
        data = web_data(code, start, end, freq, fqt)
        data_list.append(data)

    for code in tqdm(code_list):
        run(code)
    multitasking.wait_for_tasks()
    # 转换为dataframe
    df = pd.concat(data_list, axis=0)
    return df