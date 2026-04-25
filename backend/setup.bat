@echo off
echo ========================================
echo Shri Krishna Udhav Memorial Trust Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

echo [1/4] Python version:
python --version
echo.

echo [2/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo [3/4] Creating uploads directory...
if not exist uploads mkdir uploads
echo Uploads directory created!
echo.

echo [4/4] Setup complete!
echo.
echo ========================================
echo To start the server, run:
echo   python main.py
echo or
echo   uvicorn main:app --reload --host 0.0.0.0 --port 8000
echo.
echo Access the website at:
echo   http://localhost:8000
echo.
echo API Documentation at:
echo   http://localhost:8000/docs
echo ========================================
pause
