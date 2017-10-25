# -*- coding -*-

import time

def InitNeiHan():
	import neihan.neihan
	obj=neihan.neihan.CNeiHan()
	iEndTime=time.time()+5*3600
	i=0
	while True:
		obj.GetData()
		time.sleep(2)
		iNowTime=time.time()
		if iNowTime>iEndTime:
			break
		i=i+1
		print("count:{}".format(i))
	obj.SaveOtherInfo()
