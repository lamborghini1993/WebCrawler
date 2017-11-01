# -*- coding -*-
#从花椒网上面爬出在线直播的女神id列表

from pubdefine import *

import urllib.request
import re
import bs4


class CWebData(object):

	m_BaseUrl	="http://www.huajiao.com"
	m_SearchUrl=["/category/2","/category/999"]

	def __init__(self):
		self.m_AllGirlUrl=set()
		self.m_AllGirlIDS=set()


	def Start(self):
		self.GetAllGirlUrl()
		self.GetAllLiveIDS()
		self.Fuck()


	def GetAllGirlUrl(self):
		"""获取所以女神驾到的url地址"""
		for sEndUrl in self.m_SearchUrl:
			sUrl=self.m_BaseUrl+sEndUrl
			oResponse=urllib.request.urlopen(sUrl)
			oBS4=bs4.BeautifulSoup(oResponse,"html.parser")
			for sLink in oBS4.findAll("a",href=re.compile(sUrl)):
				if "href" in sLink.attrs:
					sGirlUrl=sLink.attrs['href']
					self.m_AllGirlUrl.add(sGirlUrl)


	def GetAllLiveIDS(self):
		"""获取在线直播的女神驾到id列表"""
		for sUrl in self.m_AllGirlUrl:
			# print(sUrl)
			oResponse=urllib.request.urlopen(sUrl)
			oBS4=bs4.BeautifulSoup(oResponse,"html.parser")
			for sLink in oBS4.findAll("a",href=re.compile("^(/l/)")):
				if "href" in sLink.attrs:
					newPage=sLink.attrs['href']
					liveId=re.findall("[0-9]+", newPage)
					self.m_AllGirlIDS.add(liveId[0])

	def Fuck(self):
		print(len(self.m_AllGirlUrl))
		print(len(self.m_AllGirlIDS))

obj=CWebData()
obj.Start()
