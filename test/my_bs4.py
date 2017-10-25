# -*- coding:utf8 -*-

import bs4

html_doc = """
<html><head><title>The Dormouse's story1</title></head>
<body>
<p class="title"><b>The Dormouse's story2</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup=bs4.BeautifulSoup(html_doc,"html.parser")
# print(soup.prettify())
# print(soup.title)
# print(soup.title.name)
# print(soup.title.string)
# print(soup.title.parent.name)
# print(soup.p)
# print(soup.p["class"])
# print(soup.a)
# print(soup.find_all("p"))
# print(soup.find(id="link3"))
# print(soup.find(class_="sister"))
# print(soup.get_text())	#从文档中获取所有文字内容:

# aa=soup.a
# print(aa.string)
# print(aa["href"],aa["class"],aa["id"],aa.get_text())

markup = "<b><!--Hey, buddy. Want to buy a used parser?--></b>"
soup = bs4.BeautifulSoup(markup,"html.parser")
comment = soup.b.string
print(comment)
