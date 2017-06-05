@echo off
setlocal enabledelayedexpansion

set /a n=0
for /F %%a in ('dir /B *.txt') do set /a n+=1

echo [>result.ini

set /a ind=0

for /F %%a in ('dir /B *.txt') do (
	set /a ind+=1
	echo {>>result.ini
	echo "type": "polyline",>>result.ini
	echo "id": 3,>>result.ini
	echo "latlngs": [>>result.ini
	
	set /a inn=0
	set /a inind=0
	for /F %%i in (%%a) do set /a inn+=1

	for /F "tokens=1,2 delims=," %%i in (%%a) do (
		set /a inind+=1
		echo {>>result.ini
		echo 	"lat": %%j,>>result.ini
		echo 	"lng": %%i>>result.ini
		if !inind! neq !inn! (
			echo },>>result.ini
		) else (
			echo }>>result.ini
		)
	)

	echo ]>>result.ini
	if !ind! neq !n! (
		echo },>>result.ini
	) else (
		echo }>>result.ini
	)
)

echo ]>>result.ini

setlocal disabledelayedexpansion
