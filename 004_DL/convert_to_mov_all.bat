@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo mp4 → MOV 一括変換
echo.

set "ffmpeg_path=%~dp0ffmpeg\bin\ffmpeg.exe"

REM 現在のディレクトリにある *.mp4 をすべて処理
for %%f in ("%~dp0*.mp4") do (
    set "input=%%f"
    set "filename=%%~nf"
    set "filepath=%%~dpf"
    set "output=%%~dpf!filename!.mov"

    echo 変換中: %%f → !filename!.mov
    "%ffmpeg_path%" -i "%%f" -c:v libx264 -c:a aac "!output!"
    echo.
)

echo すべての変換が完了しました！
pause
