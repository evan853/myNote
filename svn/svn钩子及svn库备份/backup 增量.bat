@echo off


set SRC_PATH="C:\Repositories"
set DEST_PATH="\\192.168.0.6\SVN_Backup\192.168.0.37"
set DEST_USER="administrator"
set DEST_PWD="Istuary88"

REM ##################分割线####################
net use /y Z: /d
net use /y * /d
net use Z: %DEST_PATH% %DEST_PWD% /user:%DEST_USER%

xcopy /C/E/I/Y/D list Z:\

Z:
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