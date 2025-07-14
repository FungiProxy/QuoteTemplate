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

:: Create installation directory
set INSTALL_DIR=C:\Program Files\BabbittQuoteGenerator
echo Installing to: %INSTALL_DIR%
echo.

:: Create directory if it doesn't exist
if not exist "%INSTALL_DIR%" (
    echo Creating installation directory...
    mkdir "%INSTALL_DIR%"
)

:: Copy application files
echo Installing application files...
copy "BabbittQuoteGenerator.exe" "%INSTALL_DIR%\" >nul
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy application files.
    pause
    exit /b 1
)

:: Create desktop shortcut
echo Creating desktop shortcut...
set SHORTCUT="%USERPROFILE%\Desktop\BabbittQuoteGenerator.lnk"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut(%SHORTCUT%); $Shortcut.TargetPath = '%INSTALL_DIR%\BabbittQuoteGenerator.exe'; $Shortcut.Description = 'BabbittQuoteGenerator - Professional Quote Generator'; $Shortcut.Save()" >nul 2>&1

:: Create start menu shortcut
echo Creating start menu shortcut...
set START_MENU="%APPDATA%\Microsoft\Windows\Start Menu\Programs\BabbittQuoteGenerator.lnk"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut(%START_MENU%); $Shortcut.TargetPath = '%INSTALL_DIR%\BabbittQuoteGenerator.exe'; $Shortcut.Description = 'BabbittQuoteGenerator - Professional Quote Generator'; $Shortcut.Save()" >nul 2>&1

:: Add to registry for uninstall
echo Adding to Windows registry...
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\BabbittQuoteGenerator" /v "DisplayName" /t REG_SZ /d "BabbittQuoteGenerator" /f >nul
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\BabbittQuoteGenerator" /v "UninstallString" /t REG_SZ /d "%INSTALL_DIR%\uninstall.bat" /f >nul
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\BabbittQuoteGenerator" /v "DisplayVersion" /t REG_SZ /d "1.0.0" /f >nul
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\BabbittQuoteGenerator" /v "Publisher" /t REG_SZ /d "Babbitt International" /f >nul
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\BabbittQuoteGenerator" /v "InstallLocation" /t REG_SZ /d "%INSTALL_DIR%" /f >nul

:: Create uninstall script
echo Creating uninstall script...
set UNINSTALL_SCRIPT=@echo off
set UNINSTALL_SCRIPT=%UNINSTALL_SCRIPT%^
echo Removing BabbittQuoteGenerator...
set UNINSTALL_SCRIPT=%UNINSTALL_SCRIPT%^
if exist "%USERPROFILE%\Desktop\BabbittQuoteGenerator.lnk" del "%USERPROFILE%\Desktop\BabbittQuoteGenerator.lnk"
set UNINSTALL_SCRIPT=%UNINSTALL_SCRIPT%^
if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\BabbittQuoteGenerator.lnk" del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\BabbittQuoteGenerator.lnk"
set UNINSTALL_SCRIPT=%UNINSTALL_SCRIPT%^
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\BabbittQuoteGenerator" /f >nul 2>&1
set UNINSTALL_SCRIPT=%UNINSTALL_SCRIPT%^
if exist "%INSTALL_DIR%" rmdir /s /q "%INSTALL_DIR%"
set UNINSTALL_SCRIPT=%UNINSTALL_SCRIPT%^
echo BabbittQuoteGenerator has been uninstalled.
set UNINSTALL_SCRIPT=%UNINSTALL_SCRIPT%^
pause

echo %UNINSTALL_SCRIPT% > "%INSTALL_DIR%\uninstall.bat"

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
echo.
pause
