# Babbitt Quote Generator - Antivirus-Safe Portable Version

## 🚨 IMPORTANT: Antivirus Protection Setup

**Before using this application, please add it to your antivirus exclusions to prevent deletion.**

### Quick Setup (30 seconds):

**Option 1: Automatic Setup (Easiest)**
1. **Double-click `Setup_Antivirus_Protection.bat`**
2. **Click "YES"** when Windows asks for administrator permission
3. **Done!** Your executable is now protected.

**Option 2: PowerShell Setup**
1. **Right-click `Setup_Protection.ps1`** → **"Run with PowerShell"**
2. **Click "YES"** when prompted for admin access
3. **Done!** Your executable is now protected.

**Option 3: Manual Setup**
1. **Right-click on PowerShell** and select **"Run as Administrator"**
2. **Navigate to this folder** in PowerShell
3. **Run:** `Add-MpPreference -ExclusionPath (Get-Location).Path`
4. **Done!** Your executable is now protected.

## 🚀 How to Use

### Option 1: Easy Launch (Recommended)
- **Double-click `Launch.bat`** - This will check for issues and start the app

### Option 2: Direct Launch
- **Double-click `BabbittQuoteGenerator.exe`** directly

## 📁 What's Included

- `BabbittQuoteGenerator.exe` (21.3 MB) - Main application
- `Launch.bat` - Smart launcher with error checking
- `Setup_Antivirus_Protection.bat` - **Automatic antivirus setup (just double-click!)**
- `Setup_Protection.ps1` - PowerShell version of antivirus setup
- `ANTIVIRUS_HELP.md` - Detailed antivirus troubleshooting guide
- `README.md` - This file with complete instructions
- `USER_GUIDE.md` - Application user documentation
- `data/` - Product configuration files
- `database/` - Quote database (SQLite)
- `templates/` - Word document templates for all product series

## ✅ System Requirements

- **Windows 10 or later**
- **No Python installation required** (completely portable)
- **20+ MB free disk space**

## 🧪 Test the Application

Try entering this sample part number: **`LS2000-15KV-50A-SS-NPT`**

The application will:
- Parse the part number automatically
- Generate pricing information
- Create a professional quote
- Allow export to Word document

## 🛡️ If Antivirus Deletes the Executable

**Don't panic!** This is common with Python executables. Here's what to do:

1. **Check `ANTIVIRUS_HELP.md`** for detailed instructions
2. **Add folder to exclusions** (see setup above)
3. **Copy the executable back** from the original package
4. **The application is completely safe** - it's just a false positive

## 📋 Product Series Supported

Templates included for:
- **FS10000 Series**
- **LS2000/LS2100 Series**
- **LS6000 Series**
- **LS7000/LS7000-2 Series**
- **LS8000/LS8000-2 Series**
- **LT9000 Series**

## 📞 Troubleshooting

### Application Won't Start:
1. Check if `BabbittQuoteGenerator.exe` exists in this folder
2. If missing, restore from original package
3. Add antivirus exclusions (see setup above)
4. Try running `Launch.bat` for better error messages

### Database Issues:
- The application creates its own database if none exists
- Existing quotes are stored in `database/quotes.db`

### Template Issues:
- All Word templates are in the `templates/` folder
- If missing, copy from the original package

## 🎯 For Developers

This portable package was created from the main QuoteTemplate project using PyInstaller. The executable includes:
- Complete Python runtime
- All required dependencies (python-docx, pydantic, colorama)
- Embedded data files and templates
- SQLite database engine

## 📧 Sharing This Package

When sharing with others:
1. **Include the entire folder** (not just the .exe)
2. **Share the antivirus setup instructions**
3. **Recommend setting up exclusions BEFORE first run**

---

**The application is ready to use! Start with `Launch.bat` for the best experience.** 