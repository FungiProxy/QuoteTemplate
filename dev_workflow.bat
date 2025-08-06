@echo off
echo Babbitt Quote Generator - Development Workflow
echo ==============================================
echo.
echo Choose an option:
echo 1. Fix Tcl/Tk for direct Python development (RECOMMENDED)
echo 2. Edit source code (opens in default editor)
echo 3. Test with Python (if Tcl/Tk is fixed)
echo 4. Test core functionality (no GUI required)
echo 5. Build new portable version
echo 6. Run portable version
echo 7. Open project folder
echo.
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" (
    echo.
    echo =================================
    echo FIXING TCL/TK FOR DIRECT DEVELOPMENT
    echo =================================
    echo.
    echo Choose your fix method:
    echo 1. Reinstall Python with Tcl/Tk support (RECOMMENDED)
    echo 2. Install Anaconda (includes Tcl/Tk)
    echo 3. Quick Tcl/Tk copy (if you have Tcl/Tk installed)
    echo.
    set /p fix_choice="Enter choice (1-3): "
    
    if "%fix_choice%"=="1" (
        echo.
        echo Reinstalling Python with Tcl/Tk support:
        echo 1. Download Python 3.13.x from python.org
        echo 2. Run installer as Administrator
        echo 3. Select "Customize installation"
        echo 4. Make sure "tcl/tk and IDLE" is CHECKED
        echo 5. Install to a clean directory
        echo.
        echo After installation, test with:
        echo py -c "import tkinter; root = tkinter.Tk(); root.destroy(); print('SUCCESS!')"
        echo.
        echo Opening Python download page...
        start https://www.python.org/downloads/
    ) else if "%fix_choice%"=="2" (
        echo.
        echo Installing Anaconda is recommended:
        echo 1. Go to https://www.anaconda.com/download
        echo 2. Download and install Anaconda
        echo 3. Open Anaconda Prompt and run:
        echo    conda create -n quotetemplate python=3.11
        echo    conda activate quotetemplate
        echo    pip install python-docx==0.8.11 colorama==0.4.6 pyinstaller
        echo    python main.py
        echo.
        start https://www.anaconda.com/download
    ) else if "%fix_choice%"=="3" (
        echo Running Tcl/Tk copy script...
        call copy_tcl_tk.bat
    ) else (
        echo Invalid choice.
    )
) else if "%choice%"=="2" (
    echo Opening project folder for editing...
    explorer .
) else if "%choice%"=="3" (
    echo Testing with Python version...
    py main.py
) else if "%choice%"=="4" (
    echo Testing core functionality...
    py tests\test_app.py
) else if "%choice%"=="5" (
    echo Building new portable version...
    py build_installer.py
) else if "%choice%"=="6" (
    echo Running portable version...
    .\BabbittQuoteGenerator_Portable\BabbittQuoteGenerator.exe
) else if "%choice%"=="7" (
    echo Opening project folder...
    explorer .
) else (
    echo Invalid choice. Please run again.
)

pause 