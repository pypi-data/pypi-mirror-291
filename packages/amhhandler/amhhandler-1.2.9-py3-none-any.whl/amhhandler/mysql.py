#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@time   : 2020/9/21 16:39
@file   : mysql.py
@author : 
@desc   : 
@exec   : 
"""
import pymysql
from pymysql.cursors import DictCursor


class Conn(object):
    """定义一个 MySQL 操作类"""

    def __init__(self, **config):
        """初始化数据库信息并创建数据库连接"""
        if not config:
            raise ValueError("Connect config cannot be empty!")

        for k, v in config.items():
            if k == 'charset' and v not in ('utf8', 'utf8mb4'):
                config[k] = 'utf8mb4'
            if k == 'port' and not isinstance(v, int):
                try:
                    config[k] = int(v)
                except ValueError:
                    config[k] = 3306

        try:
            self.conn = pymysql.connect(**config)
            with self.conn.cursor() as self.cur:
                pass  # 测试mysql是否通
        except Exception as e:
            raise Exception(f"Failed to connect to the mysql server. Error: {e}")

    def select(self, select_sql, return_type=None):
        """执行select, show 类查询，有返回值"""
        if not select_sql or not isinstance(select_sql, str):
            raise ValueError("select_sql cannot be empty!")

        cursor_type = DictCursor if return_type and return_type.lower() in ("dict", "d") else None
        with self.conn.cursor(cursor_type) as cur:
            try:
                cur.execute(select_sql)
                rt_tuple = cur.fetchall()
                return rt_tuple
            except Exception as e:
                raise Exception(f"Failed to execute the sql: {select_sql}. Error: {e}.")

    def exec(self, sql):
        """执行非查询类语句"""
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Failed to execute the sql: {sql}. Error: {e}.")

    def close(self):
        self.cur.close()
        self.conn.close()
