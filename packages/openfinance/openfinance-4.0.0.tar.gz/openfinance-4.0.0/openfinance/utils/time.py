#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Date    ：2022/9/29 20:28 
'''
import re
import time
import datetime

def get_current_year():
    today = datetime.date.today()
    return str(today.year)

def get_current_date():
    today = datetime.date.today()
    return today.strftime("%Y-%m-%d")

def get_previous_date(days=30):
    today = datetime.date.today()
    last_month = today - datetime.timedelta(days=days)
    return last_month.strftime("%Y-%m-%d")

def get_recent_workday(days=0):
    """
    获取最近的工作日
    """
    today = datetime.date.today()
    if days:
        today = today - datetime.timedelta(days=days)
    if today.weekday() == 5:
        return today - datetime.timedelta(days=1)
    elif today.weekday() == 6:
        return today - datetime.timedelta(days=2)
    else:
        return today

def is_workday(days=0):
    """
    获取最近的工作日
    """
    today = datetime.date.today()
    if days:
        today = today - datetime.timedelta(days=days)
    if today.weekday() == 5:
        return 0
    elif today.weekday() == 6:
        return 0
    else:
        return 1