# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-11 10:34:53
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-11 10:34:53
@Desc:
    http://www.meizitu.com/a/3525.html
    ...
    http://www.meizitu.com/a/5585.html
    爬取妹子图网站上面的图片
"""

import basecrawler
import basedbmgr
from mytool import pubdefines

TABLE_TEXT = """
create table if NOT EXISTS {}
(
    bid int unsingned primary key,
    tag TEXT,
    title TEXT,
    content TEXT
)
"""

FOLDER_NAME = "meizitu"
RESOURCE_DIR = "resources/{}".format(FOLDER_NAME)


class CDBManager(basedbmgr.CDBManager):
    tablename = "meizitu"
    dbfile = "{}/{}.sql".format(FOLDER_NAME, tablename)
    create_table_info = TABLE_TEXT.format(tablename)
    resourcename = "resources/{}/{}".format(FOLDER_NAME, tablename)

    keylist = ["bid"]
    colinfo = {
        "bid": int,
        "tag": str,
        "title": str,
        "content": str,
    }

    def insert_info(self, bid, tag, title, content):
        if bid in self.dbkeylist:
            return 1  # 已存在数据库
        obj = CDBObject(bid, tag, title, content)
        sql = self.get_insert_sql(obj)
        self.execute(sql)
        self.dbkeylist.append(bid)
        return 0

    def db_has_key(self, bid):
        if bid in self.dbkeylist:
            return True
        return False

    def get_max_key(self):
        return max(self.dbkeylist)


class CDBObject(object):
    def __init__(self, bid, tag, title, content):
        self.bid = bid
        self.tag = tag
        self.title = title
        self.content = content


class MeiZiTu(basecrawler.CWebCrawler):
    url = "http://www.meizitu.com/a/"
    logdir = FOLDER_NAME

    def __init__(self):
        super(MeiZiTu, self).__init__()
        self.dbmgr = CDBManager()

    def start(self):
        beginadr = self.dbmgr.get_max_key() + 1
        for adr in range(beginadr, 8888):
            url = self.url + str(adr) + ".html"
            self.get_url_info(url, adr)

    def get_url_info(self, url, adr):
        if self.dbmgr.db_has_key(adr):
            return
        bs4obj = self.get_bs4_by_url(url)
        if not bs4obj:
            return
        print("begin {}".format(url))
        title = tags = context = ""
        for odiv in bs4obj.findAll("div", class_="metaRight"):
            oh2 = odiv.h2
            oop = odiv.p
            title = pubdefines.filter(oh2.text)
            tags = pubdefines.filter(oop.text)
            tags = tags.replace("Tags:", "").replace(" , ", " ").rstrip()
        for odiv in bs4obj.findAll("div", id="picture"):
            oop = odiv.a
            if not oop:
                continue
            context = odiv.text
            context = pubdefines.filter(context)
        num = 1

        """
        3525-3979
        for oimg in bs4obj.findAll("img", class_="scrollLoading"):
            src = oimg.get("src")
            suffix = src.split(".")[-1]
            filename = title + str(num) + "." + suffix
            mydir = RESOURCE_DIR + "/" + str(adr // 100 * 100)
            picdata = self.get_data_by_url(src)
            if not picdata:
                continue
            pubdefines.dowland_pic(mydir, filename, picdata)
            num += 1
        """
        for odiv in bs4obj.findAll("div", id="picture"):
            oop = odiv.p
            for oimg in oop.findAll("img"):
                src = oimg.get("src")
                suffix = src.split(".")[-1]
                filename = oimg.get("alt") + "." + suffix
                mydir = RESOURCE_DIR + "/" + str(adr // 100 * 100)
                picdata = self.get_data_by_url(src)
                if not picdata:
                    continue
                pubdefines.dowland_pic(mydir, filename, picdata)
                num += 1

        if num == 1:
            self.log("fail {}".format(url))
            return

        binsert = self.dbmgr.insert_info(adr, tags, title, context)
        if binsert:
            print("\texist {}".format(url))
        else:
            print("\tdownload {}".format(url))
