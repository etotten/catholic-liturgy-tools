"""Index page generation module."""

from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass
import re
from catholic_liturgy_tools.utils.file_ops import write_file_safe


@dataclass
class ReadingsEntry:
    """Represents a readings entry in the index page."""
    date: str
    liturgical_day: str
    link: str
    
    @property
    def title(self) -> str:
        """Display title combining date and liturgical day."""
        return f"{self.date} - {self.liturgical_day}"


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


def scan_readings_files(readings_dir: str = "readings") -> List[ReadingsEntry]:
    """
    Scan directory for daily readings HTML files and create ReadingsEntry objects.
    
    This function scans the readings directory for HTML files, extracts the liturgical
    day name from each file's <h1> tag, and creates ReadingsEntry objects sorted by
    date in reverse chronological order (newest first).
    
    Args:
        readings_dir: Directory to scan (default: readings)
        
    Returns:
        List[ReadingsEntry]: List of readings entries, sorted newest first
        
    Example:
        >>> entries = scan_readings_files("readings")
        >>> len(entries) > 0
        True
        >>> entries[0].date > entries[-1].date  # Newest first
        True
    """
    dir_path = Path(readings_dir)
    
    if not dir_path.exists():
        return []
    
    entries = []
    
    # Find all HTML files matching the pattern YYYY-MM-DD.html
    html_files = list(dir_path.glob("*.html"))
    
    for html_file in html_files:
        # Extract date from filename (YYYY-MM-DD.html)
        filename = html_file.stem  # Gets filename without .html extension
        
        # Validate date format
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(date_pattern, filename):
            continue  # Skip files that don't match date pattern
        
        # Parse HTML to extract liturgical day name
        try:
            content = html_file.read_text(encoding="utf-8")
            
            # Extract text from first <h1> tag
            h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.DOTALL)
            if not h1_match:
                continue  # Skip files without h1 tag
            
            liturgical_day = h1_match.group(1).strip()
            if not liturgical_day:
                continue  # Skip files with empty h1
            
            # Create ReadingsEntry with relative link
            # Use just the directory name (not full path) for Jekyll-compatible links
            dir_name = Path(readings_dir).name
            entry = ReadingsEntry(
                date=filename,
                liturgical_day=liturgical_day,
                link=f"{dir_name}/{html_file.name}"
            )
            entries.append(entry)
            
        except Exception:
            # Skip files that can't be read or parsed
            continue
    
    # Sort by date in reverse chronological order (newest first)
    entries.sort(key=lambda e: e.date, reverse=True)
    
    return entries


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


def generate_index_content(message_files: List[Path], readings: Optional[List[ReadingsEntry]] = None) -> str:
    """
    Generate markdown content for the index page with both messages and readings sections.
    
    Args:
        message_files: List of message file paths
        readings: Optional list of ReadingsEntry objects (default: None)
        
    Returns:
        str: Markdown content with YAML frontmatter
        
    Example:
        >>> files = [Path("_posts/2025-11-22-daily-message.md")]
        >>> content = generate_index_content(files)
        >>> "layout: page" in content
        True
        >>> "Daily Messages" in content
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
    
    # Generate markdown content with updated title
    content = """---
layout: page
title: "Catholic Liturgy Tools"
---

# Catholic Liturgy Tools

Welcome to Catholic Liturgy Tools, a resource for daily liturgical content.

## Daily Messages

"""
    
    # Add messages section
    if date_file_pairs:
        for date, file in date_file_pairs:
            # Create relative path for Jekyll
            relative_path = f"_posts/{file.name}"
            content += f"- [Daily Message for {date}]({relative_path})\n"
    else:
        content += "*No messages yet.*\n"
    
    # Add readings section if provided
    if readings is not None:
        content += "\n## Daily Readings\n\n"
        
        if readings:
            for entry in readings:
                content += f"- [{entry.title}]({entry.link})\n"
        else:
            content += "*No readings yet.*\n"
    
    return content


def generate_index(posts_dir: str = "_posts", output_file: str = "index.md", readings_dir: Optional[str] = None) -> Path:
    """
    Generate an index page with links to all daily messages and readings.
    
    This is the main entry point for index generation. It scans the posts directory
    for messages and optionally the readings directory for daily readings, creating
    an index page with links to all content, sorted in reverse chronological order
    (newest first).
    
    Args:
        posts_dir: Directory containing message files (default: _posts)
        output_file: Output file path (default: index.md)
        readings_dir: Optional directory containing readings HTML files (default: None)
                     If provided, the index will include a Daily Readings section
        
    Returns:
        Path: Path to the generated index file
        
    Raises:
        OSError: If file writing fails due to permissions or other errors
        
    Example:
        >>> path = generate_index()
        >>> path.exists()
        True
        >>> path = generate_index(readings_dir="readings")
        >>> "Daily Readings" in path.read_text()
        True
    """
    # Scan for message files
    message_files = scan_message_files(posts_dir)
    
    # Scan for readings files if directory provided
    readings = None
    if readings_dir is not None:
        readings = scan_readings_files(readings_dir)
    
    # Generate content
    content = generate_index_content(message_files, readings)
    
    # Write to file
    output_path = Path(output_file)
    write_file_safe(output_path, content)
    
    return output_path
