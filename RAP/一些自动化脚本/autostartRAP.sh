#!/bin/sh

cd /usr/redis/src
nohup ./redis-server &

sleep 10s

cd /usr/tomcat/bin
./startup.sh
