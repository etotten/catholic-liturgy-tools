"""HTML index page generation module for _site/ structure."""

from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass
import re
import html
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


def scan_message_files(messages_dir: str = "_site/messages") -> List[Path]:
    """
    Scan directory for daily message files.
    
    Args:
        messages_dir: Directory to scan (default: _site/messages)
        
    Returns:
        List[Path]: List of message file paths, sorted reverse chronologically
    """
    dir_path = Path(messages_dir)
    
    if not dir_path.exists():
        return []
    
    # Find all files matching the pattern *-daily-message.md
    message_files = list(dir_path.glob("*-daily-message.md"))
    
    # Sort in reverse chronological order (newest first)
    message_files.sort(reverse=True)
    
    return message_files


def scan_readings_files(readings_dir: str = "_site/readings") -> List[ReadingsEntry]:
    """
    Scan directory for daily readings HTML files and create ReadingsEntry objects.
    
    Args:
        readings_dir: Directory to scan (default: _site/readings)
        
    Returns:
        List[ReadingsEntry]: List of readings entries, sorted newest first
    """
    dir_path = Path(readings_dir)
    
    if not dir_path.exists():
        return []
    
    entries = []
    
    # Find all HTML files matching the pattern YYYY-MM-DD.html
    html_files = list(dir_path.glob("*.html"))
    
    for html_file in html_files:
        # Extract date from filename (YYYY-MM-DD.html)
        filename = html_file.stem
        
        # Validate date format
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(date_pattern, filename):
            continue
        
        # Parse HTML to extract liturgical day name
        try:
            content = html_file.read_text(encoding="utf-8")
            
            # Extract text from first <h1> tag
            h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.DOTALL)
            if not h1_match:
                continue
            
            liturgical_day = h1_match.group(1).strip()
            if not liturgical_day:
                continue
            
            # Create entry with relative link
            entry = ReadingsEntry(
                date=filename,
                liturgical_day=liturgical_day,
                link=f"readings/{html_file.name}"
            )
            entries.append(entry)
            
        except (OSError, UnicodeDecodeError):
            continue
    
    # Sort in reverse chronological order (newest first)
    entries.sort(key=lambda e: e.date, reverse=True)
    
    return entries


def parse_date_from_filename(filename: str) -> Optional[str]:
    """
    Parse date from a message filename.
    
    Args:
        filename: Filename to parse (e.g., "2025-11-22-daily-message.md")
        
    Returns:
        str or None: Date string in YYYY-MM-DD format, or None if invalid
    """
    # Extract just the filename if a path is provided
    name = Path(filename).name
    
    # Match pattern: YYYY-MM-DD-daily-message.md
    pattern = r"^(\d{4}-\d{2}-\d{2})-daily-message\.md$"
    match = re.match(pattern, name)
    
    if match:
        return match.group(1)
    
    return None


def generate_html_index(message_files: List[Path], readings_entries: List[ReadingsEntry]) -> str:
    """
    Generate HTML content for the index page.
    
    Args:
        message_files: List of message file paths
        readings_entries: List of readings entries
        
    Returns:
        str: Complete HTML document
    """
    # Build messages list HTML
    messages_html = ""
    for msg_file in sorted(message_files, reverse=True):
        date = parse_date_from_filename(msg_file.name)
        if date:
            # Escape date for HTML safety
            safe_date = html.escape(date)
            safe_filename = html.escape(msg_file.name)
            messages_html += f'        <li><a href="messages/{safe_filename}">{safe_date}</a></li>\n'
    
    # Handle empty messages list
    if not messages_html:
        messages_html = '        <li>No messages available yet.</li>\n'
    
    # Build readings list HTML
    readings_html = ""
    for entry in readings_entries:
        safe_date = html.escape(entry.date)
        safe_day = html.escape(entry.liturgical_day)
        safe_link = html.escape(entry.link)
        readings_html += f'        <li><a href="{safe_link}">{safe_date} - {safe_day}</a></li>\n'
    
    # Handle empty readings list
    if not readings_html:
        readings_html = '        <li>No readings available yet.</li>\n'
    
    # Generate complete HTML document
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catholic Liturgy Tools</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #666;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        h2 {{
            color: #666;
            margin-top: 2em;
            margin-bottom: 1em;
        }}
        ul {{
            list-style: none;
            padding: 0;
        }}
        li {{
            margin: 0.5em 0;
            padding: 5px 0;
        }}
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
            color: #0052a3;
        }}
    </style>
</head>
<body>
    <h1>Catholic Liturgy Tools</h1>
    
    <h2>Daily Messages</h2>
    <ul>
{messages_html.rstrip()}
    </ul>
    
    <h2>Daily Readings</h2>
    <ul>
{readings_html.rstrip()}
    </ul>
</body>
</html>
"""
    
    return html_content


def generate_index(
    posts_dir: str = "_site/messages",
    output_file: str = "_site/index.html",
    readings_dir: Optional[str] = "_site/readings"
) -> Path:
    """
    Generate HTML index page with links to all messages and readings.
    
    Args:
        posts_dir: Directory containing message files (default: _site/messages)
        output_file: Output file path (default: _site/index.html)
        readings_dir: Directory containing readings files (default: _site/readings)
        
    Returns:
        Path: Path to the generated index file
    """
    # Scan for message files
    message_files = scan_message_files(posts_dir)
    
    # Scan for readings entries
    readings_entries = []
    if readings_dir:
        readings_entries = scan_readings_files(readings_dir)
    
    # Generate HTML content
    html_content = generate_html_index(message_files, readings_entries)
    
    # Write to file
    output_path = Path(output_file)
    write_file_safe(output_path, html_content)
    
    return output_path


__all__ = [
    'ReadingsEntry',
    'scan_message_files',
    'scan_readings_files', 
    'parse_date_from_filename',
    'generate_html_index',
    'generate_index',
]
