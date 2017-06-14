# -*- coding: UTF-8 -*-
import os, sys

def main():
    FilterList = ["php","js","css","html","txt","ini",'java','xml']
    TargetStr = "import"
    TargetFileList = []

    if getParasFromTerminal() <> []:
        for i in getAllAbsolutePathOfFiles(getParasFromTerminal()[0],FilterList):
            tmpFile = findStrInFile(TargetStr,i)
            if tmpFile <> "":
                TargetFileList.append(tmpFile)
    if TargetFileList <> []:
        print "These files contains strings you specified:"
        for i in TargetFileList:
            print i
    else:
        print "No file contains strings you specified."

def getAllAbsolutePathOfFiles(OriPath,FileFilterList):
    '''Usage:递归返回给定路径下指定后缀的文件全路径
       Para:OrePath 给定的路径
            FileFilterList 需要的文件类型后缀列表
       Return:文件(含绝对路径)列表'''
    FilesWithFullPath = []
    for root,dirs,files in os.walk(OriPath):
        for i in files:
            for j in FileFilterList:
                if i.endswith("."+j):
                    FilesWithFullPath.append(os.path.join(root,i))

    return FilesWithFullPath

def getParasFromTerminal():
    '''Usage：从终端获取参数列表,如果没有输入参数,返回空列表
       Para:None
       Return:终端给出的参数列表'''
    ParaList=[]
    if len(sys.argv) > 1:
        for i in range(1,len(sys.argv)):
            ParaList.append(sys.argv[i])

    return ParaList

def findStrInFile(TargetStr,TargetFile):
    returnValue = ""
    o = open(TargetFile,'rb')
    for i in o.readlines():
        if TargetStr in i:
            returnValue = TargetFile
            break

    o.close()
    return returnValue

if __name__ == "__main__":
    main()