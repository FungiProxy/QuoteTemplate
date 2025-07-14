"""
Logging Configuration for Babbitt Quote Generator
Provides centralized logging setup and utilities
"""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional
from datetime import datetime

# Import settings with fallback
try:
    from config.settings import (
        LOG_LEVEL, LOG_FORMAT, LOG_DATE_FORMAT, 
        LOGS_DIR, BASE_DIR
    )
except ImportError:
    # Fallback values if settings not available
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    BASE_DIR = Path(__file__).parent.parent
    LOGS_DIR = BASE_DIR / "logs"

def setup_logging(
    level: str = LOG_LEVEL,
    log_file: Optional[str] = None,
    console_output: bool = True,
    file_output: bool = True
) -> None:
    """
    Setup application logging configuration
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Custom log file path
        console_output: Enable console logging
        file_output: Enable file logging
    """
    # Create logs directory if it doesn't exist
    LOGS_DIR.mkdir(exist_ok=True)
    
    # Clear any existing handlers
    logging.getLogger().handlers.clear()
    
    # Set logging level
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.getLogger().setLevel(numeric_level)
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(formatter)
        logging.getLogger().addHandler(console_handler)
    
    # File handler
    if file_output:
        if not log_file:
            # Default log file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d")
            log_file = str(LOGS_DIR / f"babbitt_quote_generator_{timestamp}.log")
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        logging.getLogger().addHandler(file_handler)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    
    # If no handlers are set up, do basic setup
    if not logger.handlers and not logging.getLogger().handlers:
        setup_logging()
    
    return logger

class QuoteGeneratorLogger:
    """
    Custom logger class for the quote generator application
    """
    
    def __init__(self, name: str):
        self.logger = get_logger(name)
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.logger.debug(message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self.logger.info(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        self.logger.error(message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self.logger.critical(message, **kwargs)
    
    def exception(self, message: str, **kwargs):
        """Log exception with traceback"""
        self.logger.exception(message, **kwargs)
    
    def log_part_number_parse(self, part_number: str, success: bool, details: str = ""):
        """Log part number parsing attempt"""
        if success:
            self.info(f"Successfully parsed part number: {part_number}")
        else:
            self.error(f"Failed to parse part number: {part_number} - {details}")
    
    def log_pricing_calculation(self, part_number: str, total_price: float, breakdown: Optional[dict] = None):
        """Log pricing calculation"""
        message = f"Pricing calculated for {part_number}: ${total_price:.2f}"
        if breakdown is not None:
            details = ", ".join([f"{k}: ${v:.2f}" for k, v in breakdown.items()])
            message += f" ({details})"
        self.info(message)
    
    def log_database_operation(self, operation: str, table: str, success: bool, details: str = ""):
        """Log database operation"""
        if success:
            self.info(f"Database {operation} successful on {table}")
        else:
            self.error(f"Database {operation} failed on {table}: {details}")
    
    def log_export_operation(self, file_path: str, success: bool, details: str = ""):
        """Log export operation"""
        if success:
            self.info(f"Successfully exported to: {file_path}")
        else:
            self.error(f"Failed to export to {file_path}: {details}")
    
    def log_validation_result(self, part_number: str, errors: list, warnings: list):
        """Log validation results"""
        if errors:
            self.warning(f"Validation errors for {part_number}: {', '.join(errors)}")
        if warnings:
            self.info(f"Validation warnings for {part_number}: {', '.join(warnings)}")
        if not errors and not warnings:
            self.info(f"Validation passed for {part_number}")

# Performance logging decorator
def log_performance(func):
    """
    Decorator to log function execution time
    """
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        start_time = datetime.now()
        
        try:
            result = func(*args, **kwargs)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.debug(f"{func.__name__} executed in {duration:.3f} seconds")
            return result
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.error(f"{func.__name__} failed after {duration:.3f} seconds: {str(e)}")
            raise
    
    return wrapper

# Context manager for logging operations
class LoggingContext:
    """
    Context manager for logging operations with automatic success/failure logging
    """
    
    def __init__(self, logger: logging.Logger, operation: str):
        self.logger = logger
        self.operation = operation
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.info(f"Starting {self.operation}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time is not None:
            duration = (datetime.now() - self.start_time).total_seconds()
            
            if exc_type is None:
                self.logger.info(f"Completed {self.operation} in {duration:.3f} seconds")
            else:
                self.logger.error(f"Failed {self.operation} after {duration:.3f} seconds: {exc_val}")
        
        return False  # Don't suppress exceptions

# Initialize default logging
if not logging.getLogger().handlers:
    setup_logging() 