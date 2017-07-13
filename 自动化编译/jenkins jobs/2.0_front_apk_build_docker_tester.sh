set +x

#前台任务由后台job调用，后台获取本次构建版本号以后即触发前台apk版本构建
#变量定义
platName="Front_Apk"																#构建的模块属性
rootDir="/compileDir"																#公用脚本所在路径
baseDir="/compileDir/SmartParking/TEST/V2.0"										#分支所在的本地根路径
compileDir="/compileDir/SmartParking/TEST/V2.0/Front/apk/code"						#编译代码下载的路径
logDir="/compileDir/SmartParking/TEST/V2.0/Front/apk/log"							#日志保存的路径
archiveOutputDir="/compileDir/SmartParking/TEST/V2.0/Front/apk/archives"			#生成物保存在的路径
imageName="192.168.0.34:5000/build/smartparking-apk-build:lastest"					#构建调用的镜像

#定义版本号
svnTagMainNumber="SmartParkingV2.0.0"												#主版本号
svnTagSecondaryNumber="_b"															#次版本号

#构建的小版本号，为空时使用默认的版本号规则，否则使用该处定义的小版本号
buildNumber="1"

function createDir(){
	#创建本地目录
	#创建编译代码路径并删除该路径下的所有文件
	if [ ! -d $compileDir ] 
	then
		mkdir $compileDir -p
	fi
	rm -rf $compileDir/*
	
	#创建日志保存路径
	if [ ! -d $logDir ] 
	then
		mkdir $logDir -p
	fi
	
	#创建最终生成物保存路径
	if [ ! -d $archiveOutputDir ] 
	then
		mkdir $archiveOutputDir -p
	fi
}

function createDockerContainer(){
	#创建容器
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
	###监视容器
	dockerStatus=`docker inspect --format='{{.State.Status}}' $dockerName`
	timeStat=0
	timeout=0
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
		dockerStatus=`docker inspect --format='{{.State.Status}}' $dockerName 2>/dev/null || echo 12`
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
}

function printLog(){
	#打印日志
	echo "********************************************************"
	echo "********************************************************"
	echo "********************************************************"
	echo "********************************************************"
	echo "***********************以下为日志***********************"
	logFileName=`ls -t $logDir | awk '{if(NR==1) print $1}'`
	echo $logDir/$logFileName
	#前台apk日志文件不需要处理，直接打印
	cat $logDir/$logFileName
}

function getBuildNumber(){
	buildNumber=`cat $baseDir/BuildNumber`
	finalBuildNumber=$svnTagMainNumber$svnTagSecondaryNumber$buildNumber
}

function createTag(){
	#打标签
	svnTagNumber=`grep "Exported revision " "$logDir/$logFileName" | awk -F "[. ]" '{print $3}'`
	svn cp -r $svnTagNumber -m "add tag $svnTagNumber by $svnUserName" --username=$svnUserName --password=$svnUserPasswd "$svnCodePath" "$svnTagBasePath/$finalBuildNumber"
}

function verifyAndMvCompileResult(){
	#检查编译是否成功
	indi=`python determineIfCompileSuccess.py "$logFileName" "$archiveOutputDir" "$platName"`
	if [ "$indi"x = "0"x ]
	then
		#处理空的和改名目录
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
	#进入编译机上一些公用脚本所在的路径(该目录下包含过程中调用的一些python/shell脚本)
	cd $rootDir

	#调用其它函数完成编译
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