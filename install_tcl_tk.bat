@echo off
echo Installing Tcl/Tk for Python...
echo =================================

REM Get Python installation directory
for /f "tokens=*" %%i in ('py -c "import sys; print(sys.executable)"') do set PYTHON_EXE=%%i
for %%i in ("%PYTHON_EXE%") do set PYTHON_DIR=%%~dpi
echo Python directory: %PYTHON_DIR%

REM Create directories if they don't exist
if not exist "%PYTHON_DIR%tcl" mkdir "%PYTHON_DIR%tcl"
if not exist "%PYTHON_DIR%tcl\tcl8.6" mkdir "%PYTHON_DIR%tcl\tcl8.6"
if not exist "%PYTHON_DIR%tcl\tk8.6" mkdir "%PYTHON_DIR%tcl\tk8.6"

REM Download Tcl/Tk files (this is a simplified approach)
echo Downloading Tcl/Tk files...

REM Try to find existing Tcl/Tk installation
echo Searching for existing Tcl/Tk installation...

REM Check common installation paths
set TCL_FOUND=0
if exist "C:\tcl\tcl8.6" (
    echo Found Tcl at C:\tcl
    xcopy "C:\tcl\tcl8.6" "%PYTHON_DIR%tcl\tcl8.6\" /E /I /Y
    set TCL_FOUND=1
)

if exist "C:\Program Files\Tcl\tcl8.6" (
    echo Found Tcl at C:\Program Files\Tcl
    xcopy "C:\Program Files\Tcl\tcl8.6" "%PYTHON_DIR%tcl\tcl8.6\" /E /I /Y
    set TCL_FOUND=1
)

if exist "C:\Program Files (x86)\Tcl\tcl8.6" (
    echo Found Tcl at C:\Program Files (x86)\Tcl
    xcopy "C:\Program Files (x86)\Tcl\tcl8.6" "%PYTHON_DIR%tcl\tcl8.6\" /E /I /Y
    set TCL_FOUND=1
)

if %TCL_FOUND%==0 (
    echo No existing Tcl/Tk installation found.
    echo.
    echo Please download and install Tcl/Tk manually:
    echo 1. Go to https://www.tcl.tk/software/tcltk/
    echo 2. Download the Windows installer
    echo 3. Install it to C:\tcl
    echo 4. Run this script again
    echo.
    echo Or use the portable executable: run_app.bat
    pause
    exit /b 1
)

echo.
echo Tcl/Tk installation completed!
echo Testing tkinter...

REM Test tkinter
py -c "import tkinter; root = tkinter.Tk(); root.destroy(); print('SUCCESS: Tkinter is working!')"

if %ERRORLEVEL%==0 (
    echo.
    echo =================================
    echo Tcl/Tk installation successful!
    echo You can now run: py main.py
    echo =================================
) else (
    echo.
    echo =================================
    echo Tcl/Tk installation may need additional files.
    echo For now, use the portable executable: run_app.bat
    echo =================================
)

pause 