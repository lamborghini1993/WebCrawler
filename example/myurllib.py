# -*- coding: utf-8 -*-
# 肖豪

import socket
import json

import urllib.request
import urllib.parse


url = "http://www.python.org/"

# 1.最简单的方式
# socket.setdefaulttimeout(2)	#设置超时时间
# req = urllib.request.Request(url)
# response = urllib.request.urlopen(req)
# html = response.read().decode("utf8")
# print(html)

# 2.使用Request
# req = urllib.request.Request(url)
# response = urllib.request.urlopen(req)
# html = response.read()
# print(html)

# 3.发送数据，模拟登陆keep,POST数据
"""
Host: www.gotokeep.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Referer: https://www.gotokeep.com/login?next=https%3A%2F%2Fwww.gotokeep.com%2F
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 66
Connection: keep-alive

解决 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte
Accept-Encoding: gzip, deflate, br
这条信息代表本地可以接收压缩格式的数据，而服务器在处理时就将大文件压缩再发回客户端，
IE在接收完成后在本地对这个文件又进行了解压操作。
出错的原因是因为你的程序没有解压这个文件，所以删掉这行就不会出现问题了。
看来header不能随便复制过来啊
"""

# headers = {
# 	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
# 	"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
# 	"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
# 	"X-Requested-With": "XMLHttpRequest",
# }
# values = {
# 	"countryCode":	86,
# 	"countryName":	"",	
# 	"mobile"	:	"15671628437",
# 	"password"	:	"xxxxxx",
# }
# url = "https://www.gotokeep.com/login?next=https%3A%2F%2Fwww.gotokeep.com%2F"
# # Post的数据必须是bytes或者iterable of bytes，不能是str，因此需要进行encode（）编码
# data = urllib.parse.urlencode(values).encode(encoding='utf8')
# req = urllib.request.Request(url, data=data, headers=headers)
# response = urllib.request.urlopen(req)
# html = response.read().decode("utf8")
# dData = json.loads(html)
# print(dData)


# 4.http错误处理
# req = urllib.request.Request(url)
# try:
# 	urllib.request.urlopen(req)
# except urllib.error.HTTPError as e:
# 	print(e.code)

# 5.http认证
# # 创建一个密码管理器
# password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
# # 添加账号密码到管理器中,如果知道realm，可以不为空
# password_mgr.add_password(None, url, "rekfan", "xxxxxx")
# handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
# # 创建一个opener
# opener = urllib.request.build_opener(handler)
# # 使用opener匹配一个url
# tmp = opener.open(url)
# print(tmp.read())

# # 安装opener
# urllib.request.install_opener(opener)
# # 下面只需要使用urllib.request.urlopen操作opener即可
# response = urllib.request.urlopen(url)
# html = response.read().decode("utf8")
# print(html)


# 6.使用代理
# proxy_support = urllib.request.ProxyHandler({"sock5":"localhost:1080"})
# opener = urllib.request.build_opener(proxy_support)
# urllib.request.install_opener(opener)
# # 下面只需要使用urllib.request.urlopen操作opener即可
# response = urllib.request.urlopen(url)
# html = response.read().decode("utf8")
# print(html)






