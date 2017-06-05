@echo off


for /F "delims=." %%a in ('dir /B *.txt') do (

echo [>%%a_result.txt
echo {>>%%a_result.txt
echo "type": "polyline",>>%%a_result.txt
echo "id": 3,>>%%a_result.txt
echo "latlngs": [>>%%a_result.txt

for /F "tokens=1,2 delims=," %%i in (%%a.txt) do (
	echo {>>%%a_result.txt
	echo 	"lat": %%j,>>%%a_result.txt
	echo 	"lng": %%i>>%%a_result.txt
	echo },>>%%a_result.txt
)

echo ]>>%%a_result.txt
echo }>>%%a_result.txt
echo ]>>%%a_result.txt

)
