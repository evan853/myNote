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
        regx=re.compile("(^\s*\w+\s+\w+)|(^\s*$)")
        enContentList = []

        for content in self.fileContentList:
            if re.findall(regx,content):
                enContentList.append(content)
        for i in range(len(enContentList)):
            enContentList[i]=re.sub(u'[\u4e00-\u9fa5].*', '', enContentList[i].decode('gbk')).encode('gbk')

        return enContentList

    def outputEnContent2File(self,fileName):
        enContentList=self.extractEnContent()
        with open(fileName,'wb') as w:
            #print enContentList
            for i in enContentList:
                w.write(i.strip())
                w.write("\n")

    def extractCnContent(self):
        regx = re.compile(u'(\.*[\u4e00-\u9fa5].*)|(^\s*$)')
        cnContentList = []

        for content in self.fileContentList:
            if re.findall(regx, content.decode('gbk')): #可以指定为ignore/replace/xmlcharrefreplace,默认是strict
                cnContentList.append(content)
        for i in range(len(cnContentList)):
            cnContentList[i]=re.sub(u'[\u4e00-\u9fa5]', '', cnContentList[i].decode('gbk')).encode('gbk')

        return cnContentList

    def outputCnContent2File(self,fileName):
        cnContentList=self.extractCnContent()
        with open(fileName,'wb') as w:
            for i in cnContentList:
                w.write(i.strip())
                w.write("\n")

if __name__=="__main__":
    filePath=u"F:\\github\\new\myNote\\python\\human language\\The Old Man and The Sea.txt"
    enOutputFile=u'F:\\github\\new\\myNote\\python\\human language\\en.txt'
    cnOutputFile = u'F:\\github\\new\\myNote\\python\\human language\\cn.txt'
    hLan=HumanLanguage(filePath)
    hLan.outputEnContent2File(enOutputFile)
    hLan.outputCnContent2File(cnOutputFile)

