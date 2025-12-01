@echo off
:: Coursera Helper v1.0 - Administrator Launcher
:: This script ensures the app runs with administrator privileges

echo.
echo ========================================
echo   Coursera Helper v1.0
echo   Launching with Administrator Rights
echo ========================================
echo.

:: Check for admin rights
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Running as administrator
    echo [*] Starting Coursera Helper...
    echo.
    cd /d "%~dp0"
    call venv\Scripts\activate
    python run.py
    pause
) else (
    echo [!] Not running as administrator
    echo [*] Requesting administrator privileges...
    echo.
    powershell -Command "Start-Process cmd -ArgumentList '/c cd /d \"%~dp0\" && call venv\\Scripts\\activate && python run.py && pause' -Verb RunAs"
)
