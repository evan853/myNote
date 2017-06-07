#!/bin/bash

BACKUP_DIR=//192.168.0.11/Shares/Ist/REDMINE_BACKUP/data_backup
BACKUP_DIR_LOCAL_MOUNT_DIR=/opt/redmine_backup
BACKUP_DATE_DIR=`date +%Y%m%d%H%M%S`
BACKUP_USER_NAME=
BACKUP_USER_PASSWORD=

STORE_DAYS=3

REDMINE_ATTACHMENTS=/opt/redmine-3.3.1-0/apps/redmine/htdocs/files

MYSQL_USERNAME=bitnami
MYSQL_PASSWORD=66c18b5bac
MYSQL_DATABASE_NAME=bitnami_redmine
MYSQL_COMMOND=/opt/redmine-3.3.1-0/mysql/bin/mysqldump
MYSQL_SQL_BACKUP_FILE=bitnami_redmine.sql

if [ -d $BACKUP_DIR_LOCAL_MOUNT_DIR ]
then
umount $BACKUP_DIR_LOCAL_MOUNT_DIR 
else 
mkdir $BACKUP_DIR_LOCAL_MOUNT_DIR
fi
((STORE_DAYS-=1))

mount -o username=$BACKUP_USER_NAME,password=$BACKUP_USER_PASSWORD $BACKUP_DIR $BACKUP_DIR_LOCAL_MOUNT_DIR
cd $BACKUP_DIR_LOCAL_MOUNT_DIR

rm -rf `ls -t | awk -v d=$STORE_DAYS '{if (FNR>d) print $1}'`
mkdir $BACKUP_DIR_LOCAL_MOUNT_DIR/$BACKUP_DATE_DIR
cd $BACKUP_DIR_LOCAL_MOUNT_DIR/$BACKUP_DATE_DIR

$MYSQL_COMMOND -u$MYSQL_USERNAME -p$MYSQL_PASSWORD $MYSQL_DATABASE_NAME >$MYSQL_SQL_BACKUP_FILE
cp $REDMINE_ATTACHMENTS/* ./ -r
