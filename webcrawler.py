# -*- coding: utf-8 -*-

from pubdefine import *

import urllib.request
import bs4


class CWebCrawler(object):

    m_SaveDir = ""

    def __init__(self):
        self.m_SaveInfo = {}

    def Start(self):
        if not self.m_SaveDir:
            raise Exception("未初始化savefile")
            return
        self.m_SaveFile = self.m_SaveDir + "info.xh"
        self.Load()
        self.CustomStart()

    def CustomStart(self):
        pass

    def Load(self):
        self.m_SaveInfo = Load4File(self.m_SaveFile)

    def Save(self):
        Save2File(self.m_SaveFile, self.m_SaveInfo)

    def Done(self):
        print("\n全部下载完毕。。")

    def GetBS4ByUrl(self, sUrl, iTimeout=10):
        iNum = 0
        while True:
            try:
                oResponse = urllib.request.urlopen(sUrl, timeout=iTimeout)
                oBS4 = bs4.BeautifulSoup(oResponse, "html.parser")
                return oBS4
            except:
                print("\t第{}次开始尝试获取失败{}".format(iNum, sUrl))

    def GetDataByUrl(self, sUrl, iTimeout=10):
        oResponse = urllib.request.urlopen(sUrl, timeout=iTimeout)
        sData = oResponse.read()
        return sData
