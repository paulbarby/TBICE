@echo off
echo ==========================================
echo Image Converter - Windows Build Script
echo ==========================================
echo.

:: Check for Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or newer and try again
    pause
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist venv\ (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Error creating virtual environment
        pause
        exit /b 1
    )
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install dependencies
echo Installing required packages...
pip install -r requirements.txt
pip install pyinstaller

:: Run build script
echo Building executable...
python build_exe.py

:: Check if build was successful
if exist dist\ImageConverter.exe (
    echo.
    echo ==========================================
    echo Build successful!
    echo.
    echo The executable has been created at:
    echo dist\ImageConverter.exe
    echo ==========================================
) else (
    echo.
    echo ==========================================
    echo Build failed. Please check the output above for errors.
    echo ==========================================
)

:: Deactivate virtual environment
call venv\Scripts\deactivate.bat

echo.
pause