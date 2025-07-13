# PowerShell script to create a portable package for Babbitt Quote Generator
# Run this from the project root

$TargetDir = "BabbittQuoteGenerator_Portable"

# Remove existing portable folder if it exists
if (Test-Path $TargetDir) {
    Remove-Item -Recurse -Force $TargetDir
}

# List of files to copy
$files = @(
    "dist/BabbittQuoteGenerator.exe",
    "dist/launcher.exe",
    "dist/update_manager.exe",
    "USER_GUIDE.md",
    "INSTALLER_GUIDE.md",
    "QUICK_DEPLOYMENT_GUIDE.md"
)

# List of folders to copy
$folders = @(
    "data",
    "database",
    "config",
    "core",
    "gui",
    "utils",
    "export",
    "docs"
)

# Copy files
foreach ($file in $files) {
    if (Test-Path $file) {
        Copy-Item $file -Destination $TargetDir -Force
    }
}

# Function to copy folders recursively, skipping __pycache__ and *.pyc
function Copy-Folder($src, $dst) {
    if (!(Test-Path $src)) { return }
    Get-ChildItem -Path $src -Recurse | ForEach-Object {
        $rel = $_.FullName.Substring($src.Length)
        $target = Join-Path $dst $rel
        if ($_.PSIsContainer) {
            if ($_.Name -eq "__pycache__") { return }
            if (!(Test-Path $target)) { New-Item -ItemType Directory -Path $target | Out-Null }
        } else {
            if ($_.Name -like "*.pyc") { return }
            $parent = Split-Path $target -Parent
            if (!(Test-Path $parent)) { New-Item -ItemType Directory -Path $parent | Out-Null }
            Copy-Item $_.FullName -Destination $target -Force
        }
    }
}

# Copy folders
foreach ($folder in $folders) {
    if (Test-Path $folder) {
        Copy-Folder (Resolve-Path $folder).Path (Join-Path $TargetDir $folder)
    }
}

Write-Host "Portable package created at: $TargetDir" -ForegroundColor Green 