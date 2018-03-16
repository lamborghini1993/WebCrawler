# -*- coding: utf-8 -*-

"""
http://dp.2980.com
从2980网盘爬取免费分享的文件
"""


import urllib.request
import basecrawler
import re

lst = [
    "http://t.2980.com/96veF", 
    "http://t.2980.com/g7jg2",
    "http://t.2980.com/96veG",
]

ERROR_TITLE = "网盘-哎哟，您来晚了，分享的文件已经被取消了，下次要早点来哟"

class CDP2980(basecrawler.CWebCrawler):

    MyHead = {
        "Cookie" : "acct=xiaohao%40henhaoji.com; nick=%E7%A8%8B%E5%BA%8F-%E5%B7%A5%E5%85%B7%E9%93%BE-%E8%82%96%E8%B1%AA; logincode=; eid=0; userid=2051657720; uid=a655646786"
    }

    def __init__(self):
        self.headers.update(self.MyHead)

    def start(self):
        for sUrl in lst:
            obs4 = self.get_bs4_by_url(sUrl)
            for oTitle in obs4.find("title"):
                sTitle = oTitle.title()
                if sTitle.find(ERROR_TITLE) == -1:
                    print(sUrl, sTitle)
