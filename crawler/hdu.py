# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-06-29 18:57:06
@Desc: 爬取HDU的题目，除去自己完成的题目，按照完成数量从高到低排序
    http://acm.hdu.edu.cn/listproblem.php?vol=1
"""

import re
from pubcode import pubcrawler, misc
from bs4 import BeautifulSoup

INFO = re.compile(r"p(.*?);")


class HDU(pubcrawler.CPubCrawler):
    m_Flag = "HDU"
    m_Url = "http://acm.hdu.edu.cn/listproblem.php?"
    m_MyHeader = {
        "Cookie": "PHPSESSID=m8fu2e6sbgtenj9d6m1rii79r3; exesubmitlang=0",
        "Host": "acm.hdu.edu.cn",
        "Upgrade-Insecure-Requests": "1",
        "Accept-Encoding": "gzip,deflate",
    }
    m_DebugPrint = True
    # GB2312，GBK，GB18030，是兼容的，包含的字符个数：GB2312 < GBK < GB18030
    m_Encoding = "gb18030"

    def _CustomInit(self):
        for x in range(1, 54):
            pageurl = self.m_Url + "vol=" + str(x)
            dPageInfo = {
                "priority": 0,
            }
            self.m_WaitingUrl[pageurl] = dPageInfo

    def _Load(self):
        super(HDU, self)._Load()
        self.m_DoneInfo = {}

    async def MyParse(self, url, dInfo, html):
        iType = dInfo["priority"]
        soup = BeautifulSoup(html, "lxml")
        if iType == 0:
            await self.ParsePage(url, dInfo, soup)

    async def ParsePage(self, pageurl, dPageInfo, soup):
        for oA in soup.findAll("script", {"language": "javascript"}):
            alltext = oA.text
            if alltext.find("function p(color,pid,solved,title,ac,sub)") != -1:
                continue
            for sInfo in INFO.finditer(alltext):
                ss = sInfo.group()
                ss = re.sub(r",\".*\"", "", ss)
                ss = ss.replace("p(", "")
                ss = ss.replace(");", "")
                _, ID, Done, AC, Submit = ss.split(",")
                # ID = int(ID)
                Done = int(Done)
                AC = int(AC)
                Submit = int(Submit)
                if not Done:
                    self.m_DoneInfo[ID] = (AC, Submit)
