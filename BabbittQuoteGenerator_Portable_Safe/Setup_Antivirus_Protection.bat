@echo off
title Babbitt Quote Generator - Antivirus Protection Setup
color 0A
echo.
echo ================================================================
echo    BABBITT QUOTE GENERATOR - ANTIVIRUS PROTECTION SETUP
echo ================================================================
echo.
echo This script will add Windows Defender exclusions to protect
echo the executable from being deleted by antivirus software.
echo.
echo YOU WILL BE PROMPTED FOR ADMINISTRATOR PERMISSION
echo Please click "YES" when Windows asks for permission.
echo.
pause

echo.
echo Adding Windows Defender exclusions...
echo.

rem Request admin privileges and run PowerShell command (fixed syntax)
powershell -Command "& {Start-Process PowerShell -ArgumentList '-ExecutionPolicy Bypass -Command \"$currentPath = Split-Path -Parent $MyInvocation.MyCommand.Path; Write-Host Adding Windows Defender exclusions... -ForegroundColor Cyan; try { Add-MpPreference -ExclusionPath $currentPath; Write-Host Successfully added folder exclusion: $currentPath -ForegroundColor Green; Add-MpPreference -ExclusionProcess BabbittQuoteGenerator.exe; Write-Host Successfully added process exclusion for BabbittQuoteGenerator.exe -ForegroundColor Green; Write-Host; Write-Host Windows Defender exclusions added successfully! -ForegroundColor Green; Write-Host Your executable is now protected from deletion. -ForegroundColor Yellow; } catch { Write-Host Error adding exclusions: $($_.Exception.Message) -ForegroundColor Red; Write-Host Please ensure you clicked YES for administrator access. -ForegroundColor Yellow; } Write-Host; Write-Host Press any key to close...; $null = $Host.UI.RawUI.ReadKey(NoEcho,IncludeKeyDown)\"' -Verb RunAs}"

if %errorlevel% equ 0 (
    echo.
    echo Protection setup completed!
    echo You can now safely run the Babbitt Quote Generator.
    echo.
    echo Next steps:
    echo 1. Run Launch.bat to start the application
    echo 2. Test with sample part number: LS2000-15KV-50A-SS-NPT
) else (
    echo.
    echo There may have been an issue with the setup.
    echo Please try running Setup_Protection.ps1 instead.
    echo Or manually add this folder to Windows Defender exclusions.
)

echo.
pause 