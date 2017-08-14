@echo off


set SRC_PATH="C:\Repositories"
set DEST_PATH="\\192.168.0.11\Shares\Ist\SVN_CODE_BACKUP\192.168.0.37"
set DEST_USER="wei.yan"
set DEST_PWD="HXwl337"

REM ##################分割线####################
set date_=%date:~0,10%
set time_=%time:~0,5%
net use /y Z: /d
net use /y * /d
net use Z: %DEST_PATH% %DEST_PWD% /user:%DEST_USER%

if exist Z: (
	xcopy /C/E/I/Y/D list Z:\
	Z:
) else (
	echo You have opened a shared path locally!     TIME: %date_% %time_%>>error.log
	exit 1
)

if not exist today mkdir today
if not exist yesterday mkdir yesterday

ren today tmp
ren yesterday today
ren tmp yesterday
cd today

xcopy /C/E/I/Y/D "%SRC_PATH%"\groups.conf .\
xcopy /C/E/I/Y/D "%SRC_PATH%"\VisualSVN-GlobalWinAuthz.ini .\
xcopy /C/E/I/Y/D "%SRC_PATH%"\htpasswd .\

for /F %%i in (..\list) do (
rmdir /S/Q %%i\db\transactions
rmdir /S/Q %%i\db\txn-protorevs
rmdir /S/Q %%i\locks
xcopy /C/E/I/Y/D "%SRC_PATH%"\%%i .\%%i
)

C:
net use /y Z: /d