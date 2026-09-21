@echo off
cd /d %~dp0..
title 2 - Make today's video
echo.
echo ============================================
echo   MAKING TODAY'S VIDEO (30 to 90 seconds)
echo ============================================
echo.
if not exist .venv\Scripts\python.exe (
    echo  First time here? Double-click "1-SETUP-RUN-ONCE.bat" first.
    echo.
    pause
    exit /b 1
)
.venv\Scripts\python -m agent run
echo.
echo  Your video is ready here:
echo  vishnu folder  >  output  >  posts  >  newest folder  >  video.mp4
echo.
pause
