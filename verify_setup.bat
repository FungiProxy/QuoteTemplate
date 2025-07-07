@echo off
title QuoteTemplate Setup Verification

echo ================================================
echo QuoteTemplate Environment Verification
echo ================================================
echo.

:: Check if .vscode directory exists
if exist ".vscode" (
    echo ✓ .vscode configuration directory found
) else (
    echo ✗ .vscode directory missing
    goto :error
)

:: Check if settings.json exists
if exist ".vscode\settings.json" (
    echo ✓ Cursor/VS Code settings configured
) else (
    echo ✗ settings.json missing
    goto :error
)

:: Check if activation scripts exist
if exist ".vscode\activate_env.bat" (
    echo ✓ Batch activation script found
) else (
    echo ✗ Batch activation script missing
    goto :error
)

if exist ".vscode\activate_env.ps1" (
    echo ✓ PowerShell activation script found
) else (
    echo ✗ PowerShell activation script missing
    goto :error
)

:: Check if virtual environment exists
if exist "quote_env" (
    echo ✓ Virtual environment directory found
    if exist "quote_env\Scripts\python.exe" (
        echo ✓ Python executable found in virtual environment
    ) else (
        echo ✗ Python executable missing in virtual environment
        echo   Run setup_and_run.bat to fix this
        goto :error
    )
) else (
    echo ✗ Virtual environment not found
    echo   Run setup_and_run.bat to create it
    goto :error
)

:: Test activation
echo.
echo Testing environment activation...
call quote_env\Scripts\activate.bat
if errorlevel 1 (
    echo ✗ Failed to activate virtual environment
    goto :error
) else (
    echo ✓ Virtual environment activation successful
)

:: Test Python and packages
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python not accessible
    goto :error
) else (
    echo ✓ Python accessible
)

echo.
echo ================================================
echo ✓ Setup Verification PASSED
echo ================================================
echo.
echo Your environment is ready! 
echo New terminals in Cursor will automatically:
echo   - Activate the quote_env virtual environment
echo   - Set the correct Python interpreter
echo   - Show helpful commands
echo.
echo To test, open a new terminal in Cursor and you should see
echo the environment activation message.
echo.
pause
exit /b 0

:error
echo.
echo ================================================
echo ✗ Setup Verification FAILED
echo ================================================
echo.
echo Please run setup_and_run.bat first to create the environment.
echo.
pause
exit /b 1 