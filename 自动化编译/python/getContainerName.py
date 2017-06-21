# -*- coding:utf-8 -*-
import commands
import re

def getAllContainerName():
	shellStr = """docker ps -a | awk -F '[ ]{2,}|"' '{if(NR>1) print $8}'"""
	pattern = re.compile("a[1-9]{1}[0-9]{0,}")
	#shellStr = """docker inpect """
	(stat, output) = commands.getstatusoutput(shellStr)
	if output=="":
		return "a1"
	names = output.split("\n")
	codeN = []
	sid=0
	for i in names:
		if re.findall(pattern,i):
			codeN.append(int(i[1:]))
	if codeN <> []:
		codeN.sort()
	else:
		return "a1"
	for i in range(1, codeN[-1] + 2):
		if i not in codeN:
			sid=i
			break
	return "a"+str(sid)

if __name__ == "__main__":
	print getAllContainerName()
		
