@echo off

set REPOS="%1"
set TXN="%2"
set /A MAX_SIZE=1*1024*1024

cd.>C:\Repositories\test\hooks\size.txt
cd.>C:\Repositories\test\hooks\file.txt

for /F "tokens=1,* usebackq" %%i in (`svnlook changed "%REPOS%" -t "%TXN%"`) do (
echo %%j >>C:\Repositories\test\hooks\file.txt
svnlook filesize "%REPOS%" "%%j" -t "%TXN%" >>C:\Repositories\test\hooks\size.txt
)

for /F %%i in ("C:\Repositories\test\hooks\size.txt") do (
if %%i gtr %MAX_SIZE% goto BIG_FILE
)


:EOF
exit 0

:MESSAGE_ERROR
echo "LOG ERROR:  log !!!!!!" 1>&2
exit 1

:NOT_SUPERUSER
echo "PERMISSION ERROR:  permission!!!!!!!" 1>&2
exit 1

:BIG_FILE
echo "BIG FILE: you have committed a big file" 1>&2
exit 1