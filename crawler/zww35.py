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

DEL_LINE = [
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
            pageurl = self.m_Example + str(x) + ".htm"
            dPageInfo = {"priority":0}
            self.m_WaitingUrl[pageurl] = dPageInfo


    async def Parse(self, url, dInfo, html):
        iType = dInfo["priority"]
        if iType == 0:
            await self.ParsePage(url, dInfo, html)
        elif iType == 1:
            await self.ParseBook(url, dInfo, html)
        elif iType == 2:
            await self.ParseChapter(url, dInfo, html)


    async def ParsePage(self, pageurl, dPageInfo, html):
        soup = BeautifulSoup(html, 'lxml')
        allBookUrl = dPageInfo.setdefault("allurl", [])
        for oA in soup.findAll("a", {"href":re.compile("/35zwhtml/\d+/\d+/$")}):
            if oA.has_attr("style"):
                continue
            bookurl = self.m_Url + oA.get("href")

            if bookurl in self.m_DoneInfo:
                continue
            if bookurl in allBookUrl:
                continue

            allBookUrl.append(bookurl)
            dBookInfo = {
                "priority"  :1,
                "parent"    :pageurl,
            }
            self.m_WaitingUrl[bookurl] = dBookInfo
            # print("Add Book url ", bookurl)
        
        del self.m_DoingUrl[pageurl]
        # self.m_DoneInfo[pageurl] = self.m_DoingUrl.pop(pageurl)
        print("Page Done ", pageurl, len(allBookUrl))


    async def ParseBook(self, bookurl, dBookInfo, html):
        soup = BeautifulSoup(html, 'lxml')
        sTitle = soup.find("div", {"id":"title"}).h1.text
        dBookInfo["title"] = sTitle
        oDetails = soup.find("div", {"id":"details"})
        sAuthor = oDetails.find("a", {"href":re.compile("/author/*")}).text
        oLastUrl = oDetails.find("a", {"href":re.compile("\d+.html")})
        sLastUrl = bookurl + oLastUrl.get("href")
        dBookInfo["author"] = sAuthor
        dBookInfo["latest_chapter_url"] = sLastUrl

        oType = soup.find("div", {"id":"indexsidebar"})
        sType = oType.find("a", {"href":re.compile(".*htm")}).text
        dBookInfo["type"] = sType

        allChapterUrl = dBookInfo.setdefault("allurl", [])
        for oA in soup.findAll("a", {"href":re.compile("\d+.html")}):
            if not oA.has_attr("title"):
                continue
            chapterurl = bookurl + oA.get("href")

            if chapterurl in allChapterUrl:
                continue

            allChapterUrl.append(chapterurl)
            dChapterInfo = {
                "priority"  :2,
                "parent"    :bookurl,
            }
            # print("Add Chapter url ", chapterurl)
            self.m_WaitingUrl[chapterurl] = dChapterInfo

        self.m_DoneInfo[bookurl] = self.m_DoingUrl.pop(bookurl)
        print("Book Done ", sType, sTitle, bookurl, len(allChapterUrl))


    async def ParseChapter(self, chapterurl, dChapterInfo, html):
        soup = BeautifulSoup(html, 'lxml')
        sChapterTitle = soup.find("div", {"id":"title"}).h1.text

        oScript = soup.find("div", id="content")
        sText = oScript.text.replace("    ", "\n")
        for sDel in DEL_LINE:
            sText = sText.replace(sDel+"\n", "")
            sText = sText.replace(sDel, "")

        dChapterInfo["text"] = sText
        dChapterInfo["chapter_title"] = sChapterTitle

        self.m_DoneInfo[chapterurl] = self.m_DoingUrl.pop(chapterurl)
        print("Chapter Done ", sChapterTitle, chapterurl)

        self.CheckWriteBook(dChapterInfo["parent"])


    def CheckWriteBook(self, bookurl):
        dBookInfo = self.m_DoneInfo[bookurl]
        lstAllUrl = dBookInfo["allurl"]
        sTitle = dBookInfo["title"]
        sType = dBookInfo["type"]
        sDir = os.path.join(self.m_DownPath, sType)
        if not os.path.exists(sDir):
            os.makedirs(sDir)
        sFilePath = os.path.join(sDir, sTitle + ".txt")
        with open(sFilePath, "a+", encoding="utf-8") as fp:
            while lstAllUrl and lstAllUrl[0] in self.m_DoneInfo:
                chapterurl = lstAllUrl.pop(0)
                dChapterInfo = self.m_DoneInfo.pop(chapterurl)
                sChapterTitle = dChapterInfo["chapter_title"]
                sText = dChapterInfo["text"]

                fp.writelines("=============%s=============\n" % sChapterTitle)
                fp.writelines(sText)
                fp.writelines("\n"*8)

                print("write to book:", sTitle, sType, sChapterTitle)

        if not lstAllUrl:   # 全部下载完毕
            dNewBookInfo = {
                "statue"            :True,
                "latest_chapter_url"    :dBookInfo["latest_chapter_url"]
            }
            self.m_DoneInfo[bookurl] = dNewBookInfo
            print("%s all done" % sTitle)


        # lstDoing = self.m_XXOO[bookurl]
        # self.m_XXOO[chapterurl] = sText

        # while lstDoing and lstDoing[0] in self.m_XXOO:
        #     chapterurl = lstDoing.pop(0)
        #     sText = self.m_XXOO.pop(chapterurl)
        #     path = os.path.join(self.m_DownPath, title + ".txt")
        #     with open(path, "w+", encoding="utf-8") as fp:
        #         fp.writelines(sText)
        #         fp.writelines("\n"*8)
        #     tInfo = (chapterurl, 2, bookurl, title, chapterurl)
        #     self.m_DoingUrl.remove(tInfo)
        #     print("%s done" % chapterurl)
        # if not lstDoing:
        #     self.m_DoingUrl.remove(bookurl)
