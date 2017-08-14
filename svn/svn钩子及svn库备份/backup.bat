@echo off
setlocal enabledelayedexpansion
set SRC_PATH="C:\Repositories"
set DEST_PATH="\\192.168.0.2\svnbackup"
set DEST_USER="admin"
set DEST_PWD=""

REM ##################分割线####################
net use /y Z: /d
net use /y * /d
net use Z: %DEST_PATH% %DEST_PWD% /user:%DEST_USER%

Z:
set month_=%date:~0,2%
set day_=%date:~3,2%
set year_=%date:~6,4%

set hour_=%time:~0,2%
set min_=%time:~3,2%
set dest_dir=%year_%-%month_%-%day_%-%hour_%-%min_%
set indicator=0

mkdir "%dest_dir%"
for /F "usebackq" %%i in (`dir /B/A:D/O:-D`) do (
set /A indicator+=1
if !indicator! geq 3 rmdir /s/q %%i
)

cd "%dest_dir%"
xcopy /C/E/I/O/Y/K/D "%SRC_PATH%" .\

C:
net use /y Z: /d

setlocal disabledelayedexpansion
