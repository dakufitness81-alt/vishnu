@echo off
cd /d %~dp0..
title 1 - Setup (first time only)
echo.
echo ============================================
echo   SETUP - first time only (1 to 3 minutes)
echo ============================================
echo.

REM Find Python (prefer the "py" launcher, then "python")
set "PYCMD="
py -3 --version >nul 2>&1
if not errorlevel 1 set "PYCMD=py -3"
if not defined PYCMD (
    python --version >nul 2>&1
    if not errorlevel 1 set "PYCMD=python"
)
if not defined PYCMD (
    echo.
    echo  Python was NOT found on this computer. Please do this once:
    echo.
    echo   1. Open this link:  https://www.python.org/downloads/
    echo   2. Click the yellow "Download Python" button
    echo   3. Run the downloaded file. IMPORTANT: tick the box
    echo      "Add python.exe to PATH" at the bottom of the first screen
    echo   4. Click "Install Now"
    echo   5. Then double-click THIS file again
    echo.
    pause
    exit /b 1
)

echo  Python found. Downloading free tools (please wait)...
%PYCMD% -m venv .venv
.venv\Scripts\pip install --quiet --upgrade pip
.venv\Scripts\pip install --quiet -r requirements.txt
if errorlevel 1 (
    echo.
    echo  Something failed while installing. Check your internet
    echo  connection and double-click this file again.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   DONE! Setup finished.
echo.
echo   Next step:
echo   1. Open config.yaml in Notepad, put your handle
echo   2. Double-click "2-MAKE-VIDEO.bat"
echo ============================================
echo.
pause
