# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-02 16:00:43
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-02 16:00:43
@Desc:
    百思不得姐段子
    http://www.budejie.com/text/
"""

import re
import basecrawler
from db import dbmanager


TABLE_TEXT = """
create table if NOT EXISTS text
(
    id int unsingned primary key,
    content TEXT
)
"""


class CDBManager(dbmanager.CDBManager):
    createtable = TABLE_TEXT
    dbname = "budejie.sql"
    tablename = "text"

    keylist = ["id"]
    colinfo = {
        "id": int,
        "content": str,
    }

    def get_col_data(self, value):
        if isinstance(value, str):
            return "'{}'".format(value)
        return str(value)

    def get_insert_sql(self, obj):
        name_list = []
        value_list = []
        for colname, mytype in self.colinfo.items():
            value = getattr(obj, colname, None)
            if not isinstance(value, mytype):
                raise Exception("{} not {} type. {}".format(
                    colname, mytype, value))
            name_list.append(colname)
            value_list.append(self.get_col_data(value))
        colnames = ",".join(name_list)
        colvalues = ",".join(value_list)
        sql = "insert into {}({}) values({})".format(
            self.tablename, colnames, colvalues)
        return sql

    def insert_info(self, key, content):
        obj = CDBObject(key, content)
        sql = self.get_insert_sql(obj)
        self.execute(sql)

    def get_key_list(self):
        keynames = ",".join(self.keylist)
        sql = "select {} from {}".format(keynames, self.tablename)
        sql = "select * from {}".format(self.tablename)
        print(sql)
        result = self.execute(sql)
        print(result)


class CDBObject(object):
    def __init__(self, id, content):
        self.id = id
        self.content = content


class CText(basecrawler.CWebCrawler):
    url = "http://www.budejie.com/text/"

    def __init__(self):
        super(CText, self).__init__()
        self.dbmgr = CDBManager()

    def start(self):
        self.dbmgr.get_key_list()
        return
        url = self.get_url()
        bs4obj = self.get_bs4_by_url(url)
        for oclass in bs4obj.findAll("div", class_=re.compile("j-r-list-c-desc")):
            tmp = oclass.a
            html = tmp.attrs["href"]
            htmlid = html.replace("/detail-", "").replace(".html", "")
            htmlid = int(htmlid)
            text = tmp.text
            text = text.replace(" ", "")
            self.dbmgr.insert_info(htmlid, text)
            return

    def get_url(self):
        return self.url
