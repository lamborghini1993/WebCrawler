# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-04 15:22:59
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-04 15:22:59
@Desc:
    http://haowuya.cc/laosiji/wdz/
    爬取污段子
"""

import basecrawler


class WuDuanZi(basecrawler.CWebCrawler):
    url = "http://haowuya.cc/laosiji/wdz/"

    def start(self):
        bs4obj = self.get_bs4_by_url(self.url)
        