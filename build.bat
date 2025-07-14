@echo off
title Babbitt Quote Generator - Build Script

echo ================================================
echo Babbitt Quote Generator - Professional Build
echo ================================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is required to build the application.
    echo Please install Python 3.8 or later and try again.
    echo.
    pause
    exit /b 1
)

:: Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip is required to install dependencies.
    echo Please ensure pip is installed with Python.
    echo.
    pause
    exit /b 1
)

:: Install/upgrade build dependencies
echo Installing build dependencies...
pip install --upgrade pip
pip install --upgrade pyinstaller
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies.
    echo Please check your internet connection and try again.
    echo.
    pause
    exit /b 1
)

:: Run the build script
echo.
echo Starting build process...
python build_installer.py

if %errorlevel% neq 0 (
    echo.
    echo Build failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ================================================
echo Build completed successfully!
echo ================================================
echo.
echo Generated files:
echo - dist\BabbittQuoteGenerator.exe (Standalone executable)
echo - dist\BabbittQuoteGenerator_Setup.exe (Installer)
echo - dist\BabbittQuoteGenerator_Portable.zip (Portable version)
echo.
echo You can now distribute these files to users.
echo.
pause 