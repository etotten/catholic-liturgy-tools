"""
Retry decorator with exponential backoff.

This module provides a decorator for retrying functions that may fail
transiently (e.g., network requests) with exponential backoff between attempts.
"""

import logging
import time
from functools import wraps
from typing import Callable, Type, Tuple

logger = logging.getLogger(__name__)


def retry_with_backoff(
    max_attempts: int = 3,
    backoff_factor: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    logger_name: str = None
):
    """
    Decorator that retries a function with exponential backoff on failure.
    
    Args:
        max_attempts: Maximum number of attempts (default: 3)
        backoff_factor: Multiplier for delay between retries (default: 2.0)
        exceptions: Tuple of exception types to catch and retry (default: all exceptions)
        logger_name: Optional logger name to use (default: module logger)
    
    Returns:
        Decorated function that will retry on failure
    
    Example:
        >>> @retry_with_backoff(max_attempts=3, backoff_factor=2.0)
        ... def fetch_data():
        ...     # May raise NetworkError
        ...     return requests.get("https://example.com")
        
        The function will retry up to 3 times with delays: 2s, 4s, 8s
    
    Raises:
        The last exception encountered if all retry attempts fail
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Use provided logger or module logger
            retry_logger = logging.getLogger(logger_name) if logger_name else logger
            
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    
                    # Log success if we had previous failures
                    if attempt > 1:
                        retry_logger.info(
                            f"{func.__name__} succeeded on attempt {attempt}/{max_attempts}"
                        )
                    
                    return result
                    
                except exceptions as e:
                    last_exception = e
                    
                    if attempt < max_attempts:
                        # Calculate delay with exponential backoff
                        delay = backoff_factor ** (attempt - 1)
                        
                        retry_logger.warning(
                            f"{func.__name__} failed on attempt {attempt}/{max_attempts}: {e}. "
                            f"Retrying in {delay:.1f}s..."
                        )
                        
                        time.sleep(delay)
                    else:
                        # Final attempt failed
                        retry_logger.error(
                            f"{func.__name__} failed after {max_attempts} attempts: {e}"
                        )
            
            # All attempts failed, raise the last exception
            raise last_exception
        
        return wrapper
    return decorator
