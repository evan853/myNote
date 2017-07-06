#!/bin/bash
workspace="/compileDir/PRODUCT/PROJECT/MODULE"
logDir="log"
codeDir="code"
archiveDir="archives"

if [ ! -d $workspace/$logDir ]; then mkdir $workspace/$logDir; fi
if [ ! -d $workspace/$codeDir ]; then mkdir $workspace/$codeDir; fi
if [ ! -d $workspace/$archiveDir ]; then mkdir $workspace/$archiveDir; fi

#cp determineIfCompileSuccess.py /compileDir/
#cp getContainerName.py /compileDir/
#cp processLogFile.py /compileDir/
#cp statTime.py /compileDir/