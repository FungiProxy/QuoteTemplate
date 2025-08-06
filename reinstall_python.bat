@echo off
echo Python Reinstallation Guide
echo ===========================
echo.
echo This will help you reinstall Python with Tcl/Tk support.
echo.
echo IMPORTANT: Make sure to check "tcl/tk and IDLE" during installation!
echo.
echo Steps:
echo 1. Download Python 3.13.x from python.org
echo 2. Run installer as Administrator
echo 3. Select "Customize installation"
echo 4. Make sure "tcl/tk and IDLE" is CHECKED
echo 5. Install to a clean directory
echo.
echo Opening Python download page...
start https://www.python.org/downloads/
echo.
echo After installation, test with:
echo py -c "import tkinter; root = tkinter.Tk(); root.destroy(); print('SUCCESS!')"
echo.
echo If successful, you can then run:
echo py main.py
echo.
pause 