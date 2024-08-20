#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import (Dict, Any)

import math
import asyncio
import aiomysql
import pymysql
import pandas as pd
import pymysql.cursors

from collections import deque

from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.types import NVARCHAR, Float, Integer
from dbutils.pooled_db import PooledDB

from openfinance.config import Config
from openfinance.config.macro import MLOG
from openfinance.utils.singleton import Singleton
from openfinance.utils.string_tools.util import (
    is_chinese,
    num_to_string
)

EMPTY_DATA = " "
EMPTY_NUM = -1000000

class Database:
    """ Python连接到 MySQL 数据库及相关操作 """

    connected = False
    engine = None
    pool = None
    # 构造函数，初始化时直接连接数据库

    def __init__(self, conf):
        if type(conf) is not dict:
            print('错误: 参数不是字典类型！')
        else:
            for key in ['host', 'port', 'user', 'pw', 'db']:
                if key not in conf.keys():
                    print('错误: 参数字典缺少 %s' % key)
            if 'charset' not in conf.keys():
                conf['charset'] = 'utf8'
        try:
            self.pool = PooledDB(
                creator=pymysql,
                maxconnections=6,
                mincached=2,
                maxcached=5,
                maxshared=3,
                blocking=True,
                maxusage=None,
                setsession=['SET AUTOCOMMIT = 1'],
                ping=0,
                host=conf['host'],
                port=conf['port'],
                user=conf['user'],
                passwd=conf['pw'],
                db=conf['db'],
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor
            )
            self.connected = True
            self.engine = create_engine(
                "mysql+pymysql://%(user)s:%(pw)s@%(host)s:%(port)d/%(db)s?charset=utf8" % conf
            )
        except pymysql.Error as e:
            print('数据库连接失败:', end='')

    def create_table(self, table, contents):
        with self.pool.connection() as conn:
            try:
                # 使用execute()方法执行sql，如果表存在则删除
                with conn.cursor() as cursor:
                    cursor.execute('drop table if EXISTS ' + table)
                # 创建表的sql
                    if isinstance(contents, dict):
                        new_contents = ""
                        for k, v in contents.items():
                            new_contents += "\n" + k + " " + v + ","
                        contents = new_contents[:-1]  # delete last ","
                    sql = '''create table ''' + table + '''\n(''' + contents + '''\n)'''
                    print(sql)
                    cursor.execute(sql)
            except pymysql.Error as e:
                print(e)
                conn.rollback()
                return False

    def add_column_to_table(self, table, contents):
        with self.pool.connection() as conn:
            try:
                with conn.cursor() as cursor:
                    if isinstance(contents, dict):
                        new_contents = ""
                        for k, v in contents.items():
                            new_contents += k + " " + v + ","
                        contents = new_contents[:-1]  # delete last ","
                    sql = '''ALTER TABLE ''' + table + ''' ADD ''' + contents
                    print(sql)
                    cursor.execute(sql)
            except pymysql.Error as e:
                conn.rollback()
                return False

    # 插入数据到数据表
    def insert(self, table, val_obj, dup_key=None):
        sql_top = 'INSERT INTO ' + table + ' ('
        sql_tail = ') VALUES ('
        with self.pool.connection() as conn:
            try:
                for key, val in val_obj.items():
                    sql_top += key + ','
                    if isinstance(val, str):
                        val = "\'" + val + "\'"
                    else:
                        val = str(val)
                    sql_tail += val + ','
                sql = sql_top[:-1] + sql_tail[:-1] + ')'
                #print(sql)
                if dup_key:
                    sql += " ON DUPLICATE KEY UPDATE "
                    for key in dup_key:
                        val = val_obj[key]
                        if isinstance(val, str):
                            val = "\"" + val + "\""
                        else:
                            val = str(val)                      
                        sql += key + "=" + val + ","
                    sql = sql[:-1]
                MLOG.debug(f"sql: {sql}")
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                conn.commit()
                #return conn.insert_id()
                return True
            except pymysql.Error as e:
                MLOG.error(e)
                conn.rollback()
                return False

    # 插入数据到数据表
    def execute(self, sql):
        with self.pool.connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                conn.commit()
                return True
            except pymysql.Error as e:
                conn.rollback()
                return False

    # 更新数据到数据表
    def update(self, table, val_obj, range_str):
        with self.pool.connection() as conn:
            sql = 'UPDATE ' + table + ' SET '
            try:
                for key, val in val_obj.items():
                    if isinstance(val, str):
                        val = "\"" + val + "\""
                    sql += key + '=' + val + ','
                sql = sql[:-1] + ' WHERE ' + range_str
                #print(sql)
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                conn.commit()
                return cursor.rowcount
            except pymysql.Error as e:
                conn.rollback()
                return False

    # 删除数据在数据表中
    def delete(self, table, range_str):
        with self.pool.connection() as conn:
            sql = 'DELETE FROM ' + table + ' WHERE ' + range_str
            try:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                conn.commit()
                return cursor.rowcount
            except pymysql.Error as e:
                conn.rollback()
                return False

    # 查询唯一数据在数据表中
    def select_one(self, table, range_str, field='*'):
        with self.pool.connection() as conn:
            sql = 'SELECT ' + field + ' FROM ' + table + ' WHERE ' + range_str
            print("Sql: ", sql)
            try:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                conn.commit()
                return cursor.fetchall()[0]
            except pymysql.Error as e:
                return False

    # 查询多条数据在数据表中
    def select_more(self, table, range_str="", field='*'):
        with self.pool.connection() as conn:
            if range_str:
                sql = 'SELECT ' + field + ' FROM ' + table + ' WHERE ' + range_str
            else:
                sql = 'SELECT ' + field + ' FROM ' + table 
            # print(sql)
            try:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                conn.commit()
                return cursor.fetchall()
            except pymysql.Error as e:
                return False

    # 查询条件筛选查询
    def select_limit_asc_order(self, table, order_column, limit_num=4, field='*'):
        """ Get latest list in desc order"""
        with self.pool.connection() as conn:
            sql = 'SELECT ' + field + ' FROM ' + table + \
                        ' order by ' + order_column + \
                ' desc limit ' + str(limit_num)
            try:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                conn.commit()
                data = cursor.fetchall()
                if data:
                    return data.reverse()
                else:
                    return data
            except pymysql.Error as e:
                print(e)
                return False

    # 直接执行
    def exec(self, sql):
        with self.pool.connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                conn.commit()
                return cursor.fetchall()
            except pymysql.Error as e:
                print(e)
                return False

    def insert_data_by_pandas(
        self,
        dataframe,
        table_name,
        dtypes={},
        if_exists='append',
        single=False
    ):
        """通过dataframe 向 sql 中插入表，此方法缺点是若表已存在，不能替换表中部分重复数据，只能替换/追加整张表
        
        Args:
            dataframe: pd.Dataframe类型
            table_name: 插入的表名
            if_exists: {'fail', 'replace', 'append'}, default 'fail'
                - fail: If table exists, do nothing.
                - replace: If table exists, drop it, recreate it, and insert data.
                - append: If table exists, insert data. Create if does not exist.
        Returns:
        """
        def create_upsert_method(primary_key_column):
            def method(table, conn, keys, data_iter):
                # Create the INSERT statement with named placeholders
                insert = f"INSERT INTO {table.name} ({','.join(keys)})"
                try:
                    for d in data_iter:
                        values = " VALUES("
                        update = " ON DUPLICATE KEY UPDATE "
                        for i, name in enumerate(keys):
                            new_val = "NULL,"
                            if d[i]:
                                new_val = "'" + str(d[i]) + "',"
                            values += new_val
                            if name not in primary_key_column:
                                update += name + "=" + new_val

                        values = values[:-1] + ")"
                        sql = insert + values + update[:-1]
                        # print(sql)
                        conn.execute(text(sql))
                except Exception as e:
                    print("An error occurred:", str(e))
            return method

        if single:
            for i in range(len(dataframe)):
                try:
                    dataframe.iloc[i:i+1].to_sql(
                        table_name,
                        self.engine,
                        if_exists=if_exists,
                        index=False,
                        chunksize=100,
                        dtype=dtypes,
                        method=create_upsert_method(list(dtypes.keys()))
                    )
                except Exception as e:
                    print(e)
                    pass
        else:
            try:
                dataframe.to_sql(
                    table_name,
                    self.engine,
                    if_exists=if_exists,
                    index=False,
                    chunksize=100,
                    dtype=dtypes,
                    method=create_upsert_method(list(dtypes.keys()))
                )
            except Exception as e:
                print(e)
                pass

    # 查询多条数据在数据表中
    def get_key_list_column_merge_summary(
        self,
        table,
        order_str,
        limit_num=5,
        columns_to_names=None,
        latest={},   
        with_chart=False,
        with_text=True,
        key_prefix="Sequential ",
        key_postfix= "",
        **kwargs
    ):
        """
        Args:
            table: 原始table
            order_str: 排序的key
            limit_num=5: 图表展示多少数据
            columns_to_names=None: 查询哪些字段出来
            latest={"key": "DATE", "order":1}: 是否查询最近,传入模型排序key名称比如DATE
            with_chart=False: 是否展示图标
            key_prefix=" in sequencial order: ": 文案前缀
            key_postfix= "": 文案后缀
        """

        # 构造fields查询
        if columns_to_names is None:
            fields = "*"
        else:
            fields = ", ".join(k for k, v in columns_to_names.items())

        if order_str not in fields:
            fields += ", " + order_str

        # 构造判断是否最近数据   
        # print("latest: ", latest, "table: ", table)     
        if latest:
            latest_order = latest.get("order", 1)
            latest_key = latest.get("key")    
            date = self.select_limit_asc_order(
                table = table,
                order_column = latest_key,
                limit_num = latest_order,
                field = latest_key
            )
            if len(date) >= latest_order:
                date = date[latest_order-1][latest_key]
                if "where" in table:
                    table = table + " and " + latest_key + "='" + date + "'"
                else:
                    table = table + " where " + latest_key + "='" + date + "'"
            else:
                return

        # 按照order_str排序，查询数据
        data = self.select_limit_asc_order(
            table=table,
            order_column=order_str,
            limit_num=limit_num,
            field=fields
        )
        if data:
            if with_text:
                idx = 0
                # 构造文本输出
                for line in data:
                    for k, v in line.items():
                        if k in columns_to_names:
                            if k == order_str:
                                columns_to_names[k] = columns_to_names[k] + ", "
                                continue # remove Time Order in String
                            if 0 == idx:
                                columns_to_names[k] = key_prefix + columns_to_names[k] + ": "
                            try:
                                columns_to_names[k] += num_to_string(v) + ", "
                            except:
                                columns_to_names[k] += str(v) + ", "
                    idx += 1
                result = ""
                if fields == "*":
                    result = "\n".join(k + " : " + v for k, v in columns_to_names.items())
                    # error here, to improve later
                else:
                    result = "\n".join(v[:-2] + key_postfix for k, v in columns_to_names.items())
            
            # 返回图表数据
            if with_chart and with_text:
                return {
                    "result": result,
                    "chart": data
                }
            elif with_chart:
                return {
                    "chart": data
                }
            else:
                return result
        else:
            return EMPTY_DATA

    # 直接执行sql查询多条数据在数据表中
    def exec_by_modelformat(
        self,
        sql,
        columns_to_names
    ):
        data = self.exec(sql)
        if not data:
            return EMPTY_DATA
        # print(data, columns_to_names)
        hit_columns = dict()
        idx = 0
        for line in data:
            for k, v in line.items():
                if k in columns_to_names:
                    if 0 == idx:
                        hit_columns[k] = "Progressive " + \
                            columns_to_names[k] + ":"
                    try:
                        hit_columns[k] += num_to_string(v) + ", "
                    except:
                        hit_columns[k] += str(v) + ", "
                elif is_chinese(k):
                    if 0 == idx:
                        hit_columns[k] = "Progressive " + k + ":"
                    try:
                        hit_columns[k] += num_to_string(v) + ", "
                    except:
                        hit_columns[k] += str(v) + ", "
            idx += 1
        if len(hit_columns) == 0:
            return EMPTY_DATA
        result = " \n".join(v[:-2] for k, v in hit_columns.items())
        return result

class AsyncDB:
    pool = None
    connected = False

    def __init__(
        self,
        conf
    ):
        self.conf = conf

    async def init_pool(
        self
    ):
        self.pool = await aiomysql.create_pool(
            host = self.conf.get("host", "localhost"), 
            port = self.conf.get("port", "3306"), 
            user = self.conf.get("user", "root"), 
            password = self.conf.get("pw", ""),
            db = self.conf.get("db", ""),
            connect_timeout=self.conf.get("connect_timeout", 3),
        )
        self.connected = True
     
    async def exec(
        self,
        sql
    ):
        try:
            # print("conected: ", self.connected)
            if not self.connected:
                 await self.init_pool()
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(sql)
                    # result = await cursor.fetchall()
                    result = await asyncio.wait_for(cursor.fetchall(), timeout=self.conf.get("timeout", 3))
                    field_names = [desc[0] for desc in cursor.description]
                    return [dict(zip(field_names, row)) for row in result]
        except pymysql.Error as e:
            print(e)
            return False
        except asyncio.TimeoutError:
            print("连接超时")
            return False          

    async def select_more(
        self,
        table, 
        range_str="", 
        field='*'        
    ):
        try:
            if not self.connected:
                 await self.init_pool()            
            if range_str:
                sql = 'SELECT ' + field + ' FROM ' + table + ' WHERE ' + range_str
            else:
                sql = 'SELECT ' + field + ' FROM ' + table
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(sql)
                    return await cursor.fetchall()
        except pymysql.Error as e:
            print(e)
            return False
        except asyncio.TimeoutError:
            print("连接超时")
            return False

    async def select_limit_asc_order(
        self, 
        table, 
        order_column, 
        limit_num=4, 
        field='*'
    ):
        """ Get latest list in desc order"""

        try:
            if not self.connected:
                 await self.init_pool()            
            sql = 'SELECT ' + field + ' FROM ' + table + \
                ' order by ' + order_column + \
                ' desc limit ' + str(limit_num)
            # print("sql: ", sql)
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(sql)
                    # result = await asyncio.wait_for(cursor.fetchall(), timeout=self.conf.get("timeout", 3))
                    result = await cursor.fetchall()
                    # print("result: ", result)
                    field_names = [desc[0] for desc in cursor.description]
                    data = [dict(zip(field_names, row)) for row in result]
                    # print("data: ", data)
                    if data:
                        data.reverse()
                    return data
        except pymysql.Error as e:
            print(e)
            return False
        except asyncio.TimeoutError:
            print("连接超时")
            return False

    async def select_ordered_multirows_format(
        self,
        table,
        order_str,
        limit_num=5,
        columns_to_names=None,
        latest={},   
        with_chart=False,
        with_text=True,
        key_prefix="Sequential ",
        key_postfix= "",
        **kwargs        
    ) -> Dict[str, Any]:
        """Choose list of data order by order_str

        Args:
            table: 原始table
            order_str: 排序的key
            limit_num=5: 图表展示多少数据
            columns_to_names=None: 查询哪些字段出来
            latest={"key": "DATE", "order":1}: 是否查询最近,传入模型排序key名称比如DATE
            with_chart=False: 是否展示图标
            key_prefix=" in sequencial order: ": 文案前缀
            key_postfix= "": 文案后缀

        Returns:

        """
        # 构造fields查询
        if columns_to_names is None:
            fields = "*"
        else:
            fields = ", ".join(k for k, v in columns_to_names.items())

        if order_str not in fields:
            fields += ", " + order_str

        # 查询最近的
        if latest:
            latest_order = latest.get("order", 1)
            latest_key = latest.get("key")    
            date = await self.select_limit_asc_order(
                table = table,
                order_column = latest_key,
                limit_num = latest_order,
                field = latest_key
            )
            # print("date: ", date)
            if len(date) >= latest_order:
                date = date[latest_order-1][latest_key]
                if "where" in table:
                    table = table + " and " + latest_key + "='" + date + "'"
                else:
                    table = table + " where " + latest_key + "='" + date + "'"
            else:
                return

        # 按照order_str排序，查询数据
        data = await self.select_limit_asc_order(
            table=table,
            order_column=order_str,
            limit_num=limit_num,
            field=fields
        )
        # print("data: ", data)
        result = {}
        if data:
            if with_text:
                idx = 0
                # 构造文本输出
                for line in data:
                    for k, v in line.items():
                        if k in columns_to_names:
                            if k == order_str:
                                columns_to_names[k] = columns_to_names[k] + ", "
                                continue # remove Time Order in String
                            if 0 == idx:
                                columns_to_names[k] = key_prefix + columns_to_names[k] + ": "
                            try:
                                columns_to_names[k] += num_to_string(v) + ", "
                            except:
                                columns_to_names[k] += str(v) + ", "
                    idx += 1
                if fields == "*":
                    result["result"] = "\n".join(k + " : " + v for k, v in columns_to_names.items())
                else:
                    result["result"] = "\n".join(v[:-2] + key_postfix for k, v in columns_to_names.items())
            if with_chart:
                result["chart"] = data
        return result

    async def select_ordered_pair_format(
        self,
        table,
        order_str,
        dimention,        
        limit_num=5,
        latest={},        
        with_chart=False,
        with_text=True,
        key_prefix=" in sequencial order: ",
        key_postfix= "",
        **kwargs        
    ) -> Dict[str, Any]:
        """Get key value pair from column in sorted format

        Args:
            table: 原始table
            order_str: 排序的key
            limit_num=5: 图表展示多少数据
            summary_num=5: 文字部分展示多少数据
            summary_mode='sample': 数据是否采样，默认输出最近的数据
            dimention= "SECURITY_NAME": 被排序的字段
            latest={"key": "DATE", "order":1}: 是否查询最近,传入模型排序key名称比如DATE
            with_chart=False: 是否展示图标
            key_prefix=" in sequencial order: ": 文案前缀
            key_postfix= "": 文案后缀

        Returns:
        """
   
        if latest:
            latest_order = latest.get("order", 1)
            latest_key = latest.get("key")    
            date = await self.select_limit_asc_order(
                table = table,
                order_column = latest_key,
                limit_num = latest_order,
                field = latest_key
            )
            if len(date) >= latest_order:
                date = date[latest_order-1][latest_key]
                if "where" in table:
                    table = table + " and " + latest_key + "='" + date + "'"
                else:
                    table = table + " where " + latest_key + "='" + date + "'"

        # 按照order_str排序，查询数据
        fields = dimention + "," + order_str
        data = await self.select_limit_asc_order(
            table=table,
            order_column=order_str,
            limit_num=limit_num,
            field= fields
        )
        result = {}
        if data:
            if with_text:
                result_str = ""
                for line in data:
                    result_str += line[dimention] + ": "
                    order_str_val = line[order_str]
                    try:
                        result_str += num_to_string(order_str_val) + ", "
                    except:
                        result_str += str(order_str_val) + ", "
                if result_str:
                    result["result"] = key_prefix + result_str[:-2] + key_postfix
            if with_chart:
                result["chart"] = data
        return result

    # 直接执行sql查询多条数据在数据表中
    async def select_simple_multival_format(
        self,
        table,
        columns_to_names,
        dimention="",
        key_prefix = "",
        key_postfix = "",
        with_chart = False,
        **kwargs
    ):
        """Get multi value from same column and merge them directly

        Args:
            table: 原始table
        
        Returns:
            result: Dict of data
        """
        # 构造fields查询
        if columns_to_names is None:
            fields = "*"
        else:
            fields = ", ".join(k for k, v in columns_to_names.items())
            fields += ", " + dimention
    
        sql = "select " + fields + " from " + table

        # print(sql)
        data = await self.exec(sql)
        result = {}
        if data:
            vret = []
            for line in data:
                line_str = ""
                for k, v in line.items():
                    if k == dimention:
                        line_str = key_prefix + line[k] + ":" + line_str
                        continue
                    try:
                        line_str += columns_to_names.get(k, "") + ":" + num_to_string(v) + ", "
                    except:
                        line_str += columns_to_names.get(k, "") + ":" + str(v) + ", "
                vret.append(line_str)
    
            result["result"] = "\n".join(r[:-2] + key_postfix for r in vret)
            # 返回图表数据
            if with_chart:
                result["chart"] = data
        return result

    async def select_values_pair_format(
        self,
        table,
        order_str,
        value_key,
        dimention_to_values = {},          
        limit_num=5,
        summary_num=5,
        latest={},        
        with_chart=False,
        key_prefix=" in sequencial order: ",
        key_postfix= "",
        **kwargs        
    ):
        """Get different value of single key and group them to a listed format

        Args:
            table: 原始table
            order_str: 排序的key
            limit_num=5: 图表展示多少数据
            summary_num=5: 文字部分展示多少数据
            summary_mode='sample': 数据是否采样，默认输出最近的数据
            dimention= "SECURITY_NAME": 被排序的字段
            latest={"key": "DATE", "order":1}: 是否查询最近,传入模型排序key名称比如DATE
            with_chart=False: 是否展示图标
            key_prefix=" in sequencial order: ": 文案前缀
            key_postfix= "": 文案后缀
        """
        # 构造fields查询
        fields = ", ".join(k for k, v in dimention_to_values.items()) + ", " + value_key

        if order_str not in fields:
            fields += ", " + order_str
   
        if latest:
            latest_order = latest.get("order", 1)
            latest_key = latest.get("key")    
            date = await self.select_limit_asc_order(
                table = table,
                order_column = latest_key,
                limit_num = latest_order,
                field = latest_key
            )
            if len(date) >= latest_order:
                date = date[latest_order-1][latest_key]
                if "where" in table:
                    table = table + " and " + latest_key + "='" + date + "'"
                else:
                    table = table + " where " + latest_key + "='" + date + "'"

        # 按照order_str排序，查询数据
        data = await self.select_limit_asc_order(
            table=table,
            order_column=order_str,
            limit_num=limit_num,
            field=fields
        )
        result = {}
        if data:
            columns_to_names = {}
            for line in data:
                for k, v in dimention_to_values.items():
                    col_key = line[k]
                    if col_key in v:
                        col_key = v[col_key]
                    col_val = line[value_key]
                    try:
                        col_val = num_to_string(col_val)
                    except:
                        col_val = str(col_val)

                    if col_key in columns_to_names:
                        columns_to_names[col_key] += "," + line[order_str] + ":" + col_val
                    else:
                        columns_to_names[col_key] = line[order_str] + ":" + col_val
            result["result"] = "\n".join([k + " " + v for k, v in columns_to_names.items()])

            if with_chart:
                result["chart"] = data
        return result


class DataBaseManager(metaclass=Singleton):
    name_to_databases: Dict[str, Database] = {}

    def _add(
        self,
        name: str, 
        db: Database 
    ) -> None:
        try:
            if name not in self.name_to_databases:
                self.name_to_databases.update({name: db})
        except Exception as e:
            raise e
    def get(
        self, 
        name: str
    ):
        return self.name_to_databases.get(name, None)

    def __init__(
        self,
        conf
    ):
        conf = conf.get("db")
        for k, v in conf.items():
            if v.get("async", False):
                self._add(k, AsyncDB(v))
            else:
                self._add(k, Database(v))

    # def get_data(
    #     self,
    #     table,
    #     source,
    # ):
    #     # print(table)
    #     data = None
    #     source_type = source.get("source_type", "key_value_list_output")        
    #     if source_type == "key_value_list_output":                             
    #         data = self.get(source["db"]).get_key_value_column_pair_summary(
    #             table = table,
    #             **source
    #         )
    #     elif source_type == "key_value_pair_output":
    #         data = self.get(source["db"]).get_key_value_column_pair_summary(
    #             table = table,
    #             **source
    #         )
    #     elif source_type == "key_multival_per_column":
    #         data = self.get(source["db"]).get_key_multival_per_column_summary(
    #             table = table,
    #             **source
    #         )
    #     elif source_type == "value_as_keys_output":
    #         data = self.get(source["db"]).get_value_list_column_merge_summary(
    #             table = table,
    #             **source                                    
    #         )
    #     return data


    async def get_data(
        self,
        table,
        source,
    ):
        # print(table)
        data = None
        source_type = source.get("source_type", "key_value_list_output")        
        if source_type == "key_value_list_output":                             
            data = await self.get(source["db"]).select_ordered_multirows_format(
                table = table,
                **source
            )
        elif source_type == "key_value_pair_output":
            data = await self.get(source["db"]).select_ordered_pair_format(
                table = table,
                **source
            )
        elif source_type == "key_multival_per_column":
            data = await self.get(source["db"]).select_simple_multival_format(
                table = table,
                **source
            )
        elif source_type == "value_as_keys_output":
            data = await self.get(source["db"]).select_values_pair_format(
                table = table,
                **source                                    
            )
        return data