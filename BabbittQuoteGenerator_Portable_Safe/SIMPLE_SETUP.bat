@echo off
title Setup Antivirus Protection
echo.
echo ================================================================
echo          WINDOWS DEFENDER PROTECTION SETUP
echo ================================================================
echo.
echo This will protect the Babbitt Quote Generator from being deleted
echo by Windows Defender or other antivirus software.
echo.
echo You will be asked for Administrator permission - click YES.
echo.
pause

echo Running setup...
powershell -ExecutionPolicy Bypass -File "%~dp0Setup_Protection.ps1"

echo.
echo Setup complete! You can now run Launch.bat to start the application.
pause 