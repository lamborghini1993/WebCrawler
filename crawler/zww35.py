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
import os

from bs4 import BeautifulSoup

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



class CZww35(pubcrawler.CPubCrawler):
    m_Flag = "zww35"
    m_Example = "http://www.35zww.com/zwwtopallvisit/0/"
    m_Url = "http://www.35zww.com/"


    def _CustomInit(self):
        # for x in range(2146):
        for x in range(1):
            url = self.m_Example + str(x) + ".htm"
            tInfo = (url, 0)
            self.m_WaitingUrl.add(tInfo)


    def _Save(self):
        pass

    async def Parse(self, html, tInfo):
        url, sType, *args = tInfo
        if sType == 0:
            await self.ParsePage(html, url, *args)
        elif sType == 1:
            await self.ParseBook(html, url, *args)
        elif sType == 2:
            await self.ParseChapter(html, url, *args)
            

    async def ParsePage(self, html, pageurl, *args):
        soup = BeautifulSoup(html, 'lxml')
        for oA in soup.findAll("a", {"href":re.compile("/35zwhtml/\d+/\d+/$")}):
            if oA.has_attr("style"):
                continue
            bookurl = self.m_Url + oA.get("href")
            title = oA.text
            tInfo = (bookurl, 1, pageurl, title)
            self.m_WaitingUrl.add(tInfo)
            print(title, bookurl, self.m_WaitingUrl)
            self.Print("4")
            break


    async def ParseBook(self, html, bookurl, *args):
        pageurl, title = args
        soup = BeautifulSoup(html, 'lxml')
        lstDoing = self.m_DownInfo.setdefault(bookurl, [])
        otitle = soup.find("div", {"id":"title"})
        print(otitle)
        for oA in soup.findAll("a", {"href":re.compile("\d+.html")}):
            if not oA.has_attr("title"):
                continue
            chapterurl = self.m_Url + oA.get("href")
            lstDoing.append(chapterurl)
            tInfo = (chapterurl, 2, bookurl, title, chapterurl)
            self.m_WaitingUrl.add(tInfo)
        print(len(lstDoing))


    async def ParseChapter(self, html, chapterurl, *args):
        bookurl, title, chapterurl = args
        soup = BeautifulSoup(html, 'lxml')
        oScript = soup.find("div", id="content")
        sText = oScript.text.replace("    ", "\n")
        for sDel in lstDel:
            sText = sText.replace(sDel+"\n", "")
            sText = sText.replace(sDel, "")

        lstDoing = self.m_DownInfo[bookurl]
        self.m_DownInfo[chapterurl] = sText

        while lstDoing and lstDoing[0] in self.m_DownInfo:
            chapterurl = lstDoing.pop(0)
            sText = self.m_DownInfo.pop(chapterurl)
            path = os.path.join(self.m_DownPath, title + ".txt")
            with open(path, "w+", encoding="utf-8") as fp:
                fp.writelines(sText)
                fp.writelines("\n"*8)
            tInfo = (chapterurl, 2, bookurl, title, chapterurl)
            self.m_DoingUrl.remove(tInfo)

        if not lstDoing:
            self.m_DoingUrl.remove(bookurl)
