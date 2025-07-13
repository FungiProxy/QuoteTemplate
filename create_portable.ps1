# Simple Portable Package Creator for Babbitt Quote Generator
# This creates a minimal portable package with just the essentials

$TargetDir = "BabbittQuoteGenerator_Portable"

Write-Host "Creating portable package..." -ForegroundColor Green

# Copy the main executable
if (Test-Path "dist/BabbittQuoteGenerator.exe") {
    Copy-Item "dist/BabbittQuoteGenerator.exe" -Destination $TargetDir
    Write-Host "✓ Copied main executable" -ForegroundColor Green
} else {
    Write-Host "✗ Main executable not found" -ForegroundColor Red
}

# Copy data files (essential for the app to work)
if (Test-Path "data") {
    Copy-Item -Path "data" -Destination $TargetDir -Recurse -Force
    Write-Host "✓ Copied data files" -ForegroundColor Green
}

# Copy database if it exists
if (Test-Path "database/quotes.db") {
    New-Item -ItemType Directory -Path "$TargetDir/database" -Force | Out-Null
    Copy-Item "database/quotes.db" -Destination "$TargetDir/database/"
    Write-Host "✓ Copied database" -ForegroundColor Green
}

# Copy essential documentation
$docs = @("USER_GUIDE.md", "README.md", "QUICK_DEPLOYMENT_GUIDE.md")
foreach ($doc in $docs) {
    if (Test-Path $doc) {
        Copy-Item $doc -Destination $TargetDir
        Write-Host "✓ Copied $doc" -ForegroundColor Green
    }
}

# Copy Word templates if they exist
if (Test-Path "export/templates") {
    New-Item -ItemType Directory -Path "$TargetDir/templates" -Force | Out-Null
    Get-ChildItem "export/templates/*.docx" -ErrorAction SilentlyContinue | ForEach-Object {
        Copy-Item $_.FullName -Destination "$TargetDir/templates/"
    }
    if (Get-ChildItem "$TargetDir/templates/*.docx" -ErrorAction SilentlyContinue) {
        Write-Host "✓ Copied Word templates" -ForegroundColor Green
    }
}

# Create a simple launcher batch file
$launcherContent = "@echo off`necho Starting Babbitt Quote Generator...`nBabbittQuoteGenerator.exe`npause"

$launcherContent | Out-File -FilePath "$TargetDir\Launch.bat" -Encoding ASCII
Write-Host "✓ Created launcher batch file" -ForegroundColor Green

Write-Host "`nPortable package created successfully at: $TargetDir" -ForegroundColor Cyan
Write-Host "Package contents:" -ForegroundColor Yellow
Get-ChildItem $TargetDir -Recurse | Select-Object Name, Length | Format-Table -AutoSize 