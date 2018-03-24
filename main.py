# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-01 11:43:36
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-01 11:43:36
"""

import os

from budejie import text
from haowuya import wuduanzi
from meizitu import meizitu
from xiaoshuo import zww35
from movie import imdb250
from other import dp2980

__version__ = "trunk"

def InitPubCode():
    if os.path.exists("pubcode"):
        return
    sPwd = os.getcwd()
    sPubCode = os.path.join(sPwd, "..\pubcode", __version__)
    sCode = os.path.join(sPwd, "pubcode")
    sCmd = "mklink /j %s %s" % (sCode, sPubCode)
    os.system(sCmd)


def start():
    InitPubCode()
    # obj = text.CText()
    # obj = wuduanzi.WuDuanZi()
    # obj = dp2980.CDP2980()
    # obj.start()
    # obj.resource()


if __name__ == "__main__":
    start()
