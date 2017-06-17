# -*- coding:utf-8 -*-
import sys
import urllib
import urllib2
import re
#import sys
reload(sys)
sys.setdefaultencoding('gbk')

# 从purepen爬东西
class JPM:
    # 初始化一些变量
    def __init__(self):
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}
        self.title_and_url = []
        self.title_and_content = []

    def getPageHTML(self,pageURL):
        try:
            request=urllib2.Request(pageURL,headers=self.headers)
            response=urllib2.urlopen(request)
            pageCode=response.read().decode('gbk')
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print u"打开网站失败,原因：",e.reason
                return None


    def assembleURL(self,url,chapterList):
        for n in range(len(chapterList)):
            chapterList[n][0]=url+chapterList[n][0]
        return chapterList

    def gettTitleAndURL(self,coverHtml):
        pattern=re.compile("<td.*?<a.*?\"(.*?)\">(.*?)</a>",re.S)
#        patternCh=re.compile('.*',re.S)
        self.title_and_url=re.findall(pattern,coverHtml)
        for n in range(len(self.title_and_url)):
            self.title_and_url[n]=list(self.title_and_url[n])
            self.title_and_url[n][0]=self.title_and_url[n][0].strip()
            self.title_and_url[n][1] = self.title_and_url[n][1].strip()
#            print re.findall(patternCh,self.title_and_url[n][1])[0]
#            self.title_and_url[n][1] = re.findall(patternCh,self.title_and_url[n][1])[0]
        if self.title_and_url:
            del self.title_and_url[-1]

    def getChapterContent(self,chapterHtml):
        pattern=re.compile("<pre.*?><font.*?>(.*?)</font.*?>",re.S|re.I)
        chapterContent=re.findall(pattern,chapterHtml)
        if chapterContent:
            return chapterContent[0]
        return 'nothing'

    def formatOutputList(self,outputList):
        for n in range(len(outputList)):
            for z in range(len(outputList[n])):
                outputList[n][z]=outputList[n][z]+'\n'

    def writeIntoFile(self,sourceList,fileName="JPM.txt"):
        w=open(fileName,'wb')
        for i in sourceList:
#            w.write(i[0])
            w.write(i[1])
        w.close()

    def start(self):
        url="http://www.purepen.com/jpm/"
        coverHtml=self.getPageHTML(url)
        self.gettTitleAndURL(coverHtml)
        self.title_and_url=self.assembleURL(url,self.title_and_url)


        for n in range(len(self.title_and_url)):
            chapterHtml=self.getPageHTML(self.title_and_url[n][0])
            self.title_and_content.append([self.title_and_url[n][1],self.getChapterContent(chapterHtml)])

#        self.title_and_content=self.formatOutputList(self.title_and_content)
        self.writeIntoFile(self.title_and_content)

        self.tester()

    def tester(self):
        pass
#        print self.title_and_content[0]
#        print self.title_and_url
#        for i in self.title_and_url:
#            print "%s\t:%s " % (i[1], i[0])
#        for i in self.title_and_content:
#            print "%s\t:%s " % (i[0], i[1])

class processFile:
    def __init__(self,fileName):
        self.fileName=fileName

    def processFile(self,destFileName):
        with open(self.fileName,"rb") as r:
            flag=0
            flagpoem=0
            poemPattern=re.compile("^\xa1{8}")
            lines=r.readlines()
            #print lines[:20]
            #for i in lines[:20]:
                #print i
            pattern=re.compile("^\s+$")
            for n in range(len(lines)-2,-1,-1):
                if re.findall(pattern,lines[n]):
                    flag=1
                else:
                    if flag==1:
                        flag=0
                    elif flag==0 and not re.findall(poemPattern,lines[n]):
                        lines[n]=re.sub(re.compile("\s+$"),"",lines[n])
                        #lines[n+1]=re.sub(re.compile("^\xa1*"),"",lines[n+1])
                    else:
                        pass

            with open(destFileName,"wb") as w:
                for i in lines:
                    w.write(i)

#jpm = JPM()
#jpm.start()
p=processFile("JPM.txt")
p.processFile("JPM2.txt")