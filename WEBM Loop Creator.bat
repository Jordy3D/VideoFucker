@ECHO OFF
TITLE Bane's WEBM Loop Creator

SET infile="%~1"

ECHO Enter times to loop input file. -1 is infinite and you will need to cancel manually. // Default: 10
SET /p loopcount="Enter loop count:" || SET "loopcount=10"

IF "%loopcount%" == "-1" (
	ECHO This will end up with a VERY large file VERY quickly. You have been warned.
	PAUSE
)

ffmpeg -i %infile% -c:v libvpx-vp9 -strict -2 -c:a libopus TEMP_FILE.mp4
ffmpeg -y -stream_loop %loopcount% -i TEMP_FILE.mp4 -c copy %~n1.webm

DEL TEMP_FILE.mp4