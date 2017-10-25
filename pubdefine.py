# -*- coding: utf-8 -*-

import codecs
import sys
import os
import time
import json

class COutput(object):
	def __init__(self):
		self.m_Console=sys.stdout

	def write(self,sMsg):
		try:
			# sMsg=sMsg.encode("utf8").decode("gbk")
			self.m_Console.write(sMsg)
		except:
			self.m_Console.write("\t----错误编码----")

	def flush(self):
		pass


def WriteFile(sFileName,sMsg):
	iIndex=sFileName.rfind("\\")
	sBegin=sFileName[:iIndex]
	sEnd=sFileName[iIndex:]
	if not os.path.exists(sBegin):
		os.makedirs(sBegin)
	with codecs.open(sFileName,"a","utf-8") as fd:
		fd.write(sMsg+"\n")


def Time2Str(ti=-1,sFormat="%Y-%m-%d %H:%M:%S"):
	if ti<0:
		t=time.localtime()
	else:
		t=time.localtime(ti)
	sTime=time.strftime(sFormat,t)
	return sTime


def LogFile(sFileName,sMsg):
	iIndex=sFileName.rfind("\\")
	sBegin=sFileName[:iIndex]
	sEnd=sFileName[iIndex:]
	if not os.path.exists(sBegin):
		os.makedirs(sBegin)
	sMsg="[%s] %s\n"%(Time2Str(),sMsg)
	with codecs.open(sFileName,"a","utf-8") as fd:
		fd.write(sMsg)


def Save2File(sFileName,xData):
	sData=json.dumps(xData)
	with codecs.open(sFileName,"w","utf-8") as fd:
		fd.write(sData)


def Load4File(sFileName):
	with codecs.open(sFileName,"rb","utf-8") as fd:
		sData=fd.read()
		xData=json.loads(sData)
		return xData
	return {}


def GetCWD():
	sCWD=os.getcwd()
	return sCWD
