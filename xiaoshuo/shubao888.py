# -*- coding:utf8 -*-
# 第二书包
# 网站链接 http://www.shubao888.com/xiaoshuo/6/1.html

from pubdefine import *

import urllib.request
import bs4
import re
import time

TIMEOUT = 10

class CShuBao888(object):

	m_File = "F:\\document\\novel"
	m_Url = "http://www.shubao888.com"
	m_InfoName = GetCWD() + "\\xiaoshuo\\info.xh"

	def __init__(self):
		self.m_PageUrl = {}
		self.m_AllUrlInfo = {}	#{sType:{url:xxx,name:xxx}}
		self.m_DownloadInfo = {}	#{name:newchater}

	def Start(self):
		self.m_DownloadInfo = LoadBookInfo(self.m_InfoName)
		self.GetAllPageUrl()
		self.GetAllUrlInfo()
		self.DownloadAllBook()

	def GetBSByUrl(self, sUrl):
		while True:
			try:
				oResponse = urllib.request.urlopen(sUrl, timeout=TIMEOUT)
				oBS4 = bs4.BeautifulSoup(oResponse, "html.parser")
			except:
				print("\t获取({})超时,重新获取...".format(sUrl))
				continue
			return oBS4

	def GetAllPageUrl(self):
		self.m_PageUrl["/xiaoshuo/6/1.html"] = "辣文肉文"
		return
		oBS4 = self.GetBSByUrl(self.m_Url)
		for oA in oBS4.findAll("a", href=re.compile("^/[a-z\\]*/[1-9]*.html$")):
			sUrl = oA["href"]
			sType = oA.get_text()
			self.m_PageUrl[sUrl] = sType

	def GetAllUrlInfo(self):
		for sUrl, sType in self.m_PageUrl.items():
			print("获取url:({}) 类型:({})".format(sUrl, sType))
			self.m_AllUrlInfo[sType] = {}
			self.GetOneTypeInfo(sUrl, self.m_AllUrlInfo[sType])

	def GetOneTypeInfo(self, sUrl, dInfo):
		sUrl = self.m_Url + sUrl
		oBS4 = self.GetBSByUrl(sUrl)
		iNum = self.GetPageNum(oBS4)
		sHeadUrl = self.GetUrlHead(sUrl)
		for x in range(1, iNum + 1, 1):
			sUrl = sHeadUrl + "%s.html" % x
			print("开始获取第{}页url:{}".format(x, sUrl))
			self.GetOnePageInfo(sUrl, dInfo)

	def GetOnePageInfo(self, sUrl, dInfo):
		oBS4 = self.GetBSByUrl(sUrl)
		for oSpan in oBS4.findAll("span", class_="s2"):
			oA = oSpan.a
			sUrl = oA["href"]
			sName = oA.get_text()
			if sName in dInfo:
				continue
			dInfo[sName] = sUrl
			print("获取书名:({}) 地址:({})".format(sName, sUrl))

	def GetPageNum(self, oBS4):
		oEM = oBS4.find("em", id="pagestats")
		sPage = oEM.get_text()
		lstTmp = sPage.split("/")
		iNum = int(lstTmp[1])
		return iNum

	def GetUrlHead(self, sUrl):
		iIndex = sUrl.rfind("/")
		sHeadUrl = sUrl[:iIndex + 1]
		return sHeadUrl

	def DownloadAllBook(self):
		for sType, dInfo in self.m_AllUrlInfo.items():
			for sName, sUrl in dInfo.items():
				self.DownloadBook(sUrl, sType, sName)

	def DownloadBook(self, sUrl, sType, sName):
		sFileName = "%s\\%s\\%s.txt" % (self.m_File, sType, sName)
		print("准备下载:({}) 类型:({}) 地址({})...".format(sName, sType, sUrl))
		oBS4 = self.GetBSByUrl(sUrl)
		for oDD in oBS4.findAll("dd"):
			if not hasattr(oDD, "a"):
				continue
			oA = oDD.a
			if not oA:
				continue
			sChapter = oA["href"]
			sTitle = oA["title"]
			sChapterUrl = sUrl + sChapter
			iChapter = self.GetChapterNum(sChapter)
			if sName in self.m_DownloadInfo:
				a, b, c = self.m_DownloadInfo[sName]
				if iChapter <= a:
					continue
			self.DownloadOneChapter(sChapterUrl, sFileName, sTitle)
			self.m_DownloadInfo[sName] = (iChapter, sTitle, sChapterUrl)
			SaveBookInfo(self.m_InfoName, self.m_DownloadInfo)
		print("下载完毕:({})\n".format(sName, sType))

	def GetChapterNum(self, sChapter):
		lstTmp = sChapter.split(".")
		sNum = lstTmp[0]
		iNum = int(sNum)
		return iNum

	def DownloadOneChapter(self, sUrl, sFileName, sTitle):
		oBS4 = self.GetBSByUrl(sUrl)
		oDiv = oBS4.find("div", id="content")
		sText = oDiv.get_text()
		sChapter = "%s\n%s\n\n" % (sTitle, sText)
		sChapter = sChapter.replace("    ", "\n")
		WriteFile(sFileName, sChapter)
		print("\t章节:({}) 地址({}) 下载完毕...".format(sTitle))

	# def DownloadAllType(self):
	# 	for sUrl,sType in self.m_PageUrl.items():
	# 		self.DownloadOneType(sUrl,sType)
	#
	#
	# def DownloadOneType(self,sUrl,sType):
	# 	sUrl=self.m_Url+sUrl
	# 	print("准备下载{}类型小说".format(sType))
	# 	oBS4=self.GetBSByUrl(sUrl)
	# 	iNum=self.GetPageNum(oBS4)
	# 	sHeadUrl=self.GetUrlHead(sUrl)
	# 	for x in range(1,iNum+1,1):
	# 		sUrl=sHeadUrl+"%s.html"%x
	# 		self.DownloadOnePage(sUrl,sType)
	#
	#
	# def DownloadOnePage(self,sUrl,sType):
	# 	print("{} {}".format(sUrl,sType))
	# 	oBS4=self.GetBSByUrl(sUrl)
	# 	for oSpan in oBS4.findAll("span",class_="s2"):
	# 		oA=oSpan.a
	# 		sUrl=oA["href"]
	# 		sName=oA.get_text()
	# 		self.DownloadBook(sUrl,sType,sName)
