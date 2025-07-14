@echo off
title Quick Build - Babbitt Quote Generator

echo ================================================
echo Quick Build - Babbitt Quote Generator
echo ================================================
echo.

:: Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

:: Build executable
echo Building executable...
pyinstaller --onefile --windowed --name BabbittQuoteGenerator main.py

if %errorlevel% neq 0 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo ================================================
echo Build Complete!
echo ================================================
echo.
echo Executable: dist\BabbittQuoteGenerator.exe
echo.
echo You can now test the application.
echo.
pause 