# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-04-02 20:21:00
@Desc:  三五中文网
    http://www.35zww.com/
    http://www.35zww.com/zwwtopallvisit/0/0.htm
"""

import re
import os

from pubcode import misc, pubcrawler
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

ERROR_TITLE = "404 - 页面不存在 - 三五中文网"

WAITING_URL_KEYNAME = "WaitSubUrl"  #等待顺序写入book的url
DONE_URL_KEYNAME = "DoneSubUrl"     #已经写入book的url

class CZww35(pubcrawler.CPubCrawler):
    m_Flag = "book"
    m_DebugPrint = True
    m_Example = "http://www.35zww.com/zwwtopallvisit/0/"
    m_Url = "http://www.35zww.com/"
    m_TryNum = 3    #尝试url的次数
    m_MyHeader = {
        "Cookie"    :"UM_distinctid=161bce4ba8825-085872c0cfe3518-4c322172-232800-161bce4ba8960b; CNZZDATA1263996461=193942989-1519291352-https%253A%252F%252Fwww.baidu.com%252F%7C1523409800; clickbids=5210; cp_speed_8x=66; cp_fontsize_8x=16; cp_bg_8x=%23E7F4FE; PHPSESSID=atvjgleokiruds8jsou2vhtrf4; username=lamborghini",
        "Host"      :"www.35zww.com",
        "Upgrade-Insecure-Requests":"1",
        "Accept-Encoding":"gzip,deflate",
    }

    def _CustomInit(self):
        self._LoadWaitUrl()
        for x in range(10):
            pageurl = self.m_Example + str(x) + ".htm"
            dPageInfo = {
                "priority"  :0,
                "time"      :misc.GetSecond(),
            }
            self.m_WaitingUrl[pageurl] = dPageInfo


    def _LoadWaitUrl(self):
        for bookurl, dBookInfo in self.m_DoneInfo.items():
            for chapterurl in dBookInfo.get(WAITING_URL_KEYNAME, []):
                if chapterurl in self.m_DoneInfo:
                    continue
                dChapterInfo = {
                    "priority"  :2,
                    "parent"    :bookurl,
                    "time"      :misc.GetSecond(),
                }
                self.m_WaitingUrl[chapterurl] = dChapterInfo


    def _Replace(self, sMsg, default="_"):
        sMsg = super(CZww35, self)._Replace(sMsg, default)
        sMsg = sMsg.replace("全文阅读", "")
        return sMsg



    def Is404(self, url, dInfo, soup):
        sTitle = soup.find("title").text
        if sTitle != ERROR_TITLE:    #有内容
            return False
        iNum = self.m_FailUrl.get(url, 0) + 1
        self.m_FailUrl[url] = iNum
        del self.m_DoingUrl[url]
        if iNum < self.m_TryNum:
            return True

        del self.m_FailUrl[url]
        iType = dInfo["priority"]
        if iType == 2:
            bookurl = dInfo["parent"]
            lstAllUrl = self.m_DoneInfo[bookurl].get(WAITING_URL_KEYNAME, [])
            if url in lstAllUrl:
                lstAllUrl.remove(url)
            self.CheckWriteBook(bookurl)
        misc.Write2File(self.m_LogPath, "abandon %s %s" % (url, dInfo))
        return True


    async def Crawl(self, url, dInfo):
        sReferer = dInfo.get("parent", self.m_Url)
        self.m_Headers["Referer"] = sReferer
        super(CZww35, self).Crawl(url, dInfo)


    async def Parse(self, url, dInfo, html):
        iType = dInfo["priority"]
        soup = BeautifulSoup(html, "lxml")
        if self.Is404(url, dInfo, soup):
            return
        if url in self.m_FailUrl:
            del self.m_FailUrl[url]
        if iType == 0:
            await self.ParsePage(url, dInfo, soup)
        elif iType == 1:
            await self.ParseBook(url, dInfo, soup)
        elif iType == 2:
            await self.ParseChapter(url, dInfo, soup)


    async def ParsePage(self, pageurl, dPageInfo, soup):
        allBookUrl = dPageInfo.setdefault(WAITING_URL_KEYNAME, [])
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
                "time"      :misc.GetSecond(),
            }
            self.m_WaitingUrl[bookurl] = dBookInfo
            # print("Add Book url ", bookurl)
        
        del self.m_DoingUrl[pageurl]
        # self.m_DoneInfo[pageurl] = self.m_DoingUrl.pop(pageurl)

        print("本页【%s】爬取完毕, 共需爬取%s本书籍" % (pageurl, len(allBookUrl)))


    async def ParseBook(self, bookurl, dBookInfo, soup):
        oTitle = soup.find("meta", {"property":"og:title"})
        sTitle = oTitle.get("content")
        sTitle = self._Replace(sTitle)
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

        allChapterUrl = dBookInfo.setdefault(WAITING_URL_KEYNAME, [])
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
                "time"      :misc.GetSecond(),
            }
            # print("Add Chapter url ", chapterurl)
            self.m_WaitingUrl[chapterurl] = dChapterInfo

        self.m_DoneInfo[bookurl] = self.m_DoingUrl.pop(bookurl)
        print("%s-《%s》共需爬取%s章节" % (sType, sTitle, len(allChapterUrl)))


    async def ParseChapter(self, chapterurl, dChapterInfo, soup):
        bookurl = dChapterInfo["parent"]
        oDiv = soup.find("div", {"id":"title"})
        sChapterTitle = oDiv.h1.text

        oScript = soup.find("div", id="content")
        sText = oScript.text.replace("    ", "\n")
        for sDel in DEL_LINE:
            sText = sText.replace(sDel+"\n", "")
            sText = sText.replace(sDel, "")

        dChapterInfo["text"] = sText
        dChapterInfo["chapter_title"] = sChapterTitle

        self.m_DoneInfo[chapterurl] = self.m_DoingUrl.pop(chapterurl)
        print("\t本章节<--%s-->爬取完毕" % (sChapterTitle))

        self.CheckWriteBook(bookurl)


    def CheckWriteBook(self, bookurl):
        dBookInfo = self.m_DoneInfo[bookurl]
        lstAllUrl = dBookInfo[WAITING_URL_KEYNAME]
        lstDoneUrl = dBookInfo.setdefault(DONE_URL_KEYNAME, [])
        sTitle = dBookInfo["title"]
        sType = dBookInfo["type"]
        sDir = os.path.join(self.m_DownPath, sType)
        if not os.path.exists(sDir):
            os.makedirs(sDir)
        sFilePath = os.path.join(sDir, sTitle + ".txt")
        with open(sFilePath, "a+", encoding="utf-8") as fp:
            while lstAllUrl and lstAllUrl[0] in self.m_DoneInfo:
                chapterurl = lstAllUrl.pop(0)
                if chapterurl in lstDoneUrl:
                    misc.Write2File(self.m_LogPath, "Err: %s已经在书籍中了" % (chapterurl))
                    continue
                lstDoneUrl.append(chapterurl)
                dChapterInfo = self.m_DoneInfo.pop(chapterurl)
                sChapterTitle = dChapterInfo["chapter_title"]
                sText = dChapterInfo["text"]

                fp.writelines("=============%s=============\n" % sChapterTitle)
                fp.writelines(sText)
                fp.writelines("\n"*3)
                print("\t【%s】 ————> %s/%s.txt" % (sChapterTitle, sType, sTitle))

        if not lstAllUrl:
            self.FinishDownlandBook(bookurl)


    def FinishDownlandBook(self, bookurl):
        dBookInfo = self.m_DoneInfo[bookurl]
        sTitle = dBookInfo.get("title", "")
        dNewBookInfo = {
            "statue"                :True,
            "latest_chapter_url"    :dBookInfo["latest_chapter_url"],
            "title"                 :sTitle
        }
        self.m_DoneInfo[bookurl] = dNewBookInfo
        print("《%s.txt》 下载完毕" % sTitle)

