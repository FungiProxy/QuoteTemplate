# Babbitt Quote Generator - Deployment Guide

This guide provides comprehensive instructions for building and deploying the Babbitt Quote Generator as a professional installable application.

## Prerequisites

### Development Environment
- **Python 3.8+**: Required for building the application
- **Windows 10/11**: Primary target platform
- **Git**: For version control (optional)
- **Microsoft Word**: For template functionality (optional)

### Required Python Packages
```bash
pip install pyinstaller>=5.0.0
pip install python-docx==0.8.11
pip install colorama==0.4.6
pip install pydantic==2.5.0
```

## Building the Application

### Quick Build (Recommended)

1. **Run the build script**:
   ```bash
   # Windows
   build.bat
   
   # Or manually
   python build_installer.py
   ```

2. **Check the output**:
   - `dist/BabbittQuoteGenerator.exe` - Standalone executable
   - `dist/BabbittQuoteGenerator_Setup.exe` - Professional installer
   - `dist/BabbittQuoteGenerator_Portable.zip` - Portable version

### Manual Build Process

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Build with PyInstaller**:
   ```bash
   pyinstaller --onefile --windowed --name BabbittQuoteGenerator main.py
   ```

3. **Create installer package**:
   ```bash
   python build_installer.py
   ```

## Distribution Packages

### 1. Standalone Executable
- **File**: `BabbittQuoteGenerator.exe`
- **Size**: ~50-100MB
- **Usage**: Run directly, no installation required
- **Best for**: Quick testing, portable use

### 2. Professional Installer
- **File**: `BabbittQuoteGenerator_Setup.exe`
- **Size**: ~50-100MB
- **Usage**: Full installation with registry entries
- **Features**:
  - Desktop shortcut
  - Start menu entry
  - Uninstall support
  - Registry integration

### 3. Portable Package
- **File**: `BabbittQuoteGenerator_Portable.zip`
- **Size**: ~50-100MB
- **Usage**: Extract and run
- **Features**:
  - No installation required
  - Self-contained
  - No registry changes

## Installation Methods

### Method 1: Professional Installer (Recommended)

1. **Download**: `BabbittQuoteGenerator_Setup.exe`
2. **Run as Administrator**: Right-click → "Run as administrator"
3. **Follow Wizard**: Accept defaults or customize installation path
4. **Launch**: Use desktop shortcut or start menu

### Method 2: Portable Installation

1. **Download**: `BabbittQuoteGenerator_Portable.zip`
2. **Extract**: To any folder (e.g., `C:\BabbittQuoteGenerator\`)
3. **Run**: Execute `run.bat` or `BabbittQuoteGenerator.exe`

### Method 3: Manual Installation

1. **Download**: `BabbittQuoteGenerator.exe`
2. **Create folder**: `C:\Program Files\Babbitt Quote Generator\`
3. **Copy executable**: To the created folder
4. **Create shortcuts**: Manually create desktop and start menu shortcuts

## System Requirements

### Minimum Requirements
- **OS**: Windows 10 (64-bit)
- **RAM**: 4GB
- **Storage**: 100MB free space
- **Display**: 1024x768 resolution

### Recommended Requirements
- **OS**: Windows 11 (64-bit)
- **RAM**: 8GB
- **Storage**: 500MB free space
- **Display**: 1920x1080 resolution
- **Additional**: Microsoft Word for template export

## Configuration

### Database Setup
The application creates SQLite databases automatically:
- `quotes.db`: Quote data
- `customers.db`: Customer information

### Template Configuration
Word templates are included in the distribution:
- Location: `export/templates/`
- Format: `.docx` files
- Customization: Edit templates as needed

## Troubleshooting

### Common Build Issues

1. **PyInstaller not found**:
   ```bash
   pip install pyinstaller
   ```

2. **Missing dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Large executable size**:
   - Use `--onefile` for single file
   - Use `--onedir` for smaller size but multiple files

### Common Installation Issues

1. **"Access Denied" error**:
   - Run installer as administrator
   - Check antivirus software

2. **Missing DLL errors**:
   - Install Visual C++ Redistributable
   - Ensure Windows is up to date

3. **Database errors**:
   - Check write permissions
   - Ensure sufficient disk space

## Testing

### Pre-Distribution Testing

1. **Fresh Windows VM**: Test on clean Windows installation
2. **Different Windows versions**: Test on Windows 10 and 11
3. **User permissions**: Test with standard user accounts
4. **Antivirus software**: Test with common antivirus programs

### Test Checklist

- [ ] Application launches successfully
- [ ] Database creation works
- [ ] Part number parsing functions
- [ ] Quote generation works
- [ ] Word export functions
- [ ] Customer management works
- [ ] Uninstall process works

## Distribution

### Internal Distribution
- **Network share**: Place files on company network
- **Email**: Send installer to users
- **USB drive**: Portable distribution

### External Distribution
- **Website**: Host installer on company website
- **Cloud storage**: Use OneDrive, Google Drive, etc.
- **Software distribution platforms**: Use professional distribution services

## Updates and Maintenance

### Version Management
- Use semantic versioning (e.g., 1.0.0, 1.1.0)
- Update version in `setup.py` and `main.py`
- Create release notes for each version

### Update Distribution
1. **Build new version**: Use build scripts
2. **Test thoroughly**: Follow testing checklist
3. **Distribute**: Use same methods as initial distribution
4. **Notify users**: Inform users of updates

## Security Considerations

### Code Signing
- Sign executables with trusted certificate
- Prevents Windows SmartScreen warnings
- Increases user trust

### Antivirus Whitelisting
- Submit to antivirus vendors for whitelisting
- Reduces false positive detections
- Improves user experience

## Performance Optimization

### Executable Size
- Use `--exclude-module` to remove unused modules
- Optimize imports in code
- Use UPX compression (included in PyInstaller)

### Runtime Performance
- Optimize database queries
- Minimize file I/O operations
- Use efficient data structures

## Support and Documentation

### User Documentation
- Include README.txt with installation instructions
- Provide user guide (HTML or PDF)
- Create video tutorials if needed

### Technical Support
- Document common issues and solutions
- Provide contact information for support
- Create troubleshooting guide

## Legal and Compliance

### Licensing
- Ensure proper licensing for all dependencies
- Include license files in distribution
- Review third-party component licenses

### Data Protection
- Ensure compliance with data protection regulations
- Document data handling practices
- Implement appropriate security measures

## Conclusion

This deployment guide provides a comprehensive approach to creating and distributing the Babbitt Quote Generator as a professional application. Follow these guidelines to ensure a smooth deployment process and positive user experience.

For additional support or questions, contact the development team. 