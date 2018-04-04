# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-04-02 20:28:07
@Desc: 
"""

import os
import asyncio
import aiohttp

from pubcode import misc


class CPubCrawler(object):
    m_Flag = ""
    m_MaxNum = 10
    m_Encoding = "utf-8"
    m_WaitingUrl = set()
    m_ReadyUrl = set()
    m_DoingUrl = set()

    m_WrongChar = r"<>/|:\"*?"
    m_ConfigDir = "Config"
    m_DownDir = "Downloads"
    m_headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':'gb2312,utf-8',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection':'Keep-alive'
    }

    def __init__(self):
        self.m_Run = True
        self.m_Loop = asyncio.get_event_loop()
        self.m_DownInfo = {}
        self._Init()
        self._CustomInit()


    def _Init(self):
        self.m_DownPath = os.path.join(os.getcwd(), self.m_DownDir, self.m_Flag)
        self.m_ConfigPath = os.path.join(os.getcwd(), self.m_ConfigDir, self.m_Flag)
        for sDirPath in (self.m_DownPath, self.m_ConfigPath):
            if not os.path.exists(sDirPath):
                os.makedirs(sDirPath)
        self.m_DownInfoPath = os.path.join(self.m_ConfigPath, "downland.json")


    def _CustomInit(self):
        pass


    def _Load(self):
        self.m_DownInfo = misc.JsonLoad(self.m_DownInfoPath, {})


    def _Save(self):
        misc.JsonDump(self.m_DownInfo, self.m_DownInfoPath)


    def Start(self):
        # try:
        self.m_Loop.run_until_complete(self.Run())
        self.m_Loop.close()
        # except Exception as e:
        #     print(e)
        #     self._Save()


    def _Replace(self, sMsg, default="_"):
        for char in self.m_WrongChar:
            if sMsg.find(char) == -1:
                continue
            sMsg = sMsg.replace(char, default)
        return sMsg

    def Print(self, msg):
        # return
        print(msg, len(self.m_WaitingUrl), len(self.m_ReadyUrl), len(self.m_DoingUrl))

    def NewCrawel(self):
        self.m_WaitingUrl = set(sorted(self.m_WaitingUrl, key=lambda x: x[1], reverse=True))
        self.Print("1")
        # while (len(self.m_ReadyUrl) + len(self.m_DoingUrl)) < self.m_MaxNum and self.m_WaitingUrl:
        while (len(self.m_ReadyUrl) ) < self.m_MaxNum and self.m_WaitingUrl:
            self.m_ReadyUrl.add(self.m_WaitingUrl.pop())
            self.Print("2")
        return True


    async def Run(self):
        async with aiohttp.ClientSession() as self.m_Session:
            # while self.NewCrawel() and (len(self.m_ReadyUrl) + len(self.m_DoingUrl)):
            while self.NewCrawel() and (len(self.m_WaitingUrl) + len(self.m_ReadyUrl)):
                self.Print("3")
                if not self.m_ReadyUrl:
                    await asyncio.sleep(0.1)
                    continue

                # tasks = []
                # for tInfo in self.m_ReadyUrl:
                #     oTask = self.m_Loop.create_task(self.Crawl(tInfo))
                #     tasks.append(oTask)
                #     self.m_DoingUrl.add(tInfo)

                tasks = [self.m_Loop.create_task(self.Crawl(tInfo)) for tInfo in self.m_ReadyUrl]

                self.m_DoingUrl.update(self.m_ReadyUrl)
                self.m_ReadyUrl.clear()

                finished, unfinished = await asyncio.wait(tasks)
                if unfinished:
                    print("="*20, unfinished)
                htmls = [f.result() for f in finished]
                for html, tInfo in htmls:
                    await self.Parse(html, tInfo)
            self._Save()


    async def Crawl(self, tInfo):
        url, *args = tInfo
        r = await self.m_Session.get(url, headers=self.m_headers)
        html = await r.text(encoding=self.m_Encoding)
        return html, tInfo


    async def Parse(self, html, url):
        self.m_ReadyUrl.remove(url)
