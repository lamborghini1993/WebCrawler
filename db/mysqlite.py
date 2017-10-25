# -*- coding:utf8 -*-

import sqlite3

class CSqlite(object):
	pass

TABLE_NEI_HAN="""
create table if NOT EXISTS NeiHan
(
	ID int unsigned primary key,
	digg int unsigned,
	bury int unsigned,
	repin int unsigned,
	share int unsigned,
	content mediumblob
)
"""

conn=sqlite3.connect("NeiHan")
cursor=conn.cursor()
cursor.execute(TABLE_NEI_HAN)
cursor.close
