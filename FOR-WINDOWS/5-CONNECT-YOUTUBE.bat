@echo off
cd /d %~dp0..
title 5 - Connect YouTube
echo.
echo ============================================
echo   CONNECT YOUR YOUTUBE CHANNEL
echo ============================================
echo.
echo  This will open a link in your browser.
echo  Approve it, then paste the code you see here.
echo.
echo  (If it says "no credentials", follow the YouTube
echo   steps in READ-ME-FIRST.txt first.)
echo.
if not exist .venv\Scripts\python.exe (
    echo  First time here? Double-click "1-SETUP-RUN-ONCE.bat" first.
    echo.
    pause
    exit /b 1
)
.venv\Scripts\python -m pip install --quiet google-api-python-client google-auth-httplib2 google-auth-oauthlib
.venv\Scripts\python -m agent auth youtube
echo.
pause
