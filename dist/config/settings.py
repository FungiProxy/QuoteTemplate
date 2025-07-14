"""
Application Settings and Constants
Centralized configuration for the Babbitt Quote Generator
"""

import os
from pathlib import Path

# Application Info
APP_NAME = "Babbitt Quote Generator"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Professional quote generation for Babbitt level switches"

# Paths
BASE_DIR = Path(__file__).parent.parent
DATABASE_DIR = BASE_DIR / "database"
EXPORT_DIR = BASE_DIR / "export"
TEMPLATES_DIR = EXPORT_DIR / "templates"
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# Database Settings
DATABASE_NAME = "quotes.db"
DATABASE_PATH = DATABASE_DIR / DATABASE_NAME

# Export Settings
DEFAULT_EXPORT_FORMAT = "docx"

QUOTE_TEMPLATE_NAME = "quote_template.docx"
QUOTE_TEMPLATE_PATH = TEMPLATES_DIR / QUOTE_TEMPLATE_NAME

# GUI Settings
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600

# Default Values
DEFAULT_CUSTOMER = "New Customer"
DEFAULT_QUANTITY = 1
DEFAULT_DELIVERY_WEEKS = 4

# Validation Settings
MAX_PART_NUMBER_LENGTH = 100
MAX_CUSTOMER_NAME_LENGTH = 100
MIN_PROBE_LENGTH = 1.0
MAX_PROBE_LENGTH = 120.0

# Material Limits
HALAR_MAX_LENGTH = 72.0  # inches
NONSTANDARD_LENGTH_THRESHOLD = 36.0  # inches

# Pricing Settings
CURRENCY_SYMBOL = "$"
PRICE_DECIMAL_PLACES = 2
TAX_RATE = 0.0  # Configurable tax rate

# Quote Settings
QUOTE_NUMBER_PREFIX = "BBT"
QUOTE_VALIDITY_DAYS = 30

# Logging Settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Company Information
COMPANY_NAME = "Babbitt International"
COMPANY_ADDRESS = "123 Industrial Way, Manufacturing City, ST 12345"
COMPANY_PHONE = "(555) 123-4567"
COMPANY_EMAIL = "quotes@babbitt.com"
COMPANY_WEBSITE = "www.babbittinternational.com"

# Sample Part Numbers for Testing
SAMPLE_PART_NUMBERS = [
    "LS2000-115VAC-S-10\"",
    "LS2000-115VAC-S-10\"-XSP-VR-8\"TEFINS",
    "LS2100-24VDC-H-12\"",
    "LS6000-115VAC-S-14\"-1\"NPT",
    "LS7000-115VAC-H-18\"-8\"TEFINS",
    "LS8000-115VAC-S-24\"-CP-SSTAG",
    "LS2000-115VAC-S-10\"-VRHOUSING-90DEG",
    "LS2000-115VAC-S-10\"-3/4\"OD"
]

# File Extensions
ALLOWED_EXPORT_FORMATS = ['.docx', '.pdf', '.txt']
ALLOWED_TEMPLATE_FORMATS = ['.docx']

# Error Messages
ERROR_MESSAGES = {
    'database_connection': "Could not connect to database. Please check database file.",
    'invalid_part_number': "Invalid part number format. Please check your input.",
    'missing_template': "Quote template file not found. Please check template directory.",
    'export_failed': "Failed to export quote. Please check file permissions.",
    'parsing_error': "Error parsing part number. Please verify the format.",
    'pricing_error': "Error calculating pricing. Please check database configuration."
}

# Success Messages
SUCCESS_MESSAGES = {
    'quote_generated': "Quote generated successfully!",
    'quote_exported': "Quote exported successfully!",
    'database_connected': "Database connected successfully.",
    'part_parsed': "Part number parsed successfully."
}

# Application State
class AppState:
    def __init__(self):
        self.current_quote = None
        self.current_customer = DEFAULT_CUSTOMER
        self.last_export_path = None
        self.database_connected = False
