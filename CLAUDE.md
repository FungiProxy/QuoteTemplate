# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Running the Application
```bash
# Run from source (requires Python with Tcl/Tk)
python main.py

# Test with development workflow menu
dev_workflow.bat

# Run portable version (recommended for testing)
.\BabbittQuoteGenerator_Portable\BabbittQuoteGenerator.exe
```

### Building and Deployment
```bash
# Build standalone executable and installer
python build_installer.py

# Quick build without full installer
python simple_build.py

# Test core functionality without GUI
python test_*.py  # Various test files for specific features
```

### Development Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Fix Tcl/Tk issues for GUI development (Windows)
dev_workflow.bat  # Option 1 for guided fix

# Verify database setup
python check_database.py
python verify_databases.py
```

## Code Architecture

### Core Application Structure
- **main.py**: Application entry point, handles initialization and error checking
- **gui/main_window.py**: Primary GUI interface using tkinter
- **core/**: Business logic modules
  - `quote_generator.py`: Quote document generation using python-docx
  - `part_parser.py`: Babbitt part number parsing and validation
  - `pricing_engine.py`: Pricing calculations and rules
  - `spare_parts_manager.py`: Spare parts handling
- **database/**: SQLite database management
  - `db_manager.py`: Core database operations
  - `models.py`: Data models and schemas
  - `quotes.db` and `customers.db`: SQLite databases
- **export/**: Word document export functionality
  - `word_exporter.py`: Document generation
  - `word_template_processor.py`: Template processing
  - `templates/`: Word template files for different product lines

### Key Design Patterns
- **Modular Architecture**: Each major function (parsing, pricing, export) is separated into distinct modules
- **Database Abstraction**: Database operations are centralized in `db_manager.py`
- **Template System**: Word templates are dynamically populated based on part type (LS2000, LS7000, etc.)
- **Multi-Item Support**: Quotes can contain multiple parts with individual pricing

### Important Development Notes
- **Tcl/Tk Dependency**: GUI requires proper Tcl/Tk installation for development
- **Portable Build**: The application can be built as a standalone executable that includes all dependencies
- **Database Initialization**: Application checks for database files at startup and runs in demo mode if not found
- **Template-Based Export**: Quote output uses Word templates in `export/templates/` directory
- **Part Number Format**: Babbitt parts follow format `[Series][Size][Material][Options][Insulator][Length]`

### Testing Strategy
- Individual test files for specific features (e.g., `test_housing_codes.py`, `test_insulator_length_pricing.py`)
- Core functionality can be tested without GUI using various test_*.py files
- Database verification tools: `check_database.py`, `verify_databases.py`

### Build Process
- Uses PyInstaller for creating standalone executables
- Includes installer creation with `build_installer.py`
- Supports both full installer and portable versions
- Template files and databases are included in the build

### Dependencies
- **python-docx**: Word document generation
- **colorama**: Console output formatting
- **pydantic**: Data validation
- **pyinstaller**: Executable building
- **tkinter**: GUI framework (requires Tcl/Tk)