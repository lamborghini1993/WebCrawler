# -*- coding: utf-8 -*-

from pubdefine import *

import urllib.request
import webcrawler
import re

class CXieEGIF(webcrawler.CWebCrawler):

	m_Url		="http://www.duzhebao.com/dongtaitu/xiee/"
	m_SaveDir	="F:\\code\\WebCrawler\\xiee\\xiee\\"

	def __init__(self):
		super(CXieEGIF,self).__init__()
		self.m_PageNum=99


	def Start(self):
		super(CXieEGIF,self).Start()
		self.StartDownload()
		self.Done()

	def StartDownload(self):
		for x in range(8,self.m_PageNum):
			sUrl=self.m_Url+"%s.htm"%x
			oBS4=self.GetBS4ByUrl(sUrl)
			print("准备下载第{}页gif url:{}".format(x,sUrl))
			bTrue=self.DownloadGIF(oBS4)
			if not bTrue:
				break


	def DownloadGIF(self,oBS4):
		lstImg=oBS4.findAll("img",src=re.compile("http://123.duzhebao.com/.*"))
		lstName=oBS4.findAll("div",class_="hd")
		if not lstImg:
			return False
		if len(lstImg)!=len(lstName):
			print(len(lstImg))
			print(len(lstName))
			raise Exception("长度不一样")
		for x in range(len(lstImg)):
			oImg=lstImg[x]
			oDiv=lstName[x]
			if not oImg or not oDiv:
				return False
			sGifUrl=oImg["src"]
			sName=oDiv.get_text()
			if sGifUrl in self.m_SaveInfo:
				continue
			for s in ["?","？"," "]:
				sName=sName.replace(s,"")
			sFileName=self.m_SaveDir+sName+".gif"
			urllib.request.urlretrieve(sGifUrl,sFileName)
			self.m_SaveInfo[sGifUrl]=1
			print("\t{}\t下载完成...".format(sName))
		return True
