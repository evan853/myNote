set +x

#变量
cd /compileDir
##编译时代码下载的路径
compileDir=""
##编译时需要的 docker 镜像名称
imageName=192.168.0.34:5000/build/smartparking-back-build:lastest
##编译时输出日志的路径
logDir=""
##编译时最终版本文件拷贝到的路径
archiveOutputDir=""
##容器超时等待时间
timeout=0

#本地创建目录
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

#创建容器
dockerName=`python getContainerName.py`
docker run -itd --name $dockerName --net=host -v $compileDir:/compileDir -v $logDir:/logDir -v $archiveOutputDir:/outputDir $imageName

while [ "$stat"x = "0"x ]
do
	dockerName=`python getContainerName.py`
    docker run -itd --name $dockerName --net=host -v $compileDir:/compileDir -v $logDir:/logDir -v $archiveOutputDir:/outputDir $imageName
    stat=$?
done

dockerStatus=`docker inspect --format='{{.State.Status}}' $dockerName`

###监视容器
timeStat=0
while [ "$dockerStatus"x = "running"x ]
do	
	if [ $timeout -gt 30 ]
    	then
        	echo "等待时间过长，超过了30分钟，结束任务！"
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
    	echo "容器已不存在，结束任务！"
    	break
    fi
    if [ "$dockerStatus"x != "running"x ]
    then
    	echo "容器已退出，结束任务"
        docker rm -f $dockerName
    fi
done

#打印日志
echo "********************************************************"
echo "********************************************************"
echo "********************************************************"
echo "********************************************************"
echo "***********************以下为日志***********************"
logFileName=`ls -t $logDir | awk '{if(NR==1) print $1}'`
echo $logDir/$logFileName
python processLogFile.py "$logDir/$logFileName"

#处理空的和旧的存放目录
cd $archiveOutputDir
rm -rf $(find -type d -empty)
rm -rf $(ls -t | awk '{if(NR>5) print $1}')

#检查编译是否成功
cd /compileDir
indi=`python determineIfCompileSuccess.py "$logFileName" "$archiveOutputDir"`
if [ "$indi"x = "0"x ]
then
	exit 0
else
	exit 125
fi