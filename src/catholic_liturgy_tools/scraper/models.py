"""
Data models for Catholic liturgical readings.

This module defines the core data structures for representing daily readings
from the Catholic Lectionary, including individual reading entries and
complete daily reading collections.
"""

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import List

from .exceptions import ValidationError


@dataclass
class ReadingEntry:
    """
    Represents a single reading entry (e.g., First Reading, Gospel).
    
    Attributes:
        title: The reading title (e.g., "First Reading", "Gospel")
        citation: The biblical citation (e.g., "1 Corinthians 15:54-58")
        text: List of paragraphs containing the reading text
    
    Example:
        >>> entry = ReadingEntry(
        ...     title="Gospel",
        ...     citation="Luke 21:5-11",
        ...     text=["While some people were speaking...", "Jesus said to his disciples..."]
        ... )
        >>> entry.validate()
        >>> print(entry.title_with_citation)
        'Gospel (Luke 21:5-11)'
    """
    
    title: str
    citation: str
    text: List[str] = field(default_factory=list)
    
    def validate(self) -> None:
        """
        Validate the reading entry data.
        
        Raises:
            ValidationError: If any required field is missing or invalid
        """
        if not self.title or not self.title.strip():
            raise ValidationError("Reading title cannot be empty", field="title", value=self.title)
        
        if not self.citation or not self.citation.strip():
            raise ValidationError("Reading citation cannot be empty", field="citation", value=self.citation)
        
        if not self.text or not any(p.strip() for p in self.text):
            raise ValidationError("Reading text cannot be empty", field="text", value=self.text)
    
    @property
    def title_with_citation(self) -> str:
        """
        Get formatted title with citation.
        
        Returns:
            Formatted string like "Gospel (Luke 21:5-11)"
        """
        return f"{self.title} ({self.citation})"


@dataclass
class DailyReading:
    """
    Represents the complete set of readings for a single day.
    
    Attributes:
        date: The date for these readings
        date_display: Human-readable date string (e.g., "Friday, November 22, 2025")
        liturgical_day: The liturgical day name (e.g., "Friday of the Thirty-fourth Week in Ordinary Time")
        readings: List of reading entries for this day
        source_url: URL where readings were fetched from
    
    Example:
        >>> from datetime import date
        >>> daily = DailyReading(
        ...     date=date(2025, 11, 22),
        ...     date_display="Friday, November 22, 2025",
        ...     liturgical_day="Friday of the Thirty-fourth Week in Ordinary Time",
        ...     readings=[...],
        ...     source_url="https://bible.usccb.org/bible/readings/112225.cfm"
        ... )
        >>> daily.validate()
        >>> print(daily.filename)
        '2025-11-22.html'
    """
    
    date: date
    date_display: str
    liturgical_day: str
    readings: List[ReadingEntry] = field(default_factory=list)
    source_url: str = ""
    
    def validate(self) -> None:
        """
        Validate the daily reading data.
        
        Raises:
            ValidationError: If any required field is missing or invalid
        """
        if not isinstance(self.date, date):
            raise ValidationError("Date must be a datetime.date object", field="date", value=self.date)
        
        if not self.date_display or not self.date_display.strip():
            raise ValidationError("Date display cannot be empty", field="date_display", value=self.date_display)
        
        if not self.liturgical_day or not self.liturgical_day.strip():
            raise ValidationError("Liturgical day cannot be empty", field="liturgical_day", value=self.liturgical_day)
        
        if not self.readings:
            raise ValidationError("Readings list cannot be empty", field="readings", value=self.readings)
        
        if len(self.readings) < 1:
            raise ValidationError("Must have at least one reading", field="readings", value=len(self.readings))
        
        # Validate each reading entry
        for i, reading in enumerate(self.readings):
            try:
                reading.validate()
            except ValidationError as e:
                raise ValidationError(
                    f"Invalid reading at index {i}: {e}",
                    field=f"readings[{i}].{e.field}",
                    value=e.value
                )
        
        if not self.source_url or not self.source_url.strip():
            raise ValidationError("Source URL cannot be empty", field="source_url", value=self.source_url)
    
    @property
    def filename(self) -> str:
        """
        Get the filename for this reading (without directory).
        
        Returns:
            Filename in format "YYYY-MM-DD.html"
        """
        return f"{self.date.isoformat()}.html"
    
    @property
    def file_path(self) -> Path:
        """
        Get the relative file path for this reading.
        
        Returns:
            Path object like "readings/2025-11-22.html"
        """
        return Path("readings") / self.filename
