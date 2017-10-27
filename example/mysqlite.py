# -*- coding:utf-8 -*-
# 肖豪
# sqlite3的使用

import sqlite3

TABLE_NEI_HAN = """
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

conn = sqlite3.connect("xxx.sql")
cursor = conn.cursor()
cursor.execute(TABLE_NEI_HAN)
cursor.close()


