@echo off
pip install -r requirements.txt
setlocal

rem Define the URL of the YouTube video
set /p URL="Enter the YouTube video URL: "

rem Define the download path (you can change this path)
set DOWNLOAD_PATH=%~dp0downloads

rem Check if the download path exists, if not, create it
if not exist "%DOWNLOAD_PATH%" (
    mkdir "%DOWNLOAD_PATH%"
)

rem Download the YouTube video using yt-dlp
yt-dlp.exe -o "%DOWNLOAD_PATH%\%%(title)s.%%(ext)s" %URL%

rem Notify the user of completion
echo Download completed. Video saved to "%DOWNLOAD_PATH%"
pause
endlocal
