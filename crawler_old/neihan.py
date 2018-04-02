# -*- coding -*-

from pubdefine import *

import urllib.request
import bs4
import json

class CNeiHan(object):

	m_OtherInfoFile	="neihan/otherinfo.xh"
	m_NeiHanFile	="neihan/neihan.txt"
	m_Url			="http://neihanshequ.com/"

	def __init__(self):
		self.m_OtherInfo={}	#id:(点赞,倒彩,收藏,分享,评论)


	def LoadOtherInfo(self):
		with codecs.open(self.m_OtherInfoFile,"rb") as fd:
			sMsg=fd.readline()


	def SaveOtherInfo(self):
		sMsg=json.dumps(self.m_OtherInfo)
		with open(self.m_OtherInfoFile,"w") as fd:
			fd.write(sMsg)


	def GetData(self):
		oResponse=urllib.request.urlopen(self.m_Url)
		oBS4=bs4.BeautifulSoup(oResponse,"html.parser")
		for oDiv in oBS4.findAll("div",class_="options"):
			if not "data-group-id" in oDiv.attrs:
				continue
			sID=oDiv.attrs["data-group-id"]
			iID=int(sID)
			if iID in self.m_OtherInfo:
				continue
			oUL=oDiv.ul
			iDigg=int(oUL.find("span",class_="digg").get_text())	#点赞
			iBury=int(oUL.find("span",class_="bury").get_text())	#倒赞
			iRepin=int(oUL.find("span",class_="repin").get_text())	#收藏
			iShare=int(oUL.find("span",class_="share").get_text())	#分享
			iComment=int(oUL.find("span",class_="comment J-comment-count").get_text())	#评论
			sContext=oUL.find("li",class_="share-wrapper right")["data-text"]
			self.m_OtherInfo[iID]=(iDigg,iBury,iRepin,iShare,iComment)
			# sContext="%s %s"%(iID,sContext)
			LogFile(self.m_NeiHanFile,sContext)
