@echo off
cd /d %~dp0..
title 4 - What did it make?
echo.
if not exist .venv\Scripts\python.exe (
    echo  First time here? Double-click "1-SETUP-RUN-ONCE.bat" first.
    echo.
    pause
    exit /b 1
)
.venv\Scripts\python -m agent status
echo.
pause
