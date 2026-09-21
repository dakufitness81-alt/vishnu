@echo off
cd /d %~dp0..
title 3 - Video from my own idea
echo.
echo ============================================
echo   VIDEO FROM YOUR OWN IDEA
echo ============================================
echo.
if not exist .venv\Scripts\python.exe (
    echo  First time here? Double-click "1-SETUP-RUN-ONCE.bat" first.
    echo.
    pause
    exit /b 1
)
set /p IDEA=Type your video idea in English, then press Enter:
if "%IDEA%"=="" (
    echo  You need to type an idea. Try again.
    pause
    exit /b 1
)
.venv\Scripts\python -m agent run --idea "%IDEA%"
echo.
pause
