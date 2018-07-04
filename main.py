# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-01 11:43:36
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-01 11:43:36
"""

import os


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
    # from crawler import meizitu
    # obj = meizitu.MyCrawler()

    # from crawler import zww35
    # obj = zww35.CZww35()

    from crawler import hdu
    obj = hdu.HDU()
    obj.Start()


if __name__ == "__main__":
    start()
