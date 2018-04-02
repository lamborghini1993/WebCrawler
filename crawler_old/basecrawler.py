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
from pubcode import pubdefines


class CWebCrawler(object):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"
    }
    max_try_num = 10
    timeout = 10
    logdir = "tmp"

    def log(self, msg):
        pubdefines.write_to_file(self.logdir + "/log", msg)

    def done(self):
        print("\n全部下载完毕。。")

    def get_bs4_by_url(self, url, timeout=timeout):
        for num in range(1, self.max_try_num):
            try:
                req = urllib.request.Request(url, headers=self.headers)
                response = urllib.request.urlopen(req, timeout=timeout)
                bs4obj = bs4.BeautifulSoup(
                    response, "html.parser", from_encoding="gbk")
                return bs4obj
            except:
                pass
        self.log("{}次 尝试获取失败 {}".format(num, url))
        return None

    def get_data_by_url(self, url, timeout=timeout):
        for num in range(1, self.max_try_num):
            try:
                req = urllib.request.Request(url, headers=self.headers)
                response = urllib.request.urlopen(req, timeout=timeout)
                data = response.read()
                return data
            except:
                pass
        self.log("{}次 尝试获取失败 {}".format(num, url))
        return None
