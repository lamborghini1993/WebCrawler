# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-02 21:08:30
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-02 21:08:30
@Desc:
"""

import aiohttp
import asyncio
import os

from pubcode import misc

class ShowPicture():
    m_WrongChar = r"<>/|:\"*?"
    m_headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':'gb2312,utf-8',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection':'Keep-alive'
    }
    m_Save = "Downloads/meizitu"

    def __init__(self):
        self.m_Info = {}

    def ChangeWrongChat(self, txt, default="_"):
        bHas = False
        for char in self.m_WrongChar:
            if txt.find(char) == -1:
                continue
            bHas = True
            txt = txt.replace(char, default)
        return bHas, txt

    def Start(self):
        dInfo = misc.JsonLoad("Downloads/meizitu_urlinfo.json", {})
        for _, dOther in dInfo.items():
            for url, sName in dOther.items():
                bHas, sTT = self.ChangeWrongChat(sName)
                if not bHas:
                    continue
                dOther[url] = sTT
        misc.JsonDump(dInfo, "Downloads/meizitu_urlinfo.json")
        # self.m_Loop = asyncio.get_event_loop()
        # self.m_Loop.run_until_complete(self.Downloads())
        # self.m_Loop.close()


    async def Downloads(self):
        async with aiohttp.ClientSession() as self.m_Session:
            while len(self.m_Info):
                for url, name in self.m_Info.items():
                    await self.DownPictur(name, url)

    async def DownPictur(self, name, url):
        r = await self.m_Session.get(url, headers=self.m_headers)
        picdata = await r.read()
        await self.dowland_pic(name, picdata, url)


    async def dowland_pic(self, filename, picdata, url):
        filepath = os.path.join(self.m_Save, filename)
        if os.path.exists(filepath):
            return
        print("dowland_pic %s" % (filename))
        with open(filepath, "wb") as fpic:
            fpic.write(picdata)
        if url in self.m_Info:
            del self.m_Info[url]


obj =  ShowPicture()
obj.Start()
