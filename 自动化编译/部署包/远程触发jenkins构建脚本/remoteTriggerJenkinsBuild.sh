#!/bin/bash

#svn相关配置信息
#如果有多个svn路径需要关注时，分别写在下面的数组项中
svnPath[0]=""
svnPath[1]=""
svnPath[2]=""
svnPath[3]=""
svnPath[4]=""

svnUserName=""
svnUserPasswd=""

#jenkins相关配置信息
jenkinsPath=""
jenkinsJobName=""
jenkinsJobToken=""
jenkinsUserName=""
jenkinsUserToken=""

#脚本所在路径
scriptHome=""

function main()
{
newestRev=0
for i in ${svnPath[@]}
do
	tmpRev=`svn info $i --username=$svnUserName --password=$svnUserPasswd | grep "Last Changed Rev" | awk -F ": " '{print $2}'`
	((newestRev+=$tmpRev))
done

if [ -f $scriptHome/rev ]
then
	rev=`cat $scriptHome/rev`	
	if [ $rev != $newestRev ]
	then
		wget --auth-no-challenge --http-user=$jenkinsUserName --http-password=$jenkinsUserToken --secure-protocol=TLSv1 -O - $jenkinsPath/job/$jenkinsJobName/build?token=$jenkinsJobToken
		echo $newestRev>$scriptHome/rev
	fi
else
	wget --auth-no-challenge --http-user=$jenkinsUserName --http-password=$jenkinsUserToken --secure-protocol=TLSv1 -O - $jenkinsPath/job/$jenkinsJobName/build?token=$jenkinsJobToken
    echo $newestRev>$scriptHome/rev
fi
}

main
