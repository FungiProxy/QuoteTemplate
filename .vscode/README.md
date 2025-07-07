# Cursor/VS Code Environment Setup

This directory contains configuration files that automatically activate the QuoteTemplate Python virtual environment in every new terminal you open in Cursor.

## What's Configured

- **Automatic Environment Activation**: Every new terminal will automatically activate the `quote_env` virtual environment
- **Python Interpreter**: Points to the virtual environment Python executable
- **Terminal Profiles**: Two options available:
  - Command Prompt (Default) - Most reliable on Windows
  - PowerShell - Alternative option with colored output

## Files

- `settings.json` - Main Cursor/VS Code workspace settings
- `activate_env.bat` - Batch script for Command Prompt activation
- `activate_env.ps1` - PowerShell script for PowerShell activation

## How It Works

When you open a new terminal in Cursor:
1. The terminal automatically runs the activation script
2. Checks if `quote_env` exists
3. Activates the virtual environment if found
4. Shows helpful commands and status

## If Environment Not Found

If you see "Virtual environment not found", run:
```bash
setup_and_run.bat
```

This will create the virtual environment and install all dependencies.

## Switching Terminal Types

You can switch between terminal types using:
- Cursor: Terminal → New Terminal → Select Profile
- Or use the dropdown in the terminal panel

## Manual Activation

If needed, you can still manually activate using:
```bash
quote_env\Scripts\activate.bat
``` 