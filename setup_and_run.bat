@echo off
title Babbitt Quote Generator Setup

echo ================================================
echo Babbitt Quote Generator Environment Setup
echo ================================================
echo.

:: Check if virtual environment exists
if not exist "quote_env" (
    echo Creating virtual environment...
    python -m venv quote_env
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo Make sure Python is installed and in PATH
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
    echo.
)

:: Activate virtual environment
echo Activating virtual environment...
call quote_env\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

:: Check if requirements.txt exists and install
if exist "requirements.txt" (
    echo Installing/updating requirements...
    pip install -r requirements.txt
    echo.
)

:: Check if project structure exists
if not exist "main.py" (
    echo Creating basic project structure...
    
    :: Create directories
    mkdir config 2>nul
    mkdir database 2>nul
    mkdir core 2>nul
    mkdir gui 2>nul
    mkdir export 2>nul
    mkdir utils 2>nul
    
    :: Create basic main.py
    echo # Babbitt Quote Generator > main.py
    echo print("Babbitt Quote Generator - Ready to start development!") >> main.py
    echo.
)

echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo Virtual environment is now active.
echo You can now:
echo   - Install packages with: pip install package_name
echo   - Run the app with: python main.py
echo   - Deactivate with: deactivate
echo.
echo Starting Command Prompt with activated environment...
echo.

:: Keep command prompt open with activated environment
cmd /k 