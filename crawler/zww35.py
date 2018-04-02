# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-04-02 20:21:00
@Desc:  三五中文网
    http://www.35zww.com/
    http://www.35zww.com/zwwtopallvisit/0/0.htm
"""

import pubcrawler
import re

from bs4 import BeautifulSoup

class CZww35(pubcrawler.CPubCrawler):
    m_Flag = "zww35"
    m_MaxNum = 1
    m_Example = "http://www.35zww.com/zwwtopallvisit/0/"
    m_Url = "http://www.35zww.com/"

    def NewCrawel(self):
        iPage = self.m_DownInfo.setdefault("page", 0)
        while len(self.m_CrawlerUrl) < self.m_MaxNum and iPage < 1:
            url = self.m_Example + str(iPage) + ".htm"
            self.m_CrawlerUrl.append(url)
            iPage += 1
        self.m_DownInfo["page"] = iPage
        return True

    async def Parse(self, html, url):
        soup = BeautifulSoup(html, 'lxml')
        for oA in soup.findAll("a", {"href":re.compile("/35zwhtml/\d+/\d+/$")}):
            if oA.has_attr("style"):
                continue
            url = self.m_Url + oA.get("href")
            title = oA.text
            print(title, url)
        self.m_CrawlerUrl.remove(url)