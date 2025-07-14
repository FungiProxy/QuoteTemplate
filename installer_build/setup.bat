@echo off
title BabbittQuoteGenerator v1.0.0 - Self-Extracting Installer

echo ================================================
echo BabbittQuoteGenerator v1.0.0 - Self-Extracting Installer
echo ================================================
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0install.ps1"

if %errorlevel% neq 0 (
    echo Installation failed. Please run as administrator.
    pause
)
