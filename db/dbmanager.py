# -*- coding: utf-8 -*-
# 肖豪

import sqlite3

class CDBManager(object):

	m_DBName = ""

	def __init__(self):
		self.m_Conn = None
		self.InitConn()
		self.CreateTable()

	def InitConn(self):
		self.m_Conn = sqlite3.connect(self.m_DBName)

	def CreateTable(self):
		self.Execute(TABLE_NEI_HAN)

	def GetCursor(self):
		if not self.m_Conn:
			self.m_Conn = sqlite3.connect(self.m_DBName)
		oCursor = self.m_Conn.cursor()
		return oCursor

	def Execute(self, sql):
		oCursor = self.m_Conn.cursor()
		oCursor.execute(sql)
		self.m_Conn.commit()
		oCursor.close()

