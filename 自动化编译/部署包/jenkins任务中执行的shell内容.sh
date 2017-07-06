set +x

#����
cd /compileDir
##����ʱ�������ص�·��
compileDir=""
##����ʱ��Ҫ�� docker ��������
imageName=192.168.0.34:5000/build/smartparking-back-build:lastest
##����ʱ�����־��·��
logDir=""
##����ʱ���հ汾�ļ���������·��
archiveOutputDir=""
##������ʱ�ȴ�ʱ��
timeout=0

#���ش���Ŀ¼
if [ ! -d $compileDir ] 
then
	mkdir $compileDir -p
fi
rm -rf $compileDir/*

if [ ! -d $logDir ] 
then
	mkdir $logDir -p
fi

if [ ! -d $archiveOutputDir ] 
then
	mkdir $archiveOutputDir -p
fi

#��������
dockerName=`python getContainerName.py`
docker run -itd --name $dockerName --net=host -v $compileDir:/compileDir -v $logDir:/logDir -v $archiveOutputDir:/outputDir $imageName

while [ "$stat"x = "0"x ]
do
	dockerName=`python getContainerName.py`
    docker run -itd --name $dockerName --net=host -v $compileDir:/compileDir -v $logDir:/logDir -v $archiveOutputDir:/outputDir $imageName
    stat=$?
done

dockerStatus=`docker inspect --format='{{.State.Status}}' $dockerName`

###��������
timeStat=0
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
    dockerStatus=`docker inspect --format='{{.State.Status}}' $dockerName 2>nul || echo 12`
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

#��ӡ��־
echo "********************************************************"
echo "********************************************************"
echo "********************************************************"
echo "********************************************************"
echo "***********************����Ϊ��־***********************"
logFileName=`ls -t $logDir | awk '{if(NR==1) print $1}'`
echo $logDir/$logFileName
python processLogFile.py "$logDir/$logFileName"

#����յĺ;ɵĴ��Ŀ¼
cd $archiveOutputDir
rm -rf $(find -type d -empty)
rm -rf $(ls -t | awk '{if(NR>5) print $1}')

#�������Ƿ�ɹ�
cd /compileDir
indi=`python determineIfCompileSuccess.py "$logFileName" "$archiveOutputDir"`
if [ "$indi"x = "0"x ]
then
	exit 0
else
	exit 125
fi