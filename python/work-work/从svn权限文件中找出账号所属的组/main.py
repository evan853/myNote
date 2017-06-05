# -*- coding: UTF-8 -*-
import re

def extractDictFromGroups_conf(FileName):
    '''Usage: 从给定的groups.conf文件中以字典的格式导出权限分组和账户的对应关系
       Paras: FileName 需要处理的文件名
       Return: returnDict 字典列表'''
    flag = 0
    returnDict = {}
    fo = open(FileName,'rb')
    for i in fo.readlines():
        if i.startswith("["):
            flag = 1
            continue
        if flag == 1 and len(i.split("=")) > 1:
            returnDict[i.split("=")[0]] = i.split("=")[1].strip()
    fo.close()

    return returnDict

def extractAccountsFromFile(FileName):
    '''Usage: 从给定文件中提取需要处理的账号信息
       Paras: FileName需要处理的文件名
       Return: returnList需要处理的账号列表'''
    fo = open(FileName,'rb')
    returnList = []
    for i in fo.readlines():
        returnList.append(i.strip())
    fo.close()

    return returnList

def searchGroupOfAccounts(Accounts,GroupOfAccounts):
    '''Usage: 从给定的分组账号关系dict中查找指定账号的分组信息
       Paras: Accounts账号列表；GroupOfAccounts分组和账号对应关系字典
       Return: '''
    returnDict = {}
    for i in GroupOfAccounts.keys():
        for j in Accounts:
            if j in GroupOfAccounts[i] and not (re.findall("\w"+j,GroupOfAccounts[i]) or re.findall(j+"\w",GroupOfAccounts[i])):
                if returnDict.has_key(i):
                    returnDict[i] = returnDict[i]+","+j
                else:
                    returnDict[i] = j

    return returnDict

def deleteAccountsFromFile(Accounts,FileName):
    pass

def testFunc():
    '''Usage: 测试函数'''
    D = extractDictFromGroups_conf("groups.conf")
    L = extractAccountsFromFile("list.txt")
    S = searchGroupOfAccounts(L,D)
    for i in S.keys():
        print i, " : ", S[i]

def main():
    pass

if __name__ == "__main__":
    testFunc()