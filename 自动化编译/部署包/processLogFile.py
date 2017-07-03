# -*- coding:utf-8 -*-
import os,sys,re

if __name__=="__main__":
	pattern=re.compile("^Progress \([0-9]+\)")
	pattern1=re.compile("\r")
	colorPattern=re.compile("\[[0-9]*;?[0-9]*m")
	a=[]
	with open(sys.argv[1],"rb") as src:
		for i in src.readlines():
			if re.findall(pattern1,i):
				for j in pattern1.sub("\n",i).split("\n"):
					a.append(j)
			else:
				a.append(i)
				
	for i in a:
		if re.findall(pattern,i):
			pass
		elif i.strip()=="":
			pass
		else:
			print colorPattern.sub("",i).strip()
