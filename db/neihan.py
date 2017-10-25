# -*- coding:utf8 -*-

import sqlite3

TABLE_NEI_HAN="""
create table if NOT EXISTS NeiHan
(
	ID int unsigned not null primary key,
	digg int unsigned not null,
	bury int unsigned not null,
	repin int unsigned not null,
	share int unsigned not null,
	content mediumblob not null
)
"""


class CNeiHan(object):

	m_DBName="neihan.sql"
	m_TableName="NeiHan"

	def __init__(self):
		self.m_Conn=None
		self.InitConn()
		self.CreateTable()


	def InitConn(self):
		self.m_Conn=sqlite3.connect(self.m_DBName)


	def CreateTable(self):
		self.Execute(TABLE_NEI_HAN)


	def GetCursor(self):
		if not self.m_Conn:
			self.m_Conn=sqlite3.connect(self.m_DBName)
		oCursor=self.m_Conn.cursor()
		return oCursor


	def Execute(self,sql):
		oCursor=self.m_Conn.cursor()
		oCursor.execute(sql)
		self.m_Conn.commit()
		oCursor.close()


obj=CNeiHan()
sql="select * from NeiHan"
obj.Execute(sql)
