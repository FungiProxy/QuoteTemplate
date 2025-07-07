# QuoteTemplate Environment Activation Script
Write-Host "Initializing QuoteTemplate Environment..." -ForegroundColor Cyan

# Check if virtual environment exists
if (Test-Path "quote_env\Scripts\activate.bat") {
    Write-Host "✓ Virtual environment found" -ForegroundColor Green
    
    # Activate the environment using batch file (more reliable on Windows)
    & "quote_env\Scripts\activate.bat"
    
    Write-Host "✓ Quote Environment Activated" -ForegroundColor Green
    Write-Host "Ready for development!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Available commands:" -ForegroundColor White
    Write-Host "  python main.py           - Run the quote generator" -ForegroundColor Gray
    Write-Host "  pip install package      - Install new packages" -ForegroundColor Gray
    Write-Host "  deactivate              - Exit environment" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "✗ Virtual environment not found" -ForegroundColor Red
    Write-Host "Run 'setup_and_run.bat' first to create the environment" -ForegroundColor Yellow
} 