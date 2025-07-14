"""
Custom Exception Classes for Babbitt Quote Generator
Provides specific exceptions for different error conditions
"""

from typing import Optional

class QuoteGeneratorError(Exception):
    """Base exception for all quote generator errors"""
    
    def __init__(self, message: str, details: str = None):
        super().__init__(message)
        self.message = message
        self.details = details
    
    def __str__(self):
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message

class ParseError(QuoteGeneratorError):
    """Exception raised when part number parsing fails"""
    
    def __init__(self, part_number: str, message: str = "Failed to parse part number", details: str = None):
        self.part_number = part_number
        full_message = f"{message}: '{part_number}'"
        super().__init__(full_message, details)

class ValidationError(QuoteGeneratorError):
    """Exception raised when validation fails"""
    
    def __init__(self, field: str, value: str, message: str = "Validation failed", details: str = None):
        self.field = field
        self.value = value
        full_message = f"{message} for {field}: '{value}'"
        super().__init__(full_message, details)

class DatabaseError(QuoteGeneratorError):
    """Exception raised when database operations fail"""
    
    def __init__(self, operation: str, table: str = None, message: str = "Database operation failed", details: str = None):
        self.operation = operation
        self.table = table
        if table:
            full_message = f"{message}: {operation} on {table}"
        else:
            full_message = f"{message}: {operation}"
        super().__init__(full_message, details)

class ExportError(QuoteGeneratorError):
    """Exception raised when export operations fail"""
    
    def __init__(self, file_path: str, message: str = "Export failed", details: str = None):
        self.file_path = file_path
        full_message = f"{message}: {file_path}"
        super().__init__(full_message, details)

class ConfigurationError(QuoteGeneratorError):
    """Exception raised when configuration is invalid"""
    
    def __init__(self, setting: str, message: str = "Configuration error", details: str = None):
        self.setting = setting
        full_message = f"{message}: {setting}"
        super().__init__(full_message, details)

class CompatibilityError(QuoteGeneratorError):
    """Exception raised when components are incompatible"""
    
    def __init__(self, component1: str, component2: str, message: str = "Components are incompatible", details: str = None):
        self.component1 = component1
        self.component2 = component2
        full_message = f"{message}: {component1} and {component2}"
        super().__init__(full_message, details)

class PricingError(QuoteGeneratorError):
    """Exception raised when pricing calculations fail"""
    
    def __init__(self, part_number: str, message: str = "Pricing calculation failed", details: str = None):
        self.part_number = part_number
        full_message = f"{message} for {part_number}"
        super().__init__(full_message, details)

class TemplateError(QuoteGeneratorError):
    """Exception raised when template processing fails"""
    
    def __init__(self, template_path: str, message: str = "Template processing failed", details: str = None):
        self.template_path = template_path
        full_message = f"{message}: {template_path}"
        super().__init__(full_message, details)

class DataIntegrityError(QuoteGeneratorError):
    """Exception raised when data integrity checks fail"""
    
    def __init__(self, data_type: str, message: str = "Data integrity check failed", details: str = None):
        self.data_type = data_type
        full_message = f"{message}: {data_type}"
        super().__init__(full_message, details)

class AuthenticationError(QuoteGeneratorError):
    """Exception raised when authentication fails"""
    
    def __init__(self, message: str = "Authentication failed", details: str = None):
        super().__init__(message, details)

class AuthorizationError(QuoteGeneratorError):
    """Exception raised when authorization fails"""
    
    def __init__(self, operation: str, message: str = "Authorization failed", details: str = None):
        self.operation = operation
        full_message = f"{message}: {operation}"
        super().__init__(full_message, details)

class NetworkError(QuoteGeneratorError):
    """Exception raised when network operations fail"""
    
    def __init__(self, endpoint: str, message: str = "Network operation failed", details: str = None):
        self.endpoint = endpoint
        full_message = f"{message}: {endpoint}"
        super().__init__(full_message, details)

class FileOperationError(QuoteGeneratorError):
    """Exception raised when file operations fail"""
    
    def __init__(self, file_path: str, operation: str, message: str = "File operation failed", details: str = None):
        self.file_path = file_path
        self.operation = operation
        full_message = f"{message}: {operation} on {file_path}"
        super().__init__(full_message, details)

class BusinessLogicError(QuoteGeneratorError):
    """Exception raised when business logic validation fails"""
    
    def __init__(self, rule: str, message: str = "Business logic validation failed", details: str = None):
        self.rule = rule
        full_message = f"{message}: {rule}"
        super().__init__(full_message, details)

# Exception handler utilities
def handle_exception(exc: Exception, logger=None, reraise: bool = True):
    """
    Handle exceptions with optional logging and reraising
    
    Args:
        exc: Exception to handle
        logger: Logger instance for logging
        reraise: Whether to reraise the exception
    """
    if logger:
        if isinstance(exc, QuoteGeneratorError):
            logger.error(f"Application error: {exc}")
            if exc.details:
                logger.error(f"Details: {exc.details}")
        else:
            logger.error(f"Unexpected error: {exc}")
    
    if reraise:
        raise exc

def safe_execute(func, *args, default_return=None, logger=None, **kwargs):
    """
    Safely execute a function with exception handling
    
    Args:
        func: Function to execute
        *args: Function arguments
        default_return: Value to return if function fails
        logger: Logger instance for logging
        **kwargs: Function keyword arguments
    
    Returns:
        Function result or default_return if function fails
    """
    try:
        return func(*args, **kwargs)
    except Exception as exc:
        if logger:
            logger.error(f"Safe execution failed for {func.__name__}: {exc}")
        return default_return

def validate_and_raise(condition: bool, exception_class: type, *args, **kwargs):
    """
    Validate condition and raise exception if false
    
    Args:
        condition: Condition to validate
        exception_class: Exception class to raise
        *args: Exception arguments
        **kwargs: Exception keyword arguments
    """
    if not condition:
        raise exception_class(*args, **kwargs)

# Context manager for exception handling
class ExceptionContext:
    """
    Context manager for handling exceptions with automatic logging
    """
    
    def __init__(self, logger=None, reraise: bool = True, default_return=None):
        self.logger = logger
        self.reraise = reraise
        self.default_return = default_return
        self.exception = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.exception = exc_val
            handle_exception(exc_val, self.logger, reraise=False)
            return not self.reraise
        return False
    
    def get_result(self, success_value=None):
        """Get result based on whether exception occurred"""
        if self.exception:
            return self.default_return
        return success_value 