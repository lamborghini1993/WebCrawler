# -*- coding -*-
#百思不得其姐段子

import urllib.request

import bs4

class CLove(object):

	m_Url	="http://www.budejie.com/"

	def GetData(self):
		lstAttr=["href","class",""]
		oResponse=urllib.request.urlopen(self.m_Url,timeout=55)
		oBS4=bs4.BeautifulSoup(oResponse,"html.parser")
		for sLink in oBS4.findAll("ls"):
			# if not "date-text" in sLink:
			# 	continue
			print(sLink)
			# sID=sLink.attrs["date-group-id"]
			# print(sID)
			return

obj=CLove()
obj.GetData()
