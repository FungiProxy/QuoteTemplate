@echo off
title Babbitt Quote Generator - Development

echo Starting Babbitt Quote Generator...
echo.

:: Activate environment
call quote_env\Scripts\activate.bat

:: Clear screen and show status
cls
echo ================================================
echo Babbitt Quote Generator - Development Mode
echo ================================================
echo.
echo Environment: ACTIVE
echo Project: %CD%
echo.
echo Commands:
echo   python main.py          - Run the application
echo   pip install package     - Install new package
echo   deactivate              - Exit environment
echo.
echo ================================================
echo.

:: Keep command prompt open
cmd /k 