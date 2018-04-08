# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-02 21:08:30
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-02 21:08:30
@Desc:
"""

import os

PATH = r"E:\mygithub\WebCrawler\Downloads\zww35"

def DFSReName(path):
    for sFile in os.listdir(path):
        sNextPath = os.path.join(path, sFile)
        if os.path.isfile(sNextPath):
            if sNextPath.find("全文阅读") != -1:
                sNewFile = sNextPath.replace("全文阅读", "")
                print(sNextPath)
                print("\t——>", sNewFile)
                os.rename(sNextPath, sNewFile)
        else:
            DFSReName(sNextPath)

if __name__ == "__main__":
    DFSReName(PATH)

