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
    max_try_num = 10
    timeout = 10

    def done(self):
        print("\n全部下载完毕。。")

    def get_bs4_by_url(self, url, timeout=timeout):
        for num in range(1, self.max_try_num):
            try:
                req = urllib.request.Request(url, headers=self.headers)
                response = urllib.request.urlopen(req, timeout=timeout)
                bs4obj = bs4.BeautifulSoup(response, "html.parser")
                return bs4obj
            except Exception as err:
                print("\t第{}次开始尝试获取失败{}--{}".format(num, url, err))
        return None

    def get_data_by_url(self, url, timeout=timeout):
        response = urllib.request.urlopen(url, timeout=timeout)
        data = response.read()
        return data
