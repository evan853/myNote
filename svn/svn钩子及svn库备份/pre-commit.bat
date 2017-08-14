@echo off

set REPOS="%1"
set TXN="%2"

set rightuser=0

for /f %%i in ('svnlook changed "%REPOS%" -t "%TXN%"') do (
if "%%i"=="D" set operation=%%i
)

for /F "usebackq delims=" %%i in (`svnlook author -t "%TXN%" "%REPOS%"`) do set author=%%i

if "%author%"=="haha" set rightuser=1
if "%author%"=="" set rightuser=1
if "%author%"=="" set rightuser=1
if "%author%"=="" set rightuser=1
if "%author%"=="" set rightuser=1
if "%author%"=="" set rightuser=1
if "%author%"=="" set rightuser=1
if "%author%"=="" set rightuser=1
if "%author%"=="" set rightuser=1
if "%author%"=="" set rightuser=1
if "%author%"=="" set rightuser=1


for /F "usebackq delims=" %%i in (`svnlook log -t "%TXN%" "%REPOS%" ^| findstr "........"`) do set strLog=%%i
if not defined strLog goto MESSAGE_ERROR

if defined operation (if %rightuser%==0 goto NOT_SUPERUSER)





:EOF
exit 0

:MESSAGE_ERROR
echo "LOG ERROR:  You have to enter 8 characters as log message at least!!!!!!" 1>&2
exit 1

:NOT_SUPERUSER
echo "PERMISSION ERROR: You don't have the permission to delete things!!!!!!!" 1>&2
exit 1