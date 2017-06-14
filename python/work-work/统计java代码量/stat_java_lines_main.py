# -*- coding:utf-8 -*-

import getopt
import os
import re

class statJavaLines:
    def __init__(self,statPath):
        self.statPath=statPath
        self.allFilesInAPath=[]
        self.allLines=0
        self.allBlankLines=0
        self.allAnnotationLines=0

    def validPathOrFile(self):
        if os.path.isdir(self.statPath):
            return (True,"DIR")
        elif os.path.isfile(self.statPath):
            return (True,"FILE")
        else:
            return (False,"INVALID")

    def findDotJavaFiles(self):
        self.findAllFilesInAPath()
        pattern=re.compile("\.java$",re.I)
        if self.allFilesInAPath:
            for i in range(len(self.allFilesInAPath)-1,-1,-1):
                if not re.findall(pattern,self.allFilesInAPath[i]):
                    del self.allFilesInAPath[i]
        self.allFilesInAPath=list(set(self.allFilesInAPath))

    def findAllFilesInAPath(self):
        for root,dirs,files in os.walk(self.statPath):
            for f in files:
                self.allFilesInAPath.append(os.path.join(root,f))
        #pattern=re.compile(u"\\\\.*")
        #for n in range(len(self.allFilesInAPath)):
        #    re.sub(pattern, u'/', self.allFilesInAPath[n])

    def statAllLinesInAFile(self,fileName):
        with open(fileName,"r") as o:
            #print o.readlines()
            return len(o.readlines())

    def statAllLinesInAPath(self):
        self.findDotJavaFiles()
        for filePath in self.allFilesInAPath:
            self.allLines+=self.statAllLinesInAFile(filePath)

    def statBlankLinesInAFile(self,fileName):
        pattern=re.compile("^\s*$")
        blankLines=0
        with open(fileName, "r") as o:
            #print o.readlines()
            for i in o.readlines():
                if re.findall(pattern,i):
                    blankLines+=1
            return blankLines

    def statBlankLinesInAPath(self):
        self.findDotJavaFiles()
        for filePath in self.allFilesInAPath:
            self.allBlankLines += self.statBlankLinesInAFile(filePath)

    def statAnnotationLinesInAFile(self,fileName):
        patternStart=re.compile("/\*.*")
        patternEnd=re.compile("\*/")
        patternOther=re.compile("^\s*//.*")
        flag=0
        lines=0
        with open(fileName,"r") as o:
            tmpFile=o.readlines()
            for n in range(len(tmpFile)):
                if re.findall(patternStart,tmpFile[n]) and flag==0:
                    flag=1
                    lines+=1
                elif re.findall(patternEnd,tmpFile[n]) and flag==1:
                    flag=0
                    lines+=1
                elif flag==1:
                    lines+=1
                elif flag==0 and re.findall(patternOther,tmpFile[n]):
                    lines+=1
            return lines

    def statAnnotationLinesInAPath(self):
        self.findDotJavaFiles()
        for filePath in self.allFilesInAPath:
            self.allAnnotationLines += self.statAnnotationLinesInAFile(filePath)

    def statValidLinesInAFile(self):
        pass

    def statValidLinesInAPath(self):
        pass

    def main(self):
        vP=self.validPathOrFile()
        if vP[0]:
            if vP[1]=="DIR":
                self.statAllLinesInAPath()
                self.statBlankLinesInAPath()
                self.statAnnotationLinesInAPath()
                print self.allLines,"\t",self.allBlankLines,"\t",self.allAnnotationLines
                validLines=self.allLines-self.allBlankLines-self.allAnnotationLines
                print "Valid lines: "+str(validLines)
            elif vP[1]=="FILE":
                pass
        else:
            print u"The parameter is neither a valid path, nor a valid file name!"

if __name__ =="__main__":
    #statPath=u"F:\code\SmartParking"
    statPath=u"F:\code\SmartParking\DynamicBox\src\main\java\mehdi\sakout\dynamicbox\dfa"
    s=statJavaLines(statPath)
    s.main()