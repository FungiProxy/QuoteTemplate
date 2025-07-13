# Babbitt Quote Generator - Automatic Antivirus Protection Setup
# This script automatically requests admin privileges and adds Windows Defender exclusions

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Requesting administrator privileges..." -ForegroundColor Yellow
    Write-Host "Please click YES when prompted." -ForegroundColor Cyan
    
    # Re-run this script with admin privileges
    Start-Process PowerShell -ArgumentList "-ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# Running as administrator - proceed with setup
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "    BABBITT QUOTE GENERATOR - ANTIVIRUS PROTECTION SETUP" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

$currentPath = Split-Path -Parent $MyInvocation.MyCommand.Path

try {
    Write-Host "Adding Windows Defender exclusions..." -ForegroundColor Yellow
    Write-Host ""
    
    # Add folder exclusion
    Add-MpPreference -ExclusionPath $currentPath
    Write-Host "✓ Added folder exclusion: $currentPath" -ForegroundColor Green
    
    # Add process exclusion
    Add-MpPreference -ExclusionProcess "BabbittQuoteGenerator.exe"
    Write-Host "✓ Added process exclusion for BabbittQuoteGenerator.exe" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "🎉 SUCCESS! Windows Defender exclusions added successfully!" -ForegroundColor Green
    Write-Host "Your executable is now protected from deletion." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Double-click Launch.bat to start the application" -ForegroundColor White
    Write-Host "2. Test with sample part: LS2000-15KV-50A-SS-NPT" -ForegroundColor White
    
} catch {
    Write-Host "❌ Error adding exclusions: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "This can happen if:" -ForegroundColor Yellow
    Write-Host "- You didn't click YES for administrator access" -ForegroundColor White
    Write-Host "- Windows Defender is managed by group policy" -ForegroundColor White
    Write-Host "- You're using a different antivirus software" -ForegroundColor White
    Write-Host ""
    Write-Host "Alternative: Add this folder manually to your antivirus exclusions" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Press any key to close..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 