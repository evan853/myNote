# -*- coding:utf-8 -*-

import getopt
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('gbk')

class statJavaLines:
    def __init__(self,statPath):
        self.statPath=statPath
        self.allFilesInAPath=[]
        self.allLines=0
        self.allBlankLines=0
        self.allAnnotationLines=0
        self.allValidLines=0
        self.outputFileFlag=0

    def validPathOrFile(self):
        if os.path.isdir(self.statPath):
            return (True,"DIR")
        elif os.path.isfile(self.statPath):
            return (True,"FILE")
        else:
            return (False,"INVALID")

    def validIsAJavaFile(self):
        pattern=re.compile("\.java$",re.I)
        if re.findall(pattern,self.statPath):
            return True
        else:
            return False

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
        patternStart=re.compile("/\*")
        patternEnd=re.compile("\*/")
        patternOther=re.compile("^\s*//.*")
        flag=0
        lines=0
        with open(fileName,"r") as o:
            tmpFile=o.readlines()
            for n in range(len(tmpFile)):
                if re.findall(patternStart,tmpFile[n]) and flag==0:
                    flag=1
                    if re.findall("^\s*/\*",tmpFile[n]):
                        lines+=1
                elif re.findall(patternEnd,tmpFile[n]) and flag==1:
                    flag=0
                    if re.findall("\*/\s*$",tmpFile[n]):
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

    def statValidLinesInAFile(self,fileName):
        return self.statAllLinesInAFile(fileName)-self.statBlankLinesInAFile(fileName)-self.statAnnotationLinesInAFile(fileName)

    def statValidLinesInAPath(self):
        self.findDotJavaFiles()
        for filePath in self.allFilesInAPath:
            self.allValidLines+=self.statValidLinesInAFile(filePath)

    def printDetailedInAPath(self):
        self.findDotJavaFiles()
        for fileName in self.allFilesInAPath:
            self.printAllInAFile(fileName)

    def outputFile(self,outputStr,fileName="result.txt"):
        if self.outputFileFlag==0:
            try:
                os.remove(fileName)
            except:
                pass
            self.outputFileFlag=1
        with open(fileName,"a") as i:
            i.write(outputStr.encode('gbk'))

    def printAllInAPath(self):
        self.statAllLinesInAPath()
        self.statBlankLinesInAPath()
        self.statAnnotationLinesInAPath()
        self.statValidLinesInAPath()
        outputStr=self.printInformation(self.allLines,self.allBlankLines,self.allAnnotationLines,self.allValidLines,"TOTAL")
        print outputStr
        self.outputFile(outputStr)

    def printInformation(self,allLines,allBlankLines,allAnnotationLines,allValidLines,outputType,name="Statistic information"):
        rtstr="--------------------------------------------------------------------------------\n\n"
        if outputType=="FILE":
            rtstr+="FILE:\t"+name+"\n"
        elif outputType=="TOTAL":
            rtstr+="TOTAL:\t"+name+"\n"
        rtstr +="Total lines:\t" + str(allLines)+"\n"
        rtstr +="Blank lines:\t" + str(allBlankLines)+"\n"
        rtstr +="Annot lines:\t" + str(allAnnotationLines)+"\n"
        rtstr +="Valid lines:\t" + str(allValidLines)+"\n\n"
        return rtstr


    def printAllInAFile(self, fileName):
        outputStr=self.printInformation(self.statAllLinesInAFile(fileName), self.statBlankLinesInAFile(fileName), self.statAnnotationLinesInAFile(fileName), self.statValidLinesInAFile(fileName), "FILE",fileName)
        print outputStr
        self.outputFile(outputStr)

    def main(self):
        vP=self.validPathOrFile()
        if vP[0]:
            if vP[1]=="DIR":
                #先打印详单，再打印总计
                self.printDetailedInAPath()
                self.printAllInAPath()
            elif vP[1]=="FILE":
                #入参只是文件的话，校验是否为java文件，如是java文件，则打印总计
                if self.validIsAJavaFile():
                    self.printAllInAFile(self.statPath)
                else:
                    print u"The parameter is not a java file!"
        else:
            print u"The parameter is neither a valid path, nor a valid file name!"

if __name__ =="__main__":
    if len(sys.argv)==2:
        s = statJavaLines(sys.argv[1])
        s.main()
    else:
        print "You have to enter only one parameter! "

    #statPath=ur"F:\code\SmartParking"
    #statPath=ur"F:\code\SmartParking\DynamicBox\src\main\java\mehdi\sakout\dynamicbox\测试\1.java"
    #statPath=ur"F:\code\SmartParking\DynamicBox\src\main\java\mehdi\sakout\dynamicbox\DynamicBox.java"
    #s=statJavaLines(statPath)
    #s.main()