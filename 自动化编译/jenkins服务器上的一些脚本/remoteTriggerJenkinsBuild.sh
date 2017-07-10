#!/bin/bash
svnPath[0]=""
svnUserName=""
svnUserPasswd=""

jenkinsPath=""
jenkinsJobName=""
jenkinsJobToken=""
jenkinsUserName=""
jenkinsUserToken=""

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
