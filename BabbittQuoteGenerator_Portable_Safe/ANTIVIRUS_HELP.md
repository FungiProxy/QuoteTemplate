# Windows Defender / Antivirus Issues

If the executable gets deleted by Windows Defender or other antivirus software, here's how to fix it:

## Quick Fix (Recommended):
1. **Right-click on PowerShell** and select **"Run as Administrator"**
2. Navigate to this folder: `cd "C:\path\to\this\folder"`
3. Run this command: `Add-MpPreference -ExclusionPath (Get-Location).Path`
4. Copy the executable back from the original `dist` folder

## Manual Fix Through Windows Settings:
1. Open **Windows Security** (Windows Defender)
2. Go to **"Virus & threat protection"**
3. Click **"Manage settings"** under "Virus & threat protection settings"
4. Scroll down to **"Exclusions"**
5. Click **"Add or remove exclusions"**
6. Click **"Add an exclusion"** → **"Folder"**
7. Select this entire folder

## Why This Happens:
- PyInstaller executables are sometimes flagged as suspicious
- This is a **"false positive"** - the file is completely safe
- The executable is built from legitimate Python code
- Adding exclusions prevents future automatic deletions

## Prevention for Your Friend:
When sharing this with others, include these instructions:
1. **Before running**: Add the folder to antivirus exclusions
2. **After copying**: Don't run immediately - set up exclusions first
3. **If deleted**: Use the steps above to restore and protect

## Alternative Approach:
If antivirus continues to be problematic:
- Run the application from the development environment
- Use the Python source code directly instead of the executable
- Consider code signing (for professional distribution)

## Testing the Fix:
After adding exclusions:
1. Copy `BabbittQuoteGenerator.exe` back to this folder
2. Run `Launch.bat` to test
3. The application should start without issues

## Contact:
If problems persist, the application can also be run directly from the Python source code in the development environment. 