#!/bin/bash
svnPath=""
svnUserName=""
svnUserPasswd=""

jenkinsPath=""
jenkinsJobName=""
jenkinsJobToken=""
jenkinsUserName=""
jenkinsUserToken=""

scriptHome="/home/test"

function main()
{
newestRev=`svn info $svnPath --username=$svnUserName --password=$svnUserPasswd | grep "Last Changed Rev" | awk -F ": " '{print $2}'`
if [ -f ./rev ]
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
