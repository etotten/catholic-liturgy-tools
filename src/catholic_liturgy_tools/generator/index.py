"""Index page generation module."""

from pathlib import Path
from typing import List, Optional
import re
from catholic_liturgy_tools.utils.file_ops import write_file_safe


def scan_message_files(posts_dir: str = "_posts") -> List[Path]:
    """
    Scan directory for daily message files.
    
    Args:
        posts_dir: Directory to scan (default: _posts)
        
    Returns:
        List[Path]: List of message file paths
        
    Example:
        >>> files = scan_message_files("_posts")
        >>> len(files) > 0
        True
    """
    dir_path = Path(posts_dir)
    
    if not dir_path.exists():
        return []
    
    # Find all files matching the pattern *-daily-message.md
    message_files = list(dir_path.glob("*-daily-message.md"))
    
    return message_files


def parse_date_from_filename(filename: str) -> Optional[str]:
    """
    Parse date from message filename.
    
    Args:
        filename: Filename or path to parse
        
    Returns:
        Optional[str]: Date in YYYY-MM-DD format, or None if invalid
        
    Example:
        >>> parse_date_from_filename("2025-11-22-daily-message.md")
        '2025-11-22'
    """
    # Extract just the filename if a path was provided
    filename_only = Path(filename).name
    
    # Pattern: YYYY-MM-DD-daily-message.md
    pattern = r"^(\d{4}-\d{2}-\d{2})-daily-message\.md$"
    match = re.match(pattern, filename_only)
    
    if match:
        return match.group(1)
    
    return None


def generate_index_content(message_files: List[Path]) -> str:
    """
    Generate markdown content for the index page.
    
    Args:
        message_files: List of message file paths
        
    Returns:
        str: Markdown content with YAML frontmatter
        
    Example:
        >>> files = [Path("_posts/2025-11-22-daily-message.md")]
        >>> content = generate_index_content(files)
        >>> "layout: page" in content
        True
    """
    # Parse dates from filenames and sort in reverse chronological order
    date_file_pairs = []
    for file in message_files:
        date = parse_date_from_filename(file.name)
        if date:
            date_file_pairs.append((date, file))
    
    # Sort by date (newest first)
    date_file_pairs.sort(key=lambda x: x[0], reverse=True)
    
    # Generate markdown content
    content = """---
layout: page
title: "Catholic Liturgy Tools - Daily Messages"
---

# Catholic Liturgy Tools - Daily Messages

## Recent Messages

"""
    
    if date_file_pairs:
        for date, file in date_file_pairs:
            # Create relative path for Jekyll
            relative_path = f"_posts/{file.name}"
            content += f"- [Daily Message for {date}]({relative_path})\n"
    else:
        content += "*No messages yet.*\n"
    
    return content


def generate_index(posts_dir: str = "_posts", output_file: str = "index.md") -> Path:
    """
    Generate an index page with links to all daily messages.
    
    This is the main entry point for index generation. It scans the posts directory,
    creates an index page with links to all messages, sorted in reverse chronological
    order (newest first).
    
    Args:
        posts_dir: Directory containing message files (default: _posts)
        output_file: Output file path (default: index.md)
        
    Returns:
        Path: Path to the generated index file
        
    Raises:
        OSError: If file writing fails due to permissions or other errors
        
    Example:
        >>> path = generate_index()
        >>> path.exists()
        True
    """
    # Scan for message files
    message_files = scan_message_files(posts_dir)
    
    # Generate content
    content = generate_index_content(message_files)
    
    # Write to file
    output_path = Path(output_file)
    write_file_safe(output_path, content)
    
    return output_path
