# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-01 11:43:36
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-01 11:43:36
"""

from budejie import text
from haowuya import wuduanzi
from meizitu import meizitu


def start():
    # obj = text.CText()
    # obj = wuduanzi.WuDuanZi()
    obj = meizitu.MeiZiTu()
    obj.start()
    # obj.resource()


if __name__ == "__main__":
    start()
