# Add Windows Defender Exclusion for Babbitt Quote Generator
# Run this as Administrator to prevent Windows Defender from deleting the executable

Write-Host "Adding Windows Defender exclusions for Babbitt Quote Generator..." -ForegroundColor Cyan

try {
    # Add folder exclusion for the portable package
    $portablePath = (Get-Location).Path + "\BabbittQuoteGenerator_Portable"
    Add-MpPreference -ExclusionPath $portablePath
    Write-Host "✓ Added folder exclusion: $portablePath" -ForegroundColor Green
    
    # Add file exclusion for the executable
    $exePath = $portablePath + "\BabbittQuoteGenerator.exe"
    Add-MpPreference -ExclusionPath $exePath
    Write-Host "✓ Added file exclusion: $exePath" -ForegroundColor Green
    
    # Add process exclusion
    Add-MpPreference -ExclusionProcess "BabbittQuoteGenerator.exe"
    Write-Host "✓ Added process exclusion for BabbittQuoteGenerator.exe" -ForegroundColor Green
    
    Write-Host "`n✅ Windows Defender exclusions added successfully!" -ForegroundColor Green
    Write-Host "The executable should now be safe from deletion." -ForegroundColor Yellow
    
} catch {
    Write-Host "❌ Error adding exclusions. Please run as Administrator." -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 