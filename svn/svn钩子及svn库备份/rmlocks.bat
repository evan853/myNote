@echo off
set REPO_PATH="C:\Repositories\test"

cd. >path_need_to_be_delete.txt

for /F "tokens=*" %%i in ('svnadmin lslocks %REPO_PATH%') do (
echo %%i | find "Path: /" >nul 2>&1 && echo %%i>>path_need_to_be_delete.txt
)

echo This is the begin:
echo.
for /F "tokens=1,* delims=: " %%i in (path_need_to_be_delete.txt) do (
svnadmin rmlocks %REPO_PATH% "%%j" >nul 2>&1
echo unlock %%j 
)

echo.
echo All have been done!
pause >nul
