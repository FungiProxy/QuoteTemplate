@echo off
echo Starting Babbitt Quote Generator...
cd /d "%~dp0"
if exist "BabbittQuoteGenerator_Portable\BabbittQuoteGenerator.exe" (
    start "" "BabbittQuoteGenerator_Portable\BabbittQuoteGenerator.exe"
) else (
    echo Error: BabbittQuoteGenerator.exe not found!
    echo Please make sure the portable version is available.
    pause
) 