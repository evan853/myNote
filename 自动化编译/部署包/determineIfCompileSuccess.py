# -*- coding:utf-8 -*-
import sys
import os

dirName=sys.argv[1][:8]+"-"+sys.argv[1][8:]
if os.path.isdir(sys.argv[2]+"/"+dirName) and os.listdir(sys.argv[2]+"/"+dirName):
	print 0
else:
	print 125
