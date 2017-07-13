set +x

#ǰ̨�����ɺ�̨job���ã���̨��ȡ���ι����汾���Ժ󼴴���ǰ̨apk�汾����
#��������
platName="Front_Apk"																#������ģ������
rootDir="/compileDir"																#���ýű�����·��
baseDir="/compileDir/SmartParking/TEST/V2.0"										#��֧���ڵı��ظ�·��
compileDir="/compileDir/SmartParking/TEST/V2.0/Front/apk/code"						#����������ص�·��
logDir="/compileDir/SmartParking/TEST/V2.0/Front/apk/log"							#��־�����·��
archiveOutputDir="/compileDir/SmartParking/TEST/V2.0/Front/apk/archives"			#�����ﱣ���ڵ�·��
imageName="192.168.0.34:5000/build/smartparking-apk-build:lastest"					#�������õľ���

#����汾��
svnTagMainNumber="SmartParkingV2.0.0"												#���汾��
svnTagSecondaryNumber="_b"															#�ΰ汾��

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
	#ǰ̨apk��־�ļ�����Ҫ����ֱ�Ӵ�ӡ
	cat $logDir/$logFileName
}

function getBuildNumber(){
	buildNumber=`cat $baseDir/BuildNumber`
	finalBuildNumber=$svnTagMainNumber$svnTagSecondaryNumber$buildNumber
}

function createTag(){
	#���ǩ
	svnTagNumber=`grep "Exported revision " "$logDir/$logFileName" | awk -F "[. ]" '{print $3}'`
	svn cp -r $svnTagNumber -m "add tag $svnTagNumber by $svnUserName" --username=$svnUserName --password=$svnUserPasswd "$svnCodePath" "$svnTagBasePath/$finalBuildNumber"
}

function verifyAndMvCompileResult(){
	#�������Ƿ�ɹ�
	indi=`python determineIfCompileSuccess.py "$logFileName" "$archiveOutputDir" "$platName"`
	if [ "$indi"x = "0"x ]
	then
		#����յĺ͸���Ŀ¼
		cd $archiveOutputDir
		rm -rf $(find -type d -empty)
		thisBuildDir=`ls -t | awk '{if(NR==1)print $1}'`
		mv $thisBuildDir $finalBuildNumber
		echo 0
	else
		echo 125
	fi
}

function main(){
	#����������һЩ���ýű����ڵ�·��(��Ŀ¼�°��������е��õ�һЩpython/shell�ű�)
	cd $rootDir

	#��������������ɱ���
    getBuildNumber
	createDir
	createDockerContainer
	monitorDockerContainer
	printLog
    
	indicator=`verifyAndMvCompileResult`
	if [ "$indicator"x = "0"x ]
	then
		exit 0
	else
		exit 125
	fi
}

main