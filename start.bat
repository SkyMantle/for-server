@echo off
cd /d %~dp0
echo Starting Drone Geo-Localization Web Server...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: REM Check if dependencies are installed
:: python -c "import gradio" >nul 2>&1
:: if errorlevel 1 (
::     echo Installing dependencies...
::     python -m pip install -r requirements.txt
::     if errorlevel 1 (
::         echo ERROR: Failed to install dependencies
::         pause
::         exit /b 1
::     )
:: )

echo.
echo ========================================
echo   Drone Geo-Localization Web Server
echo ========================================
echo.
echo Starting server...
echo Access at: http://localhost:7860
echo Press Ctrl+C to stop
echo.

python app.py

pause
