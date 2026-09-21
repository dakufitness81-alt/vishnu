@echo off
REM One-time setup for Windows — run in a cmd window inside the vishnu folder:
REM   setup.bat
cd /d %~dp0

echo - Setting up Python environment...
python -m venv .venv
if errorlevel 1 (
    echo.
    echo ERROR: Python was not found.
    echo Install it from https://www.python.org/downloads/
    echo and tick "Add python.exe to PATH" during install.
    pause
    exit /b 1
)

echo - Installing packages (this takes 1-2 minutes)...
.venv\Scripts\pip install --quiet --upgrade pip
.venv\Scripts\pip install --quiet -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: package installation failed. Check your internet and try again.
    pause
    exit /b 1
)

echo.
echo Done! Next steps:
echo    1) Edit config.yaml  -  set your handle
echo    2) .venv\Scripts\python -m agent init
echo    3) .venv\Scripts\python -m agent run --dry-run
pause
