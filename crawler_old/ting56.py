# -*- coding:utf8 -*-

"""
爬取听书网的有声小说
http://www.ting56.com/
http://audio.xmcdn.com/group7/M07/27/7C/wKgDWlWDF5ySxXMgAFq-KbQ32ww177.m4a
http://audio.xmcdn.com/group14/M06/44/06/wKgDY1WlPoaTpABlAF0WxaapayE059.m4a
"""

from pubdefine import *

import urllib.request
import webcrawler
import re
import codecs

class CTing56(webcrawler.CWebCrawler):
    m_Url = "http://www.ting56.com/video/1480-0-"
    m_Save = "H:\\audiobook\\ting56"
    m_SaveDir = "audiobook/"

    def __init__(self):
        super(CTing56, self).__init__()
        self.m_PageNum = 1

    def Start(self):
        self.ParesUrl()

    def ParesUrl(self):
        for x in range(self.m_PageNum):
            sUrl = self.m_Url + "%s.html" % x
            self.Fuck(sUrl)
            return
            oBS4 = self.GetDataByUrl(sUrl)
            print("准备下载 url:{}".format(sUrl))
            self.DownloadMP3(oBS4)


    def Fuck(self, sUrl):
        dHeard = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            "Cookie":"adv=2; UM_distinctid=15ed0bc814ae7-0552aacb90f8d1-3e63430c-15f900-15ed0bc814b8df; ASPSESSIONIDAAQABTAB=OLIHJNGDPAHGFNMMNDHKFJNH; adv=1; CNZZDATA3055531=cnzz_eid%3D1351153717-1506737472-http%253A%252F%252Fwww.ting56.com%252F%26ntime%3D1506748272; Hm_lvt_f48885d046488759be0f43cb09d34403=1506740568; Hm_lpvt_f48885d046488759be0f43cb09d34403=1506749755; max_cms4_v=%u300A%u5949%u5B50%u6210%u5A5A%u300B%20%u7B2C1%u96C6^http%3A//www.ting56.com/video/1480-0-0.html_$_|,",
            "Referer":"http://www.ting56.com/mp3/1480.html",
            "Upgrade-Insecure-Requests":1,
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Connection":"keep-alive",
        }
        # sData = urllib.parse._encode_result()
        sUrl = "http://ting456.b0.upaiyun.com/15/金鳞岂是池中物?01.mp3"
        oReq = urllib.request.Request(sUrl, headers=dHeard)
        print(oReq)
        return
        # oResponse=urllib.request.urlopen(sUrl,timeout=iTimeout)
        sData = urllib.request.urlopen(oReq).read()
        with open("audiobook/xh.html","wb+") as fd:
            fd.write(sData)

    def DownloadMP3(self, oBS4):
        # oB = oBS4.findAll("audio", src=re.compile("http://audio.*m4a"))
        # print(oBS4)
        with open("audiobook/xh.html","wb+") as fd:
            fd.write(oBS4)

def Init():
    obj = CTing56()
    obj.Start()