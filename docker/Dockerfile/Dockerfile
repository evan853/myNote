#安装了expect,jdk,gradle,android-sdk,svn,python的基础镜像
FROM ey853/centos7.0.5:final-1.0

#安装android-sdk
RUN echo y | /usr/android-sdk/tools/android update sdk --no-ui --all --filter build-tools-25.0.2

#变量
ENV JAVA_HOME /usr/java/jdk1.8.0_121
ENV CLASSPATH .:$JAVA_HOME/lib/tools.jar
ENV PATH /usr/gradle-2.10/bin:/usr/gradle/gradle-3.4/bin:$JAVA_HOME/bin:$PATH

#拷贝签名store文件
ADD SmartParking.keystore /key/SmartParking.keystore
ADD compile.sh /compileScript/compile.sh
#ADD signature.sh /compileScript/signature.sh

#增加入口脚本
ENTRYPOINT /compileScript/compile.sh
