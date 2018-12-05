# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-01 11:43:36
"""


def start():
    # from crawler import meizitu
    # obj = meizitu.MyCrawler()

    # from crawler import zww35
    # obj = zww35.CZww35()

    from crawler import hdu
    obj = hdu.HDU()

    obj.Start()


if __name__ == "__main__":
    start()
