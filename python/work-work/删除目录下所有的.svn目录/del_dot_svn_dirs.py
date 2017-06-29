# -*- coding:utf-8 -*-
import os,re,shutil,commands

def findAllDotSvnDirs(srcPath):
    pattern=re.compile(r".svn$",re.I)
    SvnFiles=[]
    if os.path.isdir(srcPath):
        for root,dirs,files in os.walk(srcPath):
            for i in dirs:
                SvnDir = os.path.join(root, i)
                #print SvnDir
                if re.findall(pattern,SvnDir):
                    SvnFiles.append(SvnDir)
    else:
        print u"invalid path"

    return SvnFiles

def removeDirs(SvnFiles):
    LogStr=[]
    '''for i in SvnFiles:
        shutil.rmtree(i)
        LogFile.append(i+u" 已被删除")
    with open("log.txt","rb") as o:
        for i in LogStr:
            o.write(i)'''
    for i in SvnFiles:
        DelCommand="rmdir /S/Q \""+i+"\""
        #print DelCommand
        os.system(DelCommand.encode("gbk"))
        #commands.getstatusoutput(DelCommand)
        LogStr.append(DelCommand.encode("gbk")+"\n")
    with open("log.txt", "wb") as o:
        for i in LogStr:
            o.write(i)

if __name__ == "__main__":
    srcPath=u"H:\钉钉\ParkingAndroid"
    removeDirs(findAllDotSvnDirs(srcPath))