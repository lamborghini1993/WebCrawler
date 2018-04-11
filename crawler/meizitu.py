# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-03-30 10:42:20
@Desc: 
"""
import aiohttp
import asyncio
import time
import os
from bs4 import BeautifulSoup
from urllib.request import urljoin, urlretrieve
import re
import multiprocessing as mp

from pubcode import pubdefines, misc

class MyCrawler(object):

    m_Flag = "meizitu"
    m_ConfigDir = "Config"
    m_DownDir = "Downloads"

    m_Headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':'gb2312,utf-8',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection':'Keep-alive'
    }
    m_MaxNum = 10
    m_DelChar = [" | 妹子图", "（一）", "（二）", "？"]
    m_WrongChar = r"<>/|:\"*?"

    def __init__(self):
        self.m_Page = 1
        self.m_MaxPage = 3	#8888
        self.m_Seen = set()
        self.m_Unseen = set()
        self.m_Loop = asyncio.get_event_loop()
        self.m_DownInfo = {}
        self.m_PicNameInfo = {}
        self._Init()
        self._Load()


    def _Init(self):
        self.m_DownPath = os.path.join(os.getcwd(), self.m_DownDir, self.m_Flag)
        self.m_ConfigPath = os.path.join(os.getcwd(), self.m_ConfigDir, self.m_Flag)
        for sDirPath in (self.m_DownPath, self.m_ConfigPath):
            if not os.path.exists(sDirPath):
                os.makedirs(sDirPath)
        self.m_UrlInfoPath = os.path.join(self.m_ConfigPath, "urlinfo.json")
        self.m_NameInfoPath = os.path.join(self.m_ConfigPath, "name.json")


    def _Load(self):
        self.m_DownInfo = misc.JsonLoad(self.m_UrlInfoPath, {})
        self.m_PicNameInfo = misc.JsonLoad(self.m_NameInfoPath, {})


    def _Save(self):
        misc.JsonDump(self.m_DownInfo, self.m_UrlInfoPath)
        misc.JsonDump(self.m_PicNameInfo, self.m_NameInfoPath)


    def Start(self):
        try:
            self.m_Loop.run_until_complete(self.Run())
            self.m_Loop.close()
        except Exception as e:
            print(e)
            self._Save()


    def ChangeWrongChat(self, txt, default="_"):
        for char in self.m_WrongChar:
            if txt.find(char) == -1:
                continue
            txt = txt.replace(char, default)
        return txt


    def AddUrl(self):
        while self.m_Page < self.m_MaxPage and len(self.m_Unseen) < self.m_MaxNum:
            url = "http://www.meizitu.com/a/%s.html" % str(self.m_Page)
            self.m_Unseen.add(url)
            self.m_Page += 1
        return True


    async def Run(self):
        async with aiohttp.ClientSession() as self.m_Session:
            while self.AddUrl():
                if not self.m_Unseen:
                    await asyncio.sleep(0.1)
                    continue
                tasks = [self.m_Loop.create_task(self.Crawl(url)) for url in self.m_Unseen]
                finished, unfinished = await asyncio.wait(tasks)
                htmls = [f.result() for f in finished]
                for html, url in htmls:
                    await self.Parse(html, url)
                if self.m_Page >= self.m_MaxPage:
                    self._Save()


    async def Crawl(self, url):
        print("Crawl:", url)
        r = await self.m_Session.get(url, allow_redirects=False, headers=self.m_Headers)
        html = await r.text(encoding="gbk")
        self.m_Seen.add(url)
        self.m_Unseen.remove(url)
        return html, url


    async def Parse(self, html, url):
        soup = BeautifulSoup(html, 'lxml')
        for odiv in soup.findAll("div", id="picture") or soup.findAll("div", class_="postContent"):
            oop = odiv.p
            for oimg in oop.findAll("img"):
                src = oimg.get("src")
                filename = self._GetPicName(soup, html, oimg)
                await self.DownPictur(filename, src, url)


    def _Replace(self, sMsg, default="_"):
        for tmp in self.m_DelChar:
            sMsg = sMsg.replace(tmp, "")
        for char in self.m_WrongChar:
            if sMsg.find(char) == -1:
                continue
            sMsg = sMsg.replace(char, default)
        return sMsg


    def _GetPicName(self, soup, html, oimg):
        src = oimg.get("src")
        suffix = src.split(".")[-1]
        title = soup.title.text
        title = self._Replace(title)

        iNum = self.m_PicNameInfo.setdefault(title, 1)
        self.m_PicNameInfo[title] = iNum + 1

        filename = title + "_" + str(iNum) + "." + suffix
        return filename


    async def DownPictur(self, filename, picurl, url):
        r = await self.m_Session.get(picurl, headers=self.m_Headers)
        picdata = await r.read()
        await self.dowland_pic(filename, picdata, picurl, url)


    async def dowland_pic(self, filename, picdata, picurl, url):
        filepath = os.path.join(self.m_DownPath, filename)
        if os.path.exists(filepath):
            return
        print("%s ——> %s" % (picurl, filename))
        with open(filepath, "wb") as fpic:
            fpic.write(picdata)
        dInfo = self.m_DownInfo.setdefault(url, {})
        dInfo[picurl] = filename
