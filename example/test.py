# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
phantomjs_path = r"F:\pythonlib\phantomjs-2.1.1-windows\bin\phantomjs.exe"
driver = webdriver.PhantomJS(executable_path=phantomjs_path)
url = 'http://blog.csdn.net/jiajia_han/article/details/70810306'
driver.get(url)
#轻松得到到JS渲染页面的源码
page_source = driver.page_source.encode('utf8')
print(page_source)
