# Development Guide - Working with Portable Version

## 🎯 **Best Approach for Editing**

### **Current Setup:**
- ✅ **Source Code**: Available in main project directory
- ✅ **Portable Executable**: Working perfectly (includes all libraries)
- ⚠️ **Python GUI**: Needs Tcl/Tk fix for development

### **Recommended Workflow:**

## 📝 **For Making Edits:**

### **Step 1: Edit Source Code**
```bash
# Use your preferred editor (VS Code, Notepad++, etc.)
# Edit files in the main project directory:
# - main.py
# - gui/main_window.py
# - core/quote_generator.py
# - etc.
```

### **Step 2: Test Changes**
```bash
# Option A: Test core functionality (no GUI required)
py tests\test_app.py

# Option B: Test with Python (if Tcl/Tk is fixed)
py main.py

# Option C: Build and test portable version
py build_installer.py
```

### **Step 3: Build New Portable Version**
```bash
# After making changes, rebuild the portable version
py build_installer.py
```

## 🛠️ **Development Tools**

### **Quick Development Menu:**
```bash
# Run the development workflow
dev_workflow.bat
```

### **Individual Commands:**
```bash
# Test core functionality
py tests\test_app.py

# Build portable version
py build_installer.py

# Run portable version
.\BabbittQuoteGenerator_Portable\BabbittQuoteGenerator.exe

# Open project folder
explorer .
```

## 📁 **Key Files for Editing**

### **Main Application Files:**
- `main.py` - Application entry point
- `gui/main_window.py` - Main GUI window
- `core/quote_generator.py` - Quote generation logic
- `core/part_parser.py` - Part number parsing
- `core/pricing_engine.py` - Pricing calculations

### **Configuration Files:**
- `config/settings.py` - Application settings
- `config/database_config.py` - Database configuration
- `data/` - JSON data files for pricing, materials, etc.

### **Template Files:**
- `export/templates/` - Word document templates
- `export/word_exporter.py` - Word document generation

## 🔄 **Development Cycle**

### **1. Make Changes**
- Edit source code in your preferred editor
- Focus on the specific files you need to modify

### **2. Test Core Logic**
```bash
py tests\test_app.py
```
This tests the core functionality without requiring the GUI.

### **3. Test Full Application**
```bash
# If Tcl/Tk is fixed:
py main.py

# Or use portable version:
.\BabbittQuoteGenerator_Portable\BabbittQuoteGenerator.exe
```

### **4. Build Updated Version**
```bash
py build_installer.py
```

## 🎯 **Specific Editing Scenarios**

### **Editing Pricing Logic:**
1. Edit `core/pricing_engine.py`
2. Edit `data/*.json` files for pricing data
3. Test with `py tests\test_app.py`
4. Build new portable version

### **Editing GUI:**
1. Edit `gui/main_window.py`
2. Edit `gui/` submodules
3. Test with portable version (since Python GUI has Tcl/Tk issue)
4. Build new portable version

### **Editing Templates:**
1. Edit `export/templates/*.docx` files
2. Edit `export/word_exporter.py` if needed
3. Test quote generation with `py tests\test_app.py`
4. Build new portable version

### **Editing Database:**
1. Edit `database/` files
2. Edit `config/database_config.py`
3. Test database connection with `py tests\test_app.py`
4. Build new portable version

## 🚀 **Quick Commands Reference**

```bash
# Development workflow
dev_workflow.bat

# Test core functionality
py tests\test_app.py

# Build portable version
py build_installer.py

# Run portable version
run_app.bat

# Open project folder
explorer .
```

## 💡 **Tips for Efficient Development**

1. **Use the test suite** (`py tests\test_app.py`) for quick testing of core logic
2. **Use the portable version** for GUI testing until Tcl/Tk is fixed
3. **Build frequently** to ensure your changes work in the portable version
4. **Keep backups** of working versions before major changes
5. **Test core functionality** before testing the full GUI

## 🔧 **Fixing Tcl/Tk for Better Development**

If you want to fix the Tcl/Tk issue for easier development:

1. **Follow the TCL_TK_FIX_GUIDE.md**
2. **Use Anaconda** (includes Tcl/Tk by default)
3. **Reinstall Python** with Tcl/Tk support

But remember: **The portable version works perfectly** and includes all necessary libraries!

## ✅ **Success Indicators**

- Core functionality tests pass: `py tests\test_app.py`
- Portable version builds successfully: `py build_installer.py`
- Changes appear in the portable executable
- No errors in the test output

This workflow allows you to edit efficiently while using the portable version for testing and deployment! 