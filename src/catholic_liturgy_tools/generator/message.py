"""Daily message generation module."""

from pathlib import Path
from catholic_liturgy_tools.utils.date_utils import get_today
from catholic_liturgy_tools.utils.file_ops import write_file_safe


def generate_message_content(date: str) -> str:
    """
    Generate markdown content for a daily message.
    
    Args:
        date: Date in YYYY-MM-DD format
        
    Returns:
        str: Markdown content with YAML frontmatter
        
    Example:
        >>> content = generate_message_content("2025-11-22")
        >>> "Hello Catholic World" in content
        True
    """
    content = f"""---
layout: post
title: "Daily Message for {date}"
date: {date}
---

# {date}

Hello Catholic World
"""
    return content


def get_message_file_path(date: str, output_dir: str = "_site/messages") -> Path:
    """
    Get the file path for a daily message.
    
    Args:
        date: Date in YYYY-MM-DD format
        output_dir: Output directory (default: _site/messages)
        
    Returns:
        Path: File path for the message
        
    Example:
        >>> path = get_message_file_path("2025-11-22")
        >>> path.name
        '2025-11-22-daily-message.md'
    """
    filename = f"{date}-daily-message.md"
    return Path(output_dir) / filename


def generate_message(output_dir: str = "_site/messages", date: str = None) -> Path:
    """
    Generate a daily message for the specified date or today's date.
    
    This is the main entry point for message generation. It creates a markdown file
    with the specified date (or today's date) and the greeting "Hello Catholic World"
    in the specified output directory.
    
    Args:
        output_dir: Output directory (default: _site/messages)
        date: Date string in YYYY-MM-DD format (default: today)
        
    Returns:
        Path: Path to the generated message file
        
    Raises:
        OSError: If file writing fails due to permissions or other errors
        
    Example:
        >>> path = generate_message()
        >>> path.exists()
        True
        >>> path = generate_message(date="2025-12-25")
        >>> "2025-12-25" in str(path)
        True
    """
    # Use provided date or default to today
    date_str = date if date else get_today()
    content = generate_message_content(date_str)
    filepath = get_message_file_path(date_str, output_dir=output_dir)
    
    # Write file (this will create the directory if needed)
    write_file_safe(filepath, content)
    
    return filepath
