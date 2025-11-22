"""Date utility functions for message generation."""

from datetime import date


def get_today() -> str:
    """
    Get today's date in YYYY-MM-DD format.
    
    Returns:
        str: Today's date in ISO 8601 format (YYYY-MM-DD)
        
    Example:
        >>> get_today()
        '2025-11-22'
    """
    return date.today().isoformat()
