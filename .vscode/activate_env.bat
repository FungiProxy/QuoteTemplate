@echo off
echo Initializing QuoteTemplate Environment...

if exist "quote_env\Scripts\activate.bat" (
    echo ✓ Virtual environment found
    call quote_env\Scripts\activate.bat
    echo ✓ Quote Environment Activated
    echo.
    echo Available commands:
    echo   python main.py           - Run the quote generator
    echo   pip install package      - Install new packages  
    echo   deactivate              - Exit environment
    echo.
) else (
    echo ✗ Virtual environment not found
    echo Run 'setup_and_run.bat' first to create the environment
) 