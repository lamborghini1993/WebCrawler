# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-02 16:00:43
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-02 16:00:43
@Desc:
    百思不得姐 段子获取
    http://www.budejie.com/text/
"""

import re
import basecrawler
import basedbmgr
from pubcode import pubdefines

TABLE_TEXT = """
create table if NOT EXISTS {}
(
    bid int unsingned primary key,
    content TEXT
)
"""

FOLDER_NAME = "budejie"


class CDBManager(basedbmgr.CDBManager):
    tablename = "text"
    dbfile = "{}/{}.sql".format(FOLDER_NAME, tablename)
    create_table_info = TABLE_TEXT.format(tablename)
    resourcename = "resources/{}/{}".format(FOLDER_NAME, tablename)

    keylist = ["bid"]
    colinfo = {
        "bid": int,
        "content": str,
    }

    def insert_info(self, key, content):
        if key in self.dbkeylist:
            return 1  # 已存在数据库
        obj = CDBObject(key, content)
        sql = self.get_insert_sql(obj)
        self.execute(sql)
        self.dbkeylist.append(key)
        return 0

    def sql_to_resource(self):
        result = self.query()
        for _, content in result:
            content += "\t\n"
            pubdefines.write_to_file(self.resourcename, content)


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

    def resource(self):
        self.dbmgr.sql_to_resource()

    def get_url_info(self, url):
        bs4obj = self.get_bs4_by_url(url)
        if not bs4obj:
            return False
        binsert = 1
        pat = re.compile("j-r-list-c-desc")
        for oclass in bs4obj.findAll("div", class_=pat):
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
            print("download {}".format(url))
        return True
