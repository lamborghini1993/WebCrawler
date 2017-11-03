# -*- coding: utf-8 -*-
# 肖豪

import os
import sqlite3
from mytool import pubdefines


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

    def query(self, sql):
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
        print(self.dbkeylist)
