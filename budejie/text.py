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
create table if NOT EXISTS {}
(
    bid int unsingned primary key,
    content TEXT
)
"""


class CDBManager(dbmanager.CDBManager):
    dbfile = "budejie/budejie.sql"
    tablename = "text"
    create_table_info = TABLE_TEXT.format(tablename)

    keylist = ["bid"]
    colinfo = {
        "bid": int,
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
        if key in self.dbkeylist:
            return 1  # 已存在数据库
        obj = CDBObject(key, content)
        sql = self.get_insert_sql(obj)
        self.execute(sql)
        self.dbkeylist.append(key)
        return 0


class CDBObject(object):
    def __init__(self, bid, content):
        self.bid = bid
        self.content = content


class CText(basecrawler.CWebCrawler):
    url = "http://www.budejie.com/text/"

    def __init__(self):
        super(CText, self).__init__()
        self.dbmgr = CDBManager()

    def find_all_url(self):
        for adr in range(1, 100):
            url = self.url + str(adr)
            url_return = self.get_url_info(url)
            if not url_return:
                return

    def start(self):
        self.find_all_url()
        self.done()

    def get_url_info(self, url):
        bs4obj = self.get_bs4_by_url(url)
        if not bs4obj:
            return False
        binsert = 1
        for oclass in bs4obj.findAll("div", class_=re.compile("j-r-list-c-desc")):
            tmp = oclass.a
            html = tmp.attrs["href"]
            htmlid = html.replace("/detail-", "").replace(".html", "")
            htmlid = int(htmlid)
            text = tmp.text
            text = text.replace(" ", "")
            binsert = self.dbmgr.insert_info(htmlid, text)
        if binsert:
            print("exist {}".format(url))
        else:
            print("done\t{}".format(url))
        return True
