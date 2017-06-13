# -*- coding:utf-8 -*-
import hashlib
import sys, os

class validateFile:
    def __init__(self):
        self.modeList=["md5","sha1","sha224","sha256","sha384","sha512","all"]

    def main(self):
        paraList = self.getParaFromCmd()
        if paraList[0]==1:
            if self.validParaIsAFile(paraList[1][0]):
                sh = self.computeSha(paraList[1][0])
                print sh
        elif paraList[0]==2:
            if self.validParaIsAFile(paraList[1][0]) and self.validVerificationMode(paraList[1][1]):
                if paraList[1][1]=="all":
                    self.computeAllSha(paraList[1][0])
                else:
                    sh = self.computeSha(paraList[1][0], paraList[1][1])
                    print sh

    def computeAllSha(self,fileName):
        modeList=self.modeList
        del modeList[-1]
        for i in modeList:
            print self.computeSha(fileName,i)

    def getParaFromCmd(self):
        if len(sys.argv)==3:
            arguments=[2,[sys.argv[1],sys.argv[2]]]
        elif len(sys.argv)==2:
            arguments=[1,[sys.argv[1]]]
        elif len(sys.argv)==1:
            print "You should input one option at least! "
            arguments=[0,[]]
        else:
            print "You have entered too many parameters!"
            arguments=[-1,[]]
        return arguments

    def validVerificationMode(self,mode):
        if mode in self.modeList:
            return True
        else:
            print u'指定的校验模式"'+mode+u'"错误，只支持这些模式'+",".join(['"'+i+'"' for i in self.modeList])
            return False

    def validParaIsAFile(self,fileName):
        if os.path.isfile(fileName):
            return True
        else:
            return False

    def computeSha(self,fileName,shaC="sha256"):
        """默认计算sha256值，需要计算其它校验值请指定shaC参数，支持的校验值类型有sha256,md5,sha224,sha1,sha384,sha512"""
        t=eval("hashlib."+shaC+"()")
        with open(fileName,"rb") as o:
            while True:
                data=o.read(64*1024)
                if not data:
                    break
                t.update(data)
            rt=shaC+u"\t值\t"+t.hexdigest()
            return rt


if __name__ == "__main__":
    s=validateFile()
    s.main()