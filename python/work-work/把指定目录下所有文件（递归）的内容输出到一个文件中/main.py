# -*- coding: UTF-8 -*-
import os
import sys
import getopt


def cmdArgvsList():
    pass

def main():
    '''主函数'''
#    Paras = getParasFromTerminal()
    FilesInPath = []
    FilterList = []
    OutputFileName = "final.txt"

    ParseParas = parseParas()
    if ParseParas[0] and ParseParas[1][3] <> None:
        FilesInPath = getAllAbsolutePathOfFiles(ParseParas[1][3])

        if ParseParas[1][0] == "java":
            FilterList = ['.java', '.xml', ]
        elif ParseParas[1][0] == "object-c":
            FilterList = ['.m', '.h', ]

        FilesInPath = filterFiles(FilesInPath, FilterList)
        for FileWithAbsPath in FilesInPath:
            appendFileTo(FileWithAbsPath, OutputFileName)

        if ParseParas[1][0] == "java":
            if ParseParas[1][1] == 1:
                deleteBlankLinesOfFile(OutputFileName)
            if ParseParas[1][2] == 1:
                deleteAnnotationOfJava(OutputFileName)
                deleteAnnotationOfXml(OutputFileName)
        elif ParseParas[1][0] == "object-c":
            if ParseParas[1][1] == 1:
                deleteBlankLinesOfFile(OutputFileName)
            if ParseParas[1][2] == 1:
                pass


#    if validParasFromList(Paras):
#        Paras = Paras[0]
#        FilesInPath = getAllAbsolutePathOfFiles(Paras)
#        FilesInPath = filterFiles(FilesInPath,FilterList)
#        for FileWithAbsPath in FilesInPath:
#            appendFileTo(FileWithAbsPath,OutputFileName)
#    else:
#        usage()
#        print "Exit the program already!"
#    deleteAnnotationOfJava(OutputFileName)
#    deleteAnnotationOfXml(OutputFileName)
#    deleteBlankLinesOfFile(OutputFileName)

def deleteAnnotationOfXml(FileName):
    '''Usage: 删除给定xml文件中的注释行
       Paras: FileName 需要处理的文件
       Return: None'''
    Indicator = 0
    TempFinalFileName = 'tempfinal.txt'
    f = open(FileName, 'rb')
    o = open(TempFinalFileName, 'wb')
    AnnoFlag = 0
    for line in f.readlines():
        if line.strip().startswith("<!--") and line.strip().endswith('-->'):
            Indicator += 1
            continue
        elif line.strip().startswith("<!--") and not line.strip().endswith('-->'):
            Indicator += 1
            AnnoFlag = 1
            continue
        elif line.strip().endswith('-->'):
            Indicator += 1
            AnnoFlag = 0
            continue

        if AnnoFlag == 0:
            o.write(line)
        else:
            Indicator += 1
    o.close()
    f.close()
    os.remove(FileName)
    os.rename(TempFinalFileName, FileName)
    print "Number of XML annotation lines: ", Indicator

def deleteAnnotationOfJava(FileName):
    '''Usage: 删除掉给定java文件中的所有注释行
       Paras: FileName 需要处理的文件
       Return: None
       Note: 此函数尚有缺陷，不能去掉注释嵌套的形式，以后有时间看能否通过栈实现'''
    Indicator = 0
    TempFinalFileName = 'tempfinal.txt'
    f = open(FileName, 'rb')
    o = open(TempFinalFileName, 'wb')
    AnnoFlag = 0
    for line in f.readlines():
        if line.strip().startswith("//"):
            Indicator += 1
            continue
        elif line.strip().startswith("/*") and line.strip().endswith('*/'):
            Indicator += 1
            continue
        elif line.strip().startswith("/*") and not line.strip().endswith('*/'):
            Indicator += 1
            AnnoFlag = 1
            continue
        elif line.strip().endswith('*/'):
            Indicator += 1
            AnnoFlag = 0
            continue
        if AnnoFlag == 0:
            o.write(line)
        else:
            Indicator += 1
    o.close()
    f.close()
    os.remove(FileName)
    os.rename(TempFinalFileName,FileName)
    print "Number of JAVA annotation lines: ",Indicator

def deleteBlankLinesOfFile(FileName):
    '''Usage: 去掉java文件中的空白行
       Paras: FileName 需要处理的java文件
       Return: None'''
    Indicator = 0
    TempFinalFileName = 'tempfinal.txt'
    f = open(FileName, 'rb')
    o = open(TempFinalFileName, 'wb')
    for line in f.readlines():
        if line.strip() == '':
            Indicator += 1
        else:
            o.write(line)
    o.close()
    f.close()
    os.remove(FileName)
    os.rename(TempFinalFileName, FileName)
    print "Number of blank lines: ",Indicator

def usage():
    print ""
    print "This is the usage of the program:"
    print ""
    print "     python main.py <DIRECTORYNAME> [OPTION]"
    print ""
    print "     [OPTION]:"
    print "         --without-whitelines    -ww    Remove white lines of the code"
    print "         --without-annotation    -wa    Remove annotation of the code"
    print "         --code-type             -ct    Specify the code type, can be java/object-c"
    print ""

def appendFileTo(FileName,FinalFileName):
    '''Usage: 从源文件读取内容追加到目标文件
       Para: FileName 源文件；FinalFileName 目标文件
       Return: None'''
    f = open(FileName,'rb')
    o = open(FinalFileName,'ab')
    for line in f.readlines():
        o.write(line)
    o.close()
    f.close()

def getParasFromTerminal():
    '''Usage：从终端获取参数列表,如果没有输入参数,返回空列表
       Para:None
       Return:终端给出的参数列表'''
    ParaList=[]
    if len(sys.argv) > 1:
        for i in range(1,len(sys.argv)):
            ParaList.append(sys.argv[i])

    return ParaList

def parseParas():
    '''Usage: 处理给定的参数列表'''

    #argvsTuple三个参数分别对应代码类型，是否包含空行，是否包含注释行
    argvsTuple = ["java",0,0,None]
    flag = 0

    try:
        opts,argvs = getopt.getopt(sys.argv[1:],"",["ww","without-whitelines","wa","without-annotation","code-type=","ct="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for o,a in opts:
        if o in ("-ww","--without-whitelines") and a == "":
            argvsTuple[1] = 1
        elif o in ("-ww","--without-whitelines") and a <> "":
            flag = 1

        if o in ("-wa","--without-annotation") and a == "":
            argvsTuple[2] = 1
        elif o in ("-wa","--without-annotation") and a <> "":
            flag = 1

        if o in ("-ct","--code-type") and a in ("java","object-c"):
            argvsTuple[0] = a
        elif o in ("-ct", "--code-type") and a not in ("java", "object-c"):
            flag = 1

        if o not in ("-ww","--without-whitelines","-wa","--without-annotation","-ct", "--code-type"):
            flag = 1

    if len(argvs) == 1:
        if not os.path.isdir(argvs[0]):
            flag = 1
        else:
            argvsTuple[3] = argvs[0]
    else:
        flag = 1

    if flag == 1:
        usage()
        return (False,argvsTuple)
    else:
        return (True,argvsTuple)


#def validParasFromList(Paras):
#    '''Usage: 判断给定的参数列表是否满足参数定义
#              如果没有输入参数，提示输入参数
#              如果为单个参数，参数必须为有效的目录路径
#              如果有多个参数，则调用parseParas函数处理
#      Return:参数有效返回True,参数无效返回False'''
#    if len(Paras) == 0:
#        print "You have to enter one parameter at least!"
#        return False
#    elif len(Paras) == 1:
#        if os.path.isdir(Paras[0]):
#            return True
#        else:
#            print "What you entered is not a valid path!"
#            return False
#    else:
#        parseParas()

def filterFiles(FilesList,FilterList):
    '''Usage: 从指定文件列表中选出特定后缀的文件并返回
       Para: FilesList 指定的文件列表；FilterList指定的文件后缀列表
       Return: 处理后的文件列表'''
    FinalFilesList = []
    for i in FilterList:
        for j in FilesList:
            if j.endswith(i):
                FinalFilesList.append(j)
                FilesList.remove(j)

    return FinalFilesList


def getAllAbsolutePathOfFiles(OriPath):
    '''Usage:递归返回给定路径下所有文件的全路径
       Para:OrePath 给定的路径
       Return:文件(含绝对路径)列表'''
    FilesWithFullPath = []
    for root,dirs,files in os.walk(OriPath):
        for i in files:
            FilesWithFullPath.append(os.path.join(root,i))

    return FilesWithFullPath

if __name__=="__main__":
    main()