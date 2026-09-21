@echo off
cd /d %~dp0..
title 6 - Connect X (Twitter)
echo.
echo ============================================
echo   CONNECT YOUR X (TWITTER) ACCOUNT
echo ============================================
echo.
echo  This will open a link in your browser.
echo  Approve it, then paste the code you see here.
echo.
echo  (If it says "set X_CLIENT_ID", follow the X steps
echo   in READ-ME-FIRST.txt first.)
echo.
if not exist .venv\Scripts\python.exe (
    echo  First time here? Double-click "1-SETUP-RUN-ONCE.bat" first.
    echo.
    pause
    exit /b 1
)
.venv\Scripts\python -m agent auth x
echo.
pause
