@echo off
title Babbitt Quote Generator - Professional Installer

echo ================================================
echo Babbitt Quote Generator - Professional Edition
echo ================================================
echo.
echo Starting Professional Installer Wizard...
echo.

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is required to run the installer.
    echo Please install Python 3.7 or later and try again.
    echo.
    pause
    exit /b 1
)

:: Run the installer wizard
python "%~dp0installer_wizard.py"

if %errorlevel% neq 0 (
    echo.
    echo Installation failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ================================================
echo Installation Complete!
echo ================================================
echo.
echo The Babbitt Quote Generator has been installed successfully.
echo.
echo You can now run the application from:
echo - Desktop shortcut
echo - Start Menu
echo - Program Files directory
echo.
pause
