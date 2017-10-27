# -*- coding:utf-8 -*-
# 肖豪

import urllib.request

sUrl = "http://123.ygdppt.com/365/2017/yqt/jlqsczw/%E9%87%91%E9%B3%9E%E5%B2%82%E6%98%AF%E6%B1%A0%E4%B8%AD%E7%89%A9002.mp3"

# 爬取url上面的内容保存为xxx.mp3
urllib.request.urlretrieve(sUrl, "xxx.mp3")
