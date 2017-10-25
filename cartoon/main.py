# -*- coding:utf8 -*-

from Cartoon import *
from Gentleman import *

# http://www.xeall.com/ribenmanhua/
url = "http://www.xeall.com/shenshi"

# enter your path
save_path = "F:\\code\\python\\Internetworm\\cartoon"

gentleman = Gentleman(url, save_path)
gentleman.hentai()
