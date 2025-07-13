# Enhanced Portable Package Creator with Antivirus Compatibility
# This version is designed to be more antivirus-friendly

param(
    [switch]$AddDefenderExclusion = $false
)

$TargetDir = "BabbittQuoteGenerator_Portable_Safe"

Write-Host "Creating antivirus-safe portable package..." -ForegroundColor Green

# Remove existing directory
if (Test-Path $TargetDir) {
    Remove-Item -Recurse -Force $TargetDir
}
New-Item -ItemType Directory -Name $TargetDir -Force | Out-Null

# Copy the main executable with a different approach
if (Test-Path "dist/BabbittQuoteGenerator.exe") {
    # Copy and immediately add to Windows Defender exclusion if requested
    Copy-Item "dist/BabbittQuoteGenerator.exe" -Destination $TargetDir
    Write-Host "✓ Copied main executable" -ForegroundColor Green
    
    if ($AddDefenderExclusion) {
        try {
            $exePath = (Get-Location).Path + "\$TargetDir\BabbittQuoteGenerator.exe"
            Add-MpPreference -ExclusionPath $exePath
            Write-Host "✓ Added Windows Defender exclusion" -ForegroundColor Green
        } catch {
            Write-Host "⚠ Could not add Defender exclusion (run as Admin for this)" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "✗ Main executable not found in dist/" -ForegroundColor Red
    exit 1
}

# Copy essential files
Copy-Item -Path "data" -Destination $TargetDir -Recurse -Force
Write-Host "✓ Copied data files" -ForegroundColor Green

if (Test-Path "database/quotes.db") {
    New-Item -ItemType Directory -Path "$TargetDir/database" -Force | Out-Null
    Copy-Item "database/quotes.db" -Destination "$TargetDir/database/"
    Write-Host "✓ Copied database" -ForegroundColor Green
}

# Copy documentation
$docs = @("USER_GUIDE.md", "README.md", "QUICK_DEPLOYMENT_GUIDE.md")
foreach ($doc in $docs) {
    if (Test-Path $doc) {
        Copy-Item $doc -Destination $TargetDir
        Write-Host "✓ Copied $doc" -ForegroundColor Green
    }
}

# Copy templates
if (Test-Path "export/templates") {
    New-Item -ItemType Directory -Path "$TargetDir/templates" -Force | Out-Null
    Get-ChildItem "export/templates/*.docx" -ErrorAction SilentlyContinue | ForEach-Object {
        Copy-Item $_.FullName -Destination "$TargetDir/templates/"
    }
    Write-Host "✓ Copied Word templates" -ForegroundColor Green
}

# Create improved launcher
$launcherContent = @"
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
    echo 2. Run add_defender_exclusion.ps1 as Administrator
    echo 3. Restore the executable from the original package
    echo.
    pause
    exit /b 1
)

rem Start the application
start "" "BabbittQuoteGenerator.exe"

echo Application started successfully!
echo You can close this window.
echo.
pause
"@

$launcherContent | Out-File -FilePath "$TargetDir\Launch.bat" -Encoding ASCII
Write-Host "✓ Created enhanced launcher" -ForegroundColor Green

# Create antivirus help file
$antivirusHelp = @"
# Windows Defender / Antivirus Issues

If the executable gets deleted by Windows Defender or other antivirus:

## Quick Fix:
1. Run PowerShell as Administrator
2. Navigate to this folder
3. Run: .\add_defender_exclusion.ps1

## Manual Fix:
1. Open Windows Security (Windows Defender)
2. Go to Virus & threat protection
3. Click "Manage settings" under Virus & threat protection settings
4. Scroll down to "Exclusions"
5. Click "Add or remove exclusions"
6. Add this entire folder as an exclusion

## Why This Happens:
- PyInstaller executables are often flagged as suspicious
- This is a "false positive" - the file is safe
- Adding exclusions prevents future deletions

## Alternative:
- Run the application directly from the development folder
- Use the Python source code instead of the executable
"@

$antivirusHelp | Out-File -FilePath "$TargetDir\ANTIVIRUS_HELP.md" -Encoding UTF8
Write-Host "✓ Created antivirus help guide" -ForegroundColor Green

# Copy the defender exclusion script
Copy-Item "add_defender_exclusion.ps1" -Destination $TargetDir -ErrorAction SilentlyContinue

Write-Host "`n🎉 Enhanced portable package created: $TargetDir" -ForegroundColor Cyan
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Run as Administrator: .\add_defender_exclusion.ps1" -ForegroundColor White
Write-Host "2. Test the application with .\Launch.bat" -ForegroundColor White
Write-Host "3. Share the entire folder with your friend" -ForegroundColor White 