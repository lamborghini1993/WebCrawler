# -*- coding: utf-8 -*-
# 肖豪

import sqlite3


class CDBManager(object):
    """轻量级数据库基类"""

    dbname = ""
    createtable = ""
    tablename = ""

    def __init__(self):
        self.conn = None
        self.creat_table()

    def init_conn(self):
        if self.conn:
            return
        self.conn = sqlite3.connect(self.dbname)

    def creat_table(self):
        self.execute(self.createtable)
        self.execute("use {}".format(self.tablename))

    def get_cursor(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.dbname)
        cursor = self.conn.cursor()
        return cursor

    def execute(self, sql):
        self.init_conn()
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        cursor.close()
