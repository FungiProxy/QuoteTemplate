@echo off
title Babbitt Quote Generator
echo.
echo ================================================
echo    BABBITT QUOTE GENERATOR - PORTABLE VERSION
echo ================================================
echo.
echo Starting application...
echo.

rem Check if executable exists
if not exist "BabbittQuoteGenerator.exe" (
    echo ERROR: BabbittQuoteGenerator.exe not found!
    echo This may have been deleted by antivirus software.
    echo.
    echo SOLUTIONS:
    echo 1. Add this folder to Windows Defender exclusions
    echo 2. Run PowerShell as Administrator and execute:
    echo    Add-MpPreference -ExclusionPath "%CD%"
    echo 3. Restore the executable from the original package
    echo.
    pause
    exit /b 1
)

rem Start the application
echo Launching Babbitt Quote Generator...
start "" "BabbittQuoteGenerator.exe"

echo.
echo Application started successfully!
echo You can close this window or keep it open for troubleshooting.
echo.
pause 