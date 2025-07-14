# Babbitt Quote Generator

Professional Quote Generator for Babbitt International products.

## Overview

The Babbitt Quote Generator is a comprehensive desktop application designed to streamline the quote generation process for Babbitt International products. It provides an intuitive interface for creating, managing, and exporting professional quotes.

## Features

- **Professional Quote Generation**: Create detailed quotes with automatic pricing calculations
- **Customer Management**: Store and manage customer information
- **Employee Management**: Track employee information for quote attribution
- **Part Number Parsing**: Intelligent parsing of Babbitt part numbers
- **Word Document Export**: Export quotes to professional Word documents
- **Database Management**: Built-in SQLite database for data persistence
- **Multi-Item Quotes**: Support for complex quotes with multiple items
- **Spare Parts Management**: Add and manage spare parts in quotes
- **Template System**: Customizable Word templates for different product lines

## System Requirements

- **Operating System**: Windows 10 or later
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 100MB free disk space
- **Display**: 1024x768 minimum resolution

## Installation

### Option 1: Standalone Executable (Recommended)

1. Download the latest release from the releases page
2. Run `BabbittQuoteGenerator_Setup.exe` as administrator
3. Follow the installation wizard
4. Launch from desktop shortcut or start menu

### Option 2: Portable Version

1. Download `BabbittQuoteGenerator_Portable.zip`
2. Extract to any folder
3. Run `run.bat` or `BabbittQuoteGenerator.exe` directly

### Option 3: Python Installation

```bash
# Clone the repository
git clone https://github.com/babbitt/quote-generator.git
cd quote-generator

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Quick Start

1. **Launch the Application**: Start Babbitt Quote Generator
2. **Select User**: Choose your user profile from the dropdown
3. **Select Customer**: Click "Select Customer" to choose or add a customer
4. **Enter Part Number**: Type a Babbitt part number in the input field
5. **Parse Part**: Click "Parse Part Number" to analyze the part
6. **Add to Quote**: Click "Add to Quote" to include in the current quote
7. **Export Quote**: Click "Export to Word" to generate the final document

## Part Number Format

Babbitt part numbers follow a specific format that the application can parse:

```
[Series][Size][Material][Options][Insulator][Length]
```

Example: `LS2000-2-NPT-TEFLON-12`

## Configuration

### Database Setup

The application uses SQLite databases for data storage:

- `quotes.db`: Stores quote information
- `customers.db`: Stores customer information

### Templates

Word templates are located in `export/templates/` and can be customized for different product lines.

## Development

### Building from Source

```bash
# Install development dependencies
pip install -r requirements.txt
pip install -e .[dev,build]

# Build executable
python build_installer.py
```

### Project Structure

```
QuoteTemplate/
├── main.py                 # Application entry point
├── gui/                    # User interface components
├── core/                   # Core business logic
├── database/               # Database management
├── export/                 # Document export functionality
├── config/                 # Configuration files
├── data/                   # Data files (pricing, validation rules)
└── utils/                  # Utility functions
```

## Troubleshooting

### Common Issues

1. **"Database not found" error**
   - Ensure you're running from the project root directory
   - Check that database files exist in the `database/` folder

2. **Word export fails**
   - Verify Microsoft Word is installed
   - Check template files exist in `export/templates/`

3. **Part number parsing errors**
   - Verify the part number format is correct
   - Check that validation rules are up to date

### Logs

Application logs are stored in the `logs/` directory and can help diagnose issues.

## Support

For technical support or feature requests, please contact:

- **Email**: support@babbitt.com
- **Phone**: [Your support phone number]
- **Hours**: Monday-Friday, 8AM-5PM EST

## License

This software is proprietary to Babbitt International. All rights reserved.

## Version History

### v1.0.0 (Current)
- Initial release
- Professional quote generation
- Customer and employee management
- Word document export
- Part number parsing
- Database management

## Contributing

This is proprietary software. For internal development, please follow the established coding standards and review process. 