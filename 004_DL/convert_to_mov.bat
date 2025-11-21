@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set "input=%~1"
if "%input%"=="" (
    echo MP4ファイルをこのbatにドラッグ＆ドロップしてください。
    pause
    exit /b
)

set "filename=%~n1"
set "filepath=%~dp1"
set "ffmpeg_path=%~dp0ffmpeg\bin\ffmpeg.exe"
set "output=%filepath%%filename%.mov"

echo 変換中... (VP9 → H.264)
"%ffmpeg_path%" -i "%input%" -c:v libx264 -c:a aac "%output%"

echo.
echo 変換完了！ 出力: "%output%"
pause
