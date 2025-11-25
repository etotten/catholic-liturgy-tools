"""Utilities for HTML generation and sanitization."""

import html
from typing import List


def sanitize_text(text: str) -> str:
    """Sanitize text for safe inclusion in HTML by escaping special characters.
    
    This function escapes HTML special characters to prevent XSS attacks and
    ensure proper rendering of text content in HTML pages.
    
    Characters escaped:
    - < → &lt;
    - > → &gt;
    - & → &amp;
    - " → &quot;
    - ' → &#x27;
    
    Args:
        text: Raw text string to sanitize
        
    Returns:
        HTML-escaped string safe for inclusion in HTML content
        
    Examples:
        >>> sanitize_text("King's reading <Scripture>")
        "King&#x27;s reading &lt;Scripture&gt;"
        
        >>> sanitize_text("John 3:16 & Romans 8:28")
        "John 3:16 &amp; Romans 8:28"
    """
    return html.escape(text, quote=True)


def format_paragraph(text: str) -> str:
    """Format a paragraph of text for HTML display.
    
    This function:
    1. Strips leading and trailing whitespace
    2. Returns empty string if input is empty or whitespace-only
    3. Preserves internal whitespace (may be intentional formatting)
    4. Replaces line breaks with single spaces (for continuous text flow)
    
    Args:
        text: Raw paragraph text
        
    Returns:
        Formatted paragraph text (empty string if input was empty/whitespace)
        
    Examples:
        >>> format_paragraph("  King Antiochus was traversing the provinces.  ")
        "King Antiochus was traversing the provinces."
        
        >>> format_paragraph("  \\n  ")
        ""
        
        >>> format_paragraph("First line\\nSecond line")
        "First line Second line"
    """
    # Strip leading/trailing whitespace
    cleaned = text.strip()
    
    # Return empty string if nothing left
    if not cleaned:
        return ""
    
    # Replace line breaks with spaces for continuous text flow
    cleaned = cleaned.replace('\n', ' ').replace('\r', ' ')
    
    # Collapse multiple spaces while preserving intentional spacing
    # (We preserve double spaces as they might be intentional)
    return cleaned


def format_paragraphs(paragraphs: List[str]) -> List[str]:
    """Format a list of paragraphs, filtering out empty ones.
    
    This is a convenience function that applies format_paragraph() to each
    paragraph in a list and filters out any that become empty.
    
    Args:
        paragraphs: List of raw paragraph texts
        
    Returns:
        List of formatted paragraphs with empty ones removed
        
    Examples:
        >>> format_paragraphs(["  First para  ", "", "  Second para  "])
        ["First para", "Second para"]
    """
    return [p for p in (format_paragraph(para) for para in paragraphs) if p]
