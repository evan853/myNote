# -*- coding: utf-8 -*-
import sys

timeStat=int(sys.argv[1])
if timeStat/60 < 1:
	print "容器运行了 "+str(timeStat)+" 秒..."
else:
	if timeStat%60 == 0:
		print "容器运行了 "+str(timeStat/60)+" 分钟..."
	else:
		print "容器运行了 "+str(int(timeStat/60))+" 分 "+str(timeStat%60)+" 秒..." 
