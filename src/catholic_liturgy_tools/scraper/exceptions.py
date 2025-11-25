"""
Exception hierarchy for the Catholic Liturgy Tools scraper module.

This module defines custom exceptions for handling various error conditions
during the scraping and processing of liturgical readings.
"""


class LiturgyToolsError(Exception):
    """
    Base exception for all Catholic Liturgy Tools errors.
    
    All custom exceptions in this project inherit from this class,
    allowing for catching all tool-specific errors with a single except clause.
    """
    pass


class ScraperError(LiturgyToolsError):
    """
    Base exception for all scraper-related errors.
    
    Use this as a base class for specific scraping errors, or raise it
    directly for generic scraping issues.
    """
    pass


class NetworkError(ScraperError):
    """
    Raised when network operations fail.
    
    Examples:
    - Connection timeouts
    - DNS resolution failures
    - HTTP errors (4xx, 5xx status codes)
    - SSL/TLS errors
    
    Attributes:
        url (str): The URL that failed to load (if available)
        status_code (int): HTTP status code (if available)
    """
    
    def __init__(self, message: str, url: str = None, status_code: int = None):
        super().__init__(message)
        self.url = url
        self.status_code = status_code


class ParseError(ScraperError):
    """
    Raised when HTML parsing or data extraction fails.
    
    Examples:
    - Expected HTML elements not found
    - Malformed HTML structure
    - Unexpected HTML format or changes to source site
    - Unable to extract required data fields
    
    Attributes:
        element (str): The HTML element or selector that failed (if available)
    """
    
    def __init__(self, message: str, element: str = None):
        super().__init__(message)
        self.element = element


class ValidationError(ScraperError):
    """
    Raised when data validation fails.
    
    Examples:
    - Empty required fields
    - Invalid data formats
    - Data fails business logic validation
    - Inconsistent or corrupted data
    
    Attributes:
        field (str): The field that failed validation (if available)
        value: The invalid value (if available)
    """
    
    def __init__(self, message: str, field: str = None, value=None):
        super().__init__(message)
        self.field = field
        self.value = value


class DateError(LiturgyToolsError):
    """
    Raised when date operations or validations fail.
    
    Examples:
    - Invalid date format
    - Date out of acceptable range
    - Date parsing failures
    
    Attributes:
        date_str (str): The date string that caused the error (if available)
    """
    
    def __init__(self, message: str, date_str: str = None):
        super().__init__(message)
        self.date_str = date_str
