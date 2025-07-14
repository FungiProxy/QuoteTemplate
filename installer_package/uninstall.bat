@echo off
title BabbittQuoteGenerator - Uninstaller

echo ================================================
echo BabbittQuoteGenerator - Uninstaller
echo ================================================
echo.

:: Check for admin privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: This uninstaller requires administrator privileges.
    echo Please right-click and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

set INSTALL_DIR=C:\Program Files\BabbittQuoteGenerator

echo Removing BabbittQuoteGenerator...
echo.

:: Remove shortcuts
echo Removing shortcuts...
if exist "%USERPROFILE%\Desktop\BabbittQuoteGenerator.lnk" (
    del "%USERPROFILE%\Desktop\BabbittQuoteGenerator.lnk"
    echo - Desktop shortcut removed
)

if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\BabbittQuoteGenerator" (
    rmdir /s /q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\BabbittQuoteGenerator"
    echo - Start menu entries removed
)

:: Remove registry entries
echo Removing registry entries...
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\BabbittQuoteGenerator" /f >nul 2>&1
echo - Registry entries removed

:: Remove installation directory
if exist "%INSTALL_DIR%" (
    echo Removing installation files...
    rmdir /s /q "%INSTALL_DIR%"
    echo - Installation directory removed
)

echo.
echo ================================================
echo Uninstallation Complete!
echo ================================================
echo.
echo BabbittQuoteGenerator has been successfully uninstalled.
echo.
pause
