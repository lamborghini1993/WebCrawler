# -*- coding:utf-8 -*-

"""
三五中文网   http://www.35zww.com/
"""

import basecrawler
import re
import os

MyURLs = """
http://www.35zww.com/35zwhtml/51/51250/
http://www.35zww.com/35zwhtml/51/51228/
http://www.35zww.com/35zwhtml/51/51202/
http://www.35zww.com/35zwhtml/51/51220/
http://www.35zww.com/35zwhtml/51/51215/
http://www.35zww.com/35zwhtml/51/51241/
http://www.35zww.com/35zwhtml/51/51246/
http://www.35zww.com/35zwhtml/51/51216/
"""

lstDel = [
    "read_content_up();",
    "三↑五↑中↑文↑网",
    "ｗww.35ｚww.ｃom，更新最快的无弹窗小说网！",
    "www.35zｗｗ.com，更新快、无弹窗！",
    "三●五●中●文●网",
    "[，，，！]",
    "[]",
    "www.35zｗｗ.com，更新快、无弹窗！        ",
]


class C35ZWW(basecrawler.CWebCrawler):

    def DownlandBook(self, url):
        bs4obj = self.get_bs4_by_url(url)
        if not bs4obj:
            return
        oBookName = bs4obj.find("div", id="title")
        sBookName = oBookName.text.replace("全文阅读","")
        sFileName = "Downloads/%s.txt" % sBookName
        if os.path.exists(sFileName):
            return
        print("begin %s" % sBookName)
        fp = open(sFileName, "w+", encoding="utf-8")
        fp.writelines("=============%s===============\n" % sBookName)
        for oA in bs4obj.findAll("a", href=re.compile("^\d*.html")):
            sTitle = oA.get("title", None)
            sHref = oA.get("href", None)
            if not sTitle or not sHref:
                continue
            fp.writelines("%s\n" % sTitle)
            self.Write2Book(fp,url+sHref)
            print("\t%s" % sTitle)
        print("%s Done" % sBookName)


    def Write2Book(self, fp, url):
        bs4obj = self.get_bs4_by_url(url)
        oScript = bs4obj.find("div", id="content")
        sText = oScript.text.replace("    ", "\n")
        for sDel in lstDel:
            sText = sText.replace(sDel+"\n", "")
            sText = sText.replace(sDel, "")
        fp.writelines(sText)
        fp.writelines("\n"*8)


    def start(self):
        lstURL = []
        for url in MyURLs.split("\n"):
            if not url:
                continue
            self.DownlandBook(url)



