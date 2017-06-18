# -*- coding:utf-8 -*-
import os,time,re
#import sys
#reload(sys)
#sys.setdefaultencoding("gbk")

class ArrangeFiles():
    def __init__(self):
        self.allFilesPath=[]
        self.allFilesPathAndMtime = {}
        self.videoTypes=["avi","mp4","mkv"]
        #self.videoTypes = ["z", "m"]

    def findAllFiles(self,path):
        for root,dirs,files in os.walk(path):
            for f in files:
                self.allFilesPath.append(os.path.join(root,f))

    def getFilesMtime(self,fileName):
        ltimestamp=os.stat(fileName).st_mtime
        year=str(time.localtime(ltimestamp).tm_year)
        month= str(time.localtime(ltimestamp).tm_mon)
        day = str(time.localtime(ltimestamp).tm_mday)
        if len(month)==1:
            month = "0" + month
        if len(day)==1:
            day="0"+day
        rt=year+month+day
        return rt

    def getAllVideoFiles(self,path):
        self.findAllFiles(path)
        patternStr=""
        for i in self.videoTypes:
            patternStr+="|"+i
        patternStr="\.(?:"+patternStr[1:]+")$"
        pattern = re.compile(patternStr,re.I)
        for f in range(len(self.allFilesPath)-1,-1,-1):
            if not re.findall(pattern,self.allFilesPath[f]):
                del self.allFilesPath[f]

    def getAllFilesMtime(self):
        for i in self.allFilesPath:
            self.allFilesPathAndMtime[i]=self.getFilesMtime(i)

    def filterFilesByMtime(self,mtime):
        for i in self.allFilesPathAndMtime.keys():
            if mtime <> str(self.allFilesPathAndMtime[i]):
                self.allFilesPathAndMtime.pop(i)

    def cutFileIntoDir(self,fileName,Dir):
        os.rename(fileName,Dir)

    def cutFilesIntoDir(self):
        pattern=re.compile("^.*?:")
        #patternFile = re.compile('\\\\(.*?)$',re.S)
        patternTest=re.compile(r"\\")

        for i in self.allFilesPathAndMtime.keys():
            if not os.path.exists(re.findall(pattern,i)[0]+"\\"+self.allFilesPathAndMtime[i]):
                os.mkdir(re.findall(pattern,i)[0]+"\\"+self.allFilesPathAndMtime[i])
            self.allFilesPathAndMtime[i] = re.findall(pattern, i)[0] + "\\" + self.allFilesPathAndMtime[i] + "\\" + \
                                           re.split(patternTest,i)[-1]
            self.cutFileIntoDir(i,self.allFilesPathAndMtime[i])

if __name__=="__main__":
    af=ArrangeFiles()
    af.getAllVideoFiles("E:\\")
    af.getAllFilesMtime()
    af.filterFilesByMtime("20170618")
    af.cutFilesIntoDir()
    for i in af.allFilesPathAndMtime.keys():
        print i+'\t'+af.allFilesPathAndMtime[i]



