@echo off
title BabbittQuoteGenerator v1.0.0 - Professional Installer

echo ================================================
echo BabbittQuoteGenerator - Professional Edition v1.0.0
echo ================================================
echo.
echo Professional Quote Generator for Babbitt International
echo.

:: Check for admin privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: This installer requires administrator privileges.
    echo Please right-click and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

:: Set installation directory
set INSTALL_DIR=C:\Program Files\BabbittQuoteGenerator
echo Installing to: %INSTALL_DIR%
echo.

:: Create installation directory
if not exist "%INSTALL_DIR%" (
    echo Creating installation directory...
    mkdir "%INSTALL_DIR%"
) else (
    echo Installation directory already exists.
)

:: Copy application files
echo Installing application files...
copy "BabbittQuoteGenerator.exe" "%INSTALL_DIR%\" >nul
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy application files.
    pause
    exit /b 1
)

:: Copy supporting files
echo Copying supporting files...
copy "uninstall.bat" "%INSTALL_DIR%\" >nul
copy "README.txt" "%INSTALL_DIR%\" >nul
copy "LICENSE.txt" "%INSTALL_DIR%\" >nul
copy "version.json" "%INSTALL_DIR%\" >nul

:: Create desktop shortcut
echo Creating desktop shortcut...
set SHORTCUT="%USERPROFILE%\Desktop\BabbittQuoteGenerator.lnk"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut(%SHORTCUT%); $Shortcut.TargetPath = '%INSTALL_DIR%\BabbittQuoteGenerator.exe'; $Shortcut.Description = 'BabbittQuoteGenerator - Professional Quote Generator'; $Shortcut.Save()" >nul 2>&1

:: Create start menu shortcut
echo Creating start menu shortcut...
set START_MENU_DIR="%APPDATA%\Microsoft\Windows\Start Menu\Programs\BabbittQuoteGenerator"
if not exist %START_MENU_DIR% mkdir %START_MENU_DIR%
set START_MENU="%APPDATA%\Microsoft\Windows\Start Menu\Programs\BabbittQuoteGenerator\BabbittQuoteGenerator.lnk"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut(%START_MENU%); $Shortcut.TargetPath = '%INSTALL_DIR%\BabbittQuoteGenerator.exe'; $Shortcut.Description = 'BabbittQuoteGenerator - Professional Quote Generator'; $Shortcut.Save()" >nul 2>&1

:: Add to registry for uninstall
echo Adding to Windows registry...
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\BabbittQuoteGenerator" /v "DisplayName" /t REG_SZ /d "BabbittQuoteGenerator" /f >nul
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\BabbittQuoteGenerator" /v "UninstallString" /t REG_SZ /d "%INSTALL_DIR%\uninstall.bat" /f >nul
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\BabbittQuoteGenerator" /v "DisplayVersion" /t REG_SZ /d "1.0.0" /f >nul
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\BabbittQuoteGenerator" /v "Publisher" /t REG_SZ /d "Babbitt International" /f >nul
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\BabbittQuoteGenerator" /v "InstallLocation" /t REG_SZ /d "%INSTALL_DIR%" /f >nul
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\BabbittQuoteGenerator" /v "EstimatedSize" /t REG_DWORD /d 25000 /f >nul

echo.
echo ================================================
echo Installation Complete!
echo ================================================
echo.
echo BabbittQuoteGenerator v1.0.0 has been successfully installed.
echo.
echo You can now run the application from:
echo - Desktop shortcut
echo - Start Menu
echo - %INSTALL_DIR%\BabbittQuoteGenerator.exe
echo.
echo To uninstall, use Control Panel > Programs and Features
echo or run: %INSTALL_DIR%\uninstall.bat
echo.
pause
