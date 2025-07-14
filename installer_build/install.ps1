# Self-Extracting Installer for BabbittQuoteGenerator v1.0.0
param([string]$ExtractPath = "$env:TEMP\BabbittQuoteGenerator_Install")

# Create extraction directory
if (!(Test-Path $ExtractPath)) {
    New-Item -ItemType Directory -Path $ExtractPath | Out-Null
}

# Extract embedded files
$files = @(
    "BabbittQuoteGenerator.exe",
    "install.bat",
    "README.txt",
    "LICENSE.txt",
    "version.json"
)

foreach ($file in $files) {
    $content = Get-Content "$PSScriptRoot\$file" -Raw
    Set-Content "$ExtractPath\$file" -Value $content
}

# Run installer
Set-Location $ExtractPath
& "install.bat"

# Cleanup
Remove-Item $ExtractPath -Recurse -Force
