# -*- coding:utf-8 -*-
# 肖豪
# 获取JS渲染页面之后的源码


"""
1.使用到selenium库
2.使用了phantomjs.exe工具
"""

# import re

# info = '-----<span class="time">[--]</span>-------'
# zf = r'<span class="time">\[(.*?)\]</span>'

# zftime = r'<span class="zf(.*?)">(.*?)</span>'
# mm = re.search(zf, info)
# print(mm.group(1))

import re
import codecs
from selenium import webdriver

phantomjs_path = r"F:\pythonlib\phantomjs-2.1.1-windows\bin\phantomjs.exe"
driver = webdriver.PhantomJS(executable_path=phantomjs_path)
url = 'http://blog.csdn.net/jiajia_han/article/details/70810306'
url = "http://fund.10jqka.com.cn/001542/"
driver.get(url)
# 轻松得到到JS渲染页面的源码    估值涨幅
page_source = driver.page_source.encode('utf8')
# 输出渲染过后的html
# print(driver)
# print(dir(driver))
# print(driver.find_elements_by_name("zf f-up"))

title = r'<title>(.*?)</title>'
zf = r'<span class="time">\[(.*?)\]</span>'
zftime = r'<span class="zf(.*?)">(.*?)</span>'
page_source = page_source.decode("utf8")
pattern = re.compile(zftime)
with codecs.open("test.html", "w", "utf-8") as myfile:
    myfile.write(page_source)
m1 = pattern.search(page_source)
if m1:
    print(m1.group(1))
else:
    print("---------")

# page_source = page_source.decode("utf8")
# print("page_source")
