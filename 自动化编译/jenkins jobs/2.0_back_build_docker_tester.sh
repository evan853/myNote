set +x

#��������
platName="Back"																		#������ģ������
rootDir="/compileDir"																#���ýű�����·��
baseDir="/compileDir/SmartParking/TEST/V2.0"										#��֧���ڵı��ظ�·��
compileDir="/compileDir/SmartParking/TEST/V2.0/Back/code"							#����������ص�·��
logDir="/compileDir/SmartParking/TEST/V2.0/Back/log"								#��־�����·��
archiveOutputDir="/compileDir/SmartParking/TEST/V2.0/Back/archives"					#�����ﱣ���ڵ�·��
imageName="192.168.0.34:5000/build/smartparking-back-build:lastest"					#�������õľ���

#svn��汾��ǩ�õı���
svnTagBasePath="https://192.168.0.37/svn/Code/SmartParking/tags"					#��svn��ǩ���ڵĸ�·��
svnCodePath="https://192.168.0.37/svn/Code/SmartParking/branches/SmartParking2.0"	#��Ҫ���ǩ��svn��֧����·��
svnUserName="smartparkingpublic"
svnUserPasswd="smartparkingpublic"
svnTagMainNumber="SmartParkingV2.0.0"												#��ǩ�����е����汾��
svnTagSecondaryNumber="_b"															#��ǩ�����еĴΰ汾��

#������С�汾�ţ�Ϊ��ʱʹ��Ĭ�ϵİ汾�Ź��򣬷���ʹ�øô������С�汾��
buildNumber="1"

function createDir(){
	#��������Ŀ¼
	#�����������·����ɾ����·���µ������ļ�
	if [ ! -d $compileDir ] 
	then
		mkdir $compileDir -p
	fi
	rm -rf $compileDir/*
	
	#������־����·��
	if [ ! -d $logDir ] 
	then
		mkdir $logDir -p
	fi
	
	#�������������ﱣ��·��
	if [ ! -d $archiveOutputDir ] 
	then
		mkdir $archiveOutputDir -p
	fi
}

function createDockerContainer(){
	#��������
	dockerName=`python getContainerName.py`
	docker run -itd --name $dockerName --net=host -v $compileDir:/compileDir -v $logDir:/logDir -v $archiveOutputDir:/outputDir $imageName
	stat=$?

	while [ "$stat"x != "0"x ]
	do
		dockerName=`python getContainerName.py`
		docker run -itd --name $dockerName --net=host -v $compileDir:/compileDir -v $logDir:/logDir -v $archiveOutputDir:/outputDir $imageName
		stat=$?
	done
}

function monitorDockerContainer(){
	###��������
	dockerStatus=`docker inspect --format='{{.State.Status}}' $dockerName`
	timeStat=0
	timeout=0
	while [ "$dockerStatus"x = "running"x ]
	do	
		if [ $timeout -gt 30 ]
			then
				echo "�ȴ�ʱ�������������30���ӣ���������"
				docker rm -f $dockerName
				break
		fi
		
		sleep 2m
		((timeStat+=120))
		python statTime.py $timeStat
		timeout=$(($timeout+2))
		dockerStatus=`docker inspect --format='{{.State.Status}}' $dockerName 2>/dev/null || echo 12`
		if [ $dockerStatus = 12 ]
		then
			echo "�����Ѳ����ڣ���������"
			break
		fi
		if [ "$dockerStatus"x != "running"x ]
		then
			echo "�������˳�����������"
			docker rm -f $dockerName
		fi
	done
}

function printLog(){
	#��ӡ��־
	echo "********************************************************"
	echo "********************************************************"
	echo "********************************************************"
	echo "********************************************************"
	echo "***********************����Ϊ��־***********************"
	logFileName=`ls -t $logDir | awk '{if(NR==1) print $1}'`
	echo $logDir/$logFileName
	#��̨����־�ļ����кܶ����õ���Ϣ����Ҫͨ�����½ű�������ӡ����
	python processLogFile.py "$logDir/$logFileName"
}

function getBuildNumber(){
	#��ȡ�汾��,��������BuildNumber�ļ�ʱ����Ҫ��svn�ҵ���ȷ�İ汾��д��BuildNumber���ⲿ���߼���ûд
	#if [ ! -f $baseDir/BuildNumber ]
	#then
	#	echo 0>$baseDir/BuildNumber
	#fi

	#if [ "$buildNumber"x = ""x ]
	#then
	#	buildNumber=`cat $baseDir/BuildNumber`
	#	((buildNumber+=1))
	#fi
	buildNumber=`cat $baseDir/BuildNumber`
	((buildNumber+=1))
	finalBuildNumber=$svnTagMainNumber$svnTagSecondaryNumber$buildNumber
	echo $buildNumber>$baseDir/BuildNumber
}

function createTag(){
	#���ǩ
	svnTagNumber=`grep "Exported revision " "$logDir/$logFileName" | awk -F "[. ]" '{print $3}'`
	svn cp -r $svnTagNumber -m "add tag $svnTagNumber by $svnUserName" --username=$svnUserName --password=$svnUserPasswd "$svnCodePath" "$svnTagBasePath/$finalBuildNumber"
}

function verifyCompileResult(){
	#�������Ƿ�ɹ�
	#cd /compileDir
	indi=`python determineIfCompileSuccess.py "$logFileName" "$archiveOutputDir" "$platName"`
	if [ "$indi"x = "0"x ]
	then
		#����յĺ͸���Ŀ¼
		cd $archiveOutputDir
		rm -rf $(find $archiveOutputDir -type d -empty)
		thisBuildDir=`ls -t $archiveOutputDir | awk '{if(NR==1)print $1}'`
		mv $archiveOutputDir/$thisBuildDir $archiveOutputDir/$finalBuildNumber
		echo 0
	else
		echo 125
	fi
}

function triggerFrontApkBuild(){
	wget --auth-no-challenge --http-user="wei.yan" --http-password="08919871031c9682e353356caa8e1089" --secure-protocol=TLSv1 -O - "http://192.168.0.34:8080/jenkins/job/SmartParking_2.0_front_apk_build_docker_tester/build?token=ffff3333"
}

function main(){
	#����������һЩ���ýű����ڵ�·��(��Ŀ¼�°��������е��õ�һЩpython/shell�ű�)
	cd $rootDir

	#��������������ɱ���
    getBuildNumber
	triggerFrontApkBuild
	createDir
	createDockerContainer
	monitorDockerContainer
	printLog
	createTag
    
	indicator=`verifyCompileResult`
	if [ "$indicator"x = "0"x ]
	then
		exit 0
	else
		exit 125
	fi
}

main