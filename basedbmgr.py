# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-03 14:31:20
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-03 14:31:20
@Desc:
    db管理器的基类
"""

import os
import sqlite3
from mytool import pubdefines


def get_col_data(value):
    if isinstance(value, str):
        return "'{}'".format(value)
    return str(value)


class CDBManager(object):
    """轻量级数据库基类"""

    dbfile = ""
    create_table_info = ""
    tablename = ""

    keylist = []
    colinfo = {}

    def __init__(self):
        self.conn = None
        self.dbkeylist = []
        self.dbpath = os.path.join(pubdefines.getpwd(), self.dbfile)
        self.creat_table()
        self.get_dbkeylist()

    def init_conn(self):
        if self.conn:
            return
        self.conn = sqlite3.connect(self.dbpath)

    def creat_table(self):
        self.execute(self.create_table_info)

    def query(self, sql=None):
        if not sql:
            sql = "select * from {}".format(self.tablename)
        self.init_conn()
        cursor = self.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return result

    def execute(self, sql):
        self.init_conn()
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
        except sqlite3.Error as myerr:
            print("err {} {}".format(myerr, sql))
        self.conn.commit()
        cursor.close()

    def get_dbkeylist(self):
        keynames = ",".join(self.keylist)
        sql = "select {} from {}".format(keynames, self.tablename)
        result = self.query(sql)
        for tinfo in result:
            self.dbkeylist.append(tinfo[0])

    def get_insert_sql(self, obj):
        name_list = []
        value_list = []
        for colname, mytype in self.colinfo.items():
            value = getattr(obj, colname, None)
            if not isinstance(value, mytype):
                raise Exception("{} not {} type. {}".format(
                    colname, mytype, value))
            name_list.append(colname)
            value_list.append(get_col_data(value))
        colnames = ",".join(name_list)
        colvalues = ",".join(value_list)
        sql = "insert into {}({}) values({})".format(
            self.tablename, colnames, colvalues)
        return sql
