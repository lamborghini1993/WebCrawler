# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-01 11:43:36
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-01 11:43:36
"""

import os

from crawler import meizitu
from crawler import zww35
from crawler import shubao888

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
    # obj = meizitu.MyCrawler()
    obj = zww35.CZww35()
    obj.Start()


if __name__ == "__main__":
    start()
