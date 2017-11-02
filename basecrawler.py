# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-02 16:03:23
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-02 16:03:23
@Desc:
    爬虫基类
"""


import urllib.request
import bs4


class CWebCrawler(object):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) \
            Gecko/20100101 Firefox/57.0"
    }

    def done(self):
        print("\n全部下载完毕。。")

    def get_bs4_by_url(self, sUrl, timeout=10):
        num = 0
        while True:
            num += 1
            try:
                req = urllib.request.Request(sUrl, headers=self.headers)
                response = urllib.request.urlopen(req, timeout=timeout)
                bs4obj = bs4.BeautifulSoup(response, "html.parser")
                return bs4obj
            except Exception as err:
                print("\t第{}次开始尝试获取失败{}--{}".format(num, sUrl, err))

    def get_data_by_url(self, sUrl, timeout=10):
        response = urllib.request.urlopen(sUrl, timeout=timeout)
        data = response.read()
        return data
