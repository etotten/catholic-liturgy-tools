"""File operations utilities for safe file writing."""

from pathlib import Path
from typing import Union


def ensure_directory_exists(directory: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory: Path to the directory (string or Path object)
        
    Returns:
        Path: The directory path as a Path object
        
    Raises:
        OSError: If directory creation fails due to permissions or other errors
        
    Example:
        >>> ensure_directory_exists("_posts")
        PosixPath('_posts')
    """
    dir_path = Path(directory)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def write_file_safe(filepath: Union[str, Path], content: str, encoding: str = "utf-8") -> Path:
    """
    Safely write content to a file, creating parent directories if needed.
    
    Args:
        filepath: Path to the file to write (string or Path object)
        content: Content to write to the file
        encoding: File encoding (default: utf-8)
        
    Returns:
        Path: The file path as a Path object
        
    Raises:
        OSError: If file writing fails due to permissions or other errors
        
    Example:
        >>> write_file_safe("_posts/2025-11-22-daily-message.md", "# Hello")
        PosixPath('_posts/2025-11-22-daily-message.md')
    """
    file_path = Path(filepath)
    
    # Ensure parent directory exists
    if file_path.parent != Path("."):
        ensure_directory_exists(file_path.parent)
    
    # Write content to file
    file_path.write_text(content, encoding=encoding)
    
    return file_path
