# -*- coding: utf-8 -*-

"""
http://dp.2980.com
从2980网盘爬取免费分享的文件
"""

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from urllib import parse, request
from http import cookiejar
from mytool import pubdefines
import urllib.request
import urllib.parse

import basecrawler
import re, os

lst = [
    "http://t.2980.com/96veF", 
    "http://t.2980.com/g7jg2",
    "http://t.2980.com/96veG",
]

ERROR_TITLE = "网盘-哎哟，您来晚了，分享的文件已经被取消了，下次要早点来哟"
COOKIE_INFO ={
    'acct':'xiaohao@henhaoji.com',
    'logincode':'',
    'userid':2051657720,
    'uid':1685226154,
    'eid':0,
    'nick':'程序-工具链-肖豪',
}



class CDP2980(basecrawler.CWebCrawler):

    MyHead = {
        "Cookie" : urllib.parse.urlencode(COOKIE_INFO).replace("&", ";")
    }

    def __init__(self):
        self.headers.update(self.MyHead)

    def start(self):
        ss = ""
        for x in range(ord('0'), ord('9') + 1):
            ss += chr(x)
        for x in range(ord('A'), ord('Z') + 1):
            ss += chr(x)
        for x in range(ord('a'), ord('z') + 1):
            ss += chr(x)
        self.Example = ss
        self.DFS("", 0)

    def DFS(self, s, t):
        if t == 5:
            url = "http://t.2980.com/" + s
            obs4 = self.get_bs4_by_url(url)
            print(url)
            for oTitle in obs4.find("title"):
                sTitle = oTitle.title()
                if sTitle.find(ERROR_TITLE) != -1:
                    continue
                print(sTitle)
                pubdefines.write_to_file("2980", url)
            return

        for c in self.Example:
            self.DFS(s + c, t + 1)
