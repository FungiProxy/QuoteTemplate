@echo off
title Babbitt Quote Generator - Professional Installer

echo ================================================
echo Babbitt Quote Generator - Professional Edition
echo ================================================
echo.
echo Starting Professional Installer Wizard...
echo.

:: Run the installer wizard
"%~dp0installer_wizard.exe"

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
