#!/bin/bash
svnPath[0]="https://192.168.0.37/svn/Code/SmartParking/branches/SmartParking2.0/DynamicBox"
svnPath[1]="https://192.168.0.37/svn/Code/SmartParking/branches/SmartParking2.0/Banner"
svnPath[2]="https://192.168.0.37/svn/Code/SmartParking/branches/SmartParking2.0/SmartParkingD"
svnPath[3]="https://192.168.0.37/svn/Code/SmartParking/branches/SmartParking2.0/SmartParkingP"
svnPath[4]="https://192.168.0.37/svn/Code/SmartParking/branches/SmartParking2.0/ViewPagerIndicator"
svnPath[5]="https://192.168.0.37/svn/Code/SmartParking/branches/SmartParking2.0/build.gradle"
svnPath[6]="https://192.168.0.37/svn/Code/SmartParking/branches/SmartParking2.0/gradle.properties"
svnPath[7]="https://192.168.0.37/svn/Code/SmartParking/branches/SmartParking2.0/local.properties"
svnPath[8]="https://192.168.0.37/svn/Code/SmartParking/branches/SmartParking2.0/settings.gradle"
svnUserName="smartparkingpublic"
svnUserPasswd="smartparkingpublic"

jenkinsPath="http://192.168.0.34:8080/jenkins"
jenkinsJobName="SmartParking_2.0_front_apk_build_docker_developer"
jenkinsJobToken="ffff3333"
jenkinsUserName="wei.yan"
jenkinsUserToken="08919871031c9682e353356caa8e1089"

scriptHome="/home/jenkins_script/smartparking/v2.0/front/apk"

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
