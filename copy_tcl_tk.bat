@echo off
echo Quick Tcl/Tk Copy Script
echo ========================

REM Get Python directory
for /f "tokens=*" %%i in ('py -c "import sys; print(sys.executable)"') do set PYTHON_EXE=%%i
for %%i in ("%PYTHON_EXE%") do set PYTHON_DIR=%%~dpi
echo Python directory: %PYTHON_DIR%

REM Create tcl directory
if not exist "%PYTHON_DIR%tcl" mkdir "%PYTHON_DIR%tcl"

REM Check for Tcl/Tk installation
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
    echo.
    echo No Tcl/Tk installation found!
    echo.
    echo Please install Tcl/Tk first:
    echo 1. Go to https://www.tcl.tk/software/tcltk/
    echo 2. Download "Tcl/Tk 8.6.x for Windows"
    echo 3. Install to C:\tcl
    echo 4. Run this script again
    echo.
    echo OR install Anaconda (recommended):
    echo 1. Go to https://www.anaconda.com/download
    echo 2. Install Anaconda (includes Tcl/Tk)
    echo 3. Create environment: conda create -n quotetemplate python=3.11
    echo.
    pause
    exit /b 1
)

echo.
echo Tcl/Tk files copied successfully!
echo Testing tkinter...

REM Test tkinter
py -c "import tkinter; root = tkinter.Tk(); root.destroy(); print('SUCCESS: Tkinter is working!')"

if %ERRORLEVEL%==0 (
    echo.
    echo =================================
    echo Tcl/Tk fix successful!
    echo You can now run: py main.py
    echo =================================
) else (
    echo.
    echo =================================
    echo Tcl/Tk may need additional files.
    echo Try installing Anaconda instead.
    echo =================================
)

pause 