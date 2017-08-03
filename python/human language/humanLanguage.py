# -*- coding:utf-8 -*-
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class HumanLanguage():
    def __init__(self,fileName):
        with open(fileName) as f:
            self.fileContentList=f.readlines()

    def extractEnContent(self):
        regx=re.compile("^\s*\w+\s+\w+")
        enContentList = []

        for content in self.fileContentList:
            if re.findall(regx,content):
                enContentList.append(content)
        for i in range(len(enContentList)):
            enContentList[i]=re.sub(u'[\u4e00-\u9fa5].*', '', enContentList[i].decode('gb2312')).encode('gb2312')

        return enContentList

    def outputEnContent2File(self,fileName):
        enContentList=self.extractEnContent()
        with open(fileName,'wb') as w:
            #print enContentList
            for i in enContentList:
                w.write(i.strip())
                w.write("\n")

    def extractCnContent(self):
        pass

if __name__=="__main__":
    filePath=u"F:\\github\\new\myNote\\python\\human language\\The Old Man and The Sea.txt"
    outputFile=u'F:\\github\\new\\myNote\\python\\human language\\eng.txt'
    hLan=HumanLanguage(filePath)
    hLan.outputEnContent2File(outputFile)

