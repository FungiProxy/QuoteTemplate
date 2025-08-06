# Editing with Portable Version - Quick Guide

## 🎯 **The Best Approach**

### **Current Situation:**
- ✅ **Source Code**: Available for editing
- ✅ **Portable Executable**: Works perfectly (includes all libraries)
- ⚠️ **Python GUI**: Needs Tcl/Tk fix

### **Recommended Workflow:**

## 📝 **Step-by-Step Editing Process**

### **1. Make Your Edits**
```bash
# Edit source code in your preferred editor
# Key files to edit:
# - main.py
# - gui/main_window.py  
# - core/quote_generator.py
# - core/pricing_engine.py
# - data/*.json (pricing data)
# - export/templates/*.docx (templates)
```

### **2. Test Your Changes**
```bash
# Test core functionality (no GUI required)
py tests\test_app.py

# This tests: part parsing, pricing, database, Word export
```

### **3. Build New Portable Version**
```bash
# Build updated portable executable
py build_installer.py
```

### **4. Test Full Application**
```bash
# Run the new portable version
.\dist\BabbittQuoteGenerator.exe
# OR
.\BabbittQuoteGenerator_Portable\BabbittQuoteGenerator.exe
```

## 🚀 **Quick Commands**

```bash
# Development menu
dev_workflow.bat

# Test core functionality
py tests\test_app.py

# Build portable version
py build_installer.py

# Run portable version
run_app.bat
```

## 💡 **Key Points**

1. **Edit source code** in the main project directory
2. **Test with `py tests\test_app.py`** for quick validation
3. **Build new portable version** after changes
4. **Use portable executable** for full testing
5. **The portable version includes all libraries** - no Tcl/Tk issues!

## ✅ **Success Checklist**

- [ ] Core functionality tests pass: `py tests\test_app.py`
- [ ] New portable version builds: `py build_installer.py`
- [ ] Changes work in portable executable
- [ ] No errors in test output

## 🎯 **What You Can Edit**

- **Pricing logic**: `core/pricing_engine.py`, `data/*.json`
- **GUI**: `gui/main_window.py` and submodules
- **Templates**: `export/templates/*.docx`
- **Database**: `database/` files, `config/database_config.py`
- **Part parsing**: `core/part_parser.py`

**The portable version gives you full functionality while you edit the source code!** 