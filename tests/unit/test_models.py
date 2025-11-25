"""
Unit tests for data models (ReadingEntry and DailyReading).

Tests validation logic, properties, and edge cases for the core data structures.
"""

import pytest
from datetime import date
from pathlib import Path

from catholic_liturgy_tools.scraper.models import DailyReading, ReadingEntry
from catholic_liturgy_tools.scraper.exceptions import ValidationError


class TestReadingEntry:
    """Tests for the ReadingEntry dataclass."""
    
    def test_create_valid_reading_entry(self):
        """Test creating a valid reading entry."""
        entry = ReadingEntry(
            title="Gospel",
            citation="Luke 21:5-11",
            text=["While some people were speaking about...", "Jesus said to his disciples..."]
        )
        
        assert entry.title == "Gospel"
        assert entry.citation == "Luke 21:5-11"
        assert len(entry.text) == 2
        assert entry.text[0] == "While some people were speaking about..."
    
    def test_reading_entry_validate_success(self):
        """Test that valid reading entry passes validation."""
        entry = ReadingEntry(
            title="First Reading",
            citation="1 Corinthians 15:54-58",
            text=["Brothers and sisters..."]
        )
        
        # Should not raise
        entry.validate()
    
    def test_reading_entry_empty_title(self):
        """Test that empty title fails validation."""
        entry = ReadingEntry(
            title="",
            citation="Luke 21:5-11",
            text=["Some text"]
        )
        
        with pytest.raises(ValidationError) as exc_info:
            entry.validate()
        
        assert exc_info.value.field == "title"
        assert "title cannot be empty" in str(exc_info.value).lower()
    
    def test_reading_entry_whitespace_title(self):
        """Test that whitespace-only title fails validation."""
        entry = ReadingEntry(
            title="   ",
            citation="Luke 21:5-11",
            text=["Some text"]
        )
        
        with pytest.raises(ValidationError) as exc_info:
            entry.validate()
        
        assert exc_info.value.field == "title"
    
    def test_reading_entry_empty_citation(self):
        """Test that empty citation fails validation."""
        entry = ReadingEntry(
            title="Gospel",
            citation="",
            text=["Some text"]
        )
        
        with pytest.raises(ValidationError) as exc_info:
            entry.validate()
        
        assert exc_info.value.field == "citation"
        assert "citation cannot be empty" in str(exc_info.value).lower()
    
    def test_reading_entry_whitespace_citation(self):
        """Test that whitespace-only citation fails validation."""
        entry = ReadingEntry(
            title="Gospel",
            citation="   ",
            text=["Some text"]
        )
        
        with pytest.raises(ValidationError) as exc_info:
            entry.validate()
        
        assert exc_info.value.field == "citation"
    
    def test_reading_entry_empty_text(self):
        """Test that empty text list fails validation."""
        entry = ReadingEntry(
            title="Gospel",
            citation="Luke 21:5-11",
            text=[]
        )
        
        with pytest.raises(ValidationError) as exc_info:
            entry.validate()
        
        assert exc_info.value.field == "text"
        assert "text cannot be empty" in str(exc_info.value).lower()
    
    def test_reading_entry_whitespace_only_text(self):
        """Test that text with only whitespace fails validation."""
        entry = ReadingEntry(
            title="Gospel",
            citation="Luke 21:5-11",
            text=["   ", "  ", "\n"]
        )
        
        with pytest.raises(ValidationError) as exc_info:
            entry.validate()
        
        assert exc_info.value.field == "text"
    
    def test_reading_entry_title_with_citation_property(self):
        """Test the title_with_citation property."""
        entry = ReadingEntry(
            title="Gospel",
            citation="Luke 21:5-11",
            text=["Some text"]
        )
        
        assert entry.title_with_citation == "Gospel (Luke 21:5-11)"
    
    def test_reading_entry_title_with_citation_different_values(self):
        """Test title_with_citation with various titles and citations."""
        test_cases = [
            ("First Reading", "1 Corinthians 15:54-58", "First Reading (1 Corinthians 15:54-58)"),
            ("Responsorial Psalm", "Psalm 98:1, 2-3ab, 3cd-4", "Responsorial Psalm (Psalm 98:1, 2-3ab, 3cd-4)"),
            ("Gospel", "John 3:16", "Gospel (John 3:16)"),
        ]
        
        for title, citation, expected in test_cases:
            entry = ReadingEntry(title=title, citation=citation, text=["text"])
            assert entry.title_with_citation == expected
    
    def test_reading_entry_default_text(self):
        """Test that text defaults to empty list."""
        entry = ReadingEntry(title="Gospel", citation="Luke 21:5-11")
        assert entry.text == []


class TestDailyReading:
    """Tests for the DailyReading dataclass."""
    
    def test_create_valid_daily_reading(self):
        """Test creating a valid daily reading."""
        reading_date = date(2025, 11, 22)
        entries = [
            ReadingEntry(
                title="First Reading",
                citation="1 Corinthians 15:54-58",
                text=["Brothers and sisters..."]
            ),
            ReadingEntry(
                title="Gospel",
                citation="Luke 21:5-11",
                text=["While some people were speaking..."]
            )
        ]
        
        daily = DailyReading(
            date=reading_date,
            date_display="Friday, November 22, 2025",
            liturgical_day="Friday of the Thirty-fourth Week in Ordinary Time",
            readings=entries,
            source_url="https://bible.usccb.org/bible/readings/112225.cfm"
        )
        
        assert daily.date == reading_date
        assert daily.date_display == "Friday, November 22, 2025"
        assert daily.liturgical_day == "Friday of the Thirty-fourth Week in Ordinary Time"
        assert len(daily.readings) == 2
        assert daily.source_url == "https://bible.usccb.org/bible/readings/112225.cfm"
    
    def test_daily_reading_validate_success(self):
        """Test that valid daily reading passes validation."""
        entries = [
            ReadingEntry(
                title="Gospel",
                citation="Luke 21:5-11",
                text=["Some text"]
            )
        ]
        
        daily = DailyReading(
            date=date(2025, 11, 22),
            date_display="Friday, November 22, 2025",
            liturgical_day="Friday of the Thirty-fourth Week in Ordinary Time",
            readings=entries,
            source_url="https://bible.usccb.org/bible/readings/112225.cfm"
        )
        
        # Should not raise
        daily.validate()
    
    def test_daily_reading_invalid_date_type(self):
        """Test that invalid date type fails validation."""
        entries = [ReadingEntry(title="Gospel", citation="Luke 21:5-11", text=["text"])]
        
        daily = DailyReading(
            date="2025-11-22",  # String instead of date object
            date_display="Friday, November 22, 2025",
            liturgical_day="Friday",
            readings=entries,
            source_url="https://example.com"
        )
        
        with pytest.raises(ValidationError) as exc_info:
            daily.validate()
        
        assert exc_info.value.field == "date"
        assert "date object" in str(exc_info.value).lower()
    
    def test_daily_reading_empty_date_display(self):
        """Test that empty date_display fails validation."""
        entries = [ReadingEntry(title="Gospel", citation="Luke 21:5-11", text=["text"])]
        
        daily = DailyReading(
            date=date(2025, 11, 22),
            date_display="",
            liturgical_day="Friday",
            readings=entries,
            source_url="https://example.com"
        )
        
        with pytest.raises(ValidationError) as exc_info:
            daily.validate()
        
        assert exc_info.value.field == "date_display"
    
    def test_daily_reading_empty_liturgical_day(self):
        """Test that empty liturgical_day fails validation."""
        entries = [ReadingEntry(title="Gospel", citation="Luke 21:5-11", text=["text"])]
        
        daily = DailyReading(
            date=date(2025, 11, 22),
            date_display="Friday, November 22, 2025",
            liturgical_day="",
            readings=entries,
            source_url="https://example.com"
        )
        
        with pytest.raises(ValidationError) as exc_info:
            daily.validate()
        
        assert exc_info.value.field == "liturgical_day"
    
    def test_daily_reading_empty_readings_list(self):
        """Test that empty readings list fails validation."""
        daily = DailyReading(
            date=date(2025, 11, 22),
            date_display="Friday, November 22, 2025",
            liturgical_day="Friday",
            readings=[],
            source_url="https://example.com"
        )
        
        with pytest.raises(ValidationError) as exc_info:
            daily.validate()
        
        assert exc_info.value.field == "readings"
        assert "cannot be empty" in str(exc_info.value).lower()
    
    def test_daily_reading_invalid_reading_entry(self):
        """Test that invalid reading entry in list fails validation."""
        invalid_entry = ReadingEntry(
            title="",  # Invalid empty title
            citation="Luke 21:5-11",
            text=["text"]
        )
        
        daily = DailyReading(
            date=date(2025, 11, 22),
            date_display="Friday, November 22, 2025",
            liturgical_day="Friday",
            readings=[invalid_entry],
            source_url="https://example.com"
        )
        
        with pytest.raises(ValidationError) as exc_info:
            daily.validate()
        
        assert "readings[0]" in exc_info.value.field
        assert "title" in exc_info.value.field
    
    def test_daily_reading_multiple_entries_one_invalid(self):
        """Test that one invalid entry among multiple fails validation."""
        valid_entry = ReadingEntry(
            title="First Reading",
            citation="1 Corinthians 15:54-58",
            text=["text"]
        )
        invalid_entry = ReadingEntry(
            title="Gospel",
            citation="",  # Invalid empty citation
            text=["text"]
        )
        
        daily = DailyReading(
            date=date(2025, 11, 22),
            date_display="Friday, November 22, 2025",
            liturgical_day="Friday",
            readings=[valid_entry, invalid_entry],
            source_url="https://example.com"
        )
        
        with pytest.raises(ValidationError) as exc_info:
            daily.validate()
        
        assert "readings[1]" in exc_info.value.field
    
    def test_daily_reading_empty_source_url(self):
        """Test that empty source_url fails validation."""
        entries = [ReadingEntry(title="Gospel", citation="Luke 21:5-11", text=["text"])]
        
        daily = DailyReading(
            date=date(2025, 11, 22),
            date_display="Friday, November 22, 2025",
            liturgical_day="Friday",
            readings=entries,
            source_url=""
        )
        
        with pytest.raises(ValidationError) as exc_info:
            daily.validate()
        
        assert exc_info.value.field == "source_url"
    
    def test_daily_reading_filename_property(self):
        """Test the filename property."""
        entries = [ReadingEntry(title="Gospel", citation="Luke 21:5-11", text=["text"])]
        
        daily = DailyReading(
            date=date(2025, 11, 22),
            date_display="Friday, November 22, 2025",
            liturgical_day="Friday",
            readings=entries,
            source_url="https://example.com"
        )
        
        assert daily.filename == "2025-11-22.html"
    
    def test_daily_reading_filename_different_dates(self):
        """Test filename property with various dates."""
        entries = [ReadingEntry(title="Gospel", citation="Luke 21:5-11", text=["text"])]
        
        test_cases = [
            (date(2025, 1, 1), "2025-01-01.html"),
            (date(2025, 12, 25), "2025-12-25.html"),
            (date(2024, 2, 29), "2024-02-29.html"),  # Leap year
        ]
        
        for test_date, expected_filename in test_cases:
            daily = DailyReading(
                date=test_date,
                date_display="Some date",
                liturgical_day="Some day",
                readings=entries,
                source_url="https://example.com"
            )
            assert daily.filename == expected_filename
    
    def test_daily_reading_file_path_property(self):
        """Test the file_path property."""
        entries = [ReadingEntry(title="Gospel", citation="Luke 21:5-11", text=["text"])]
        
        daily = DailyReading(
            date=date(2025, 11, 22),
            date_display="Friday, November 22, 2025",
            liturgical_day="Friday",
            readings=entries,
            source_url="https://example.com"
        )
        
        assert daily.file_path == Path("readings/2025-11-22.html")
        assert isinstance(daily.file_path, Path)
    
    def test_daily_reading_default_readings(self):
        """Test that readings defaults to empty list."""
        daily = DailyReading(
            date=date(2025, 11, 22),
            date_display="Friday, November 22, 2025",
            liturgical_day="Friday",
            source_url="https://example.com"
        )
        assert daily.readings == []
    
    def test_daily_reading_default_source_url(self):
        """Test that source_url defaults to empty string."""
        entries = [ReadingEntry(title="Gospel", citation="Luke 21:5-11", text=["text"])]
        daily = DailyReading(
            date=date(2025, 11, 22),
            date_display="Friday, November 22, 2025",
            liturgical_day="Friday",
            readings=entries
        )
        assert daily.source_url == ""
    
    def test_daily_reading_multiple_readings_valid(self):
        """Test daily reading with multiple reading entries."""
        entries = [
            ReadingEntry(
                title="First Reading",
                citation="1 Corinthians 15:54-58",
                text=["Brothers and sisters..."]
            ),
            ReadingEntry(
                title="Responsorial Psalm",
                citation="Psalm 98:1, 2-3ab, 3cd-4",
                text=["R. The Lord comes to rule the earth with justice."]
            ),
            ReadingEntry(
                title="Gospel",
                citation="Luke 21:5-11",
                text=["While some people were speaking..."]
            )
        ]
        
        daily = DailyReading(
            date=date(2025, 11, 22),
            date_display="Friday, November 22, 2025",
            liturgical_day="Friday of the Thirty-fourth Week in Ordinary Time",
            readings=entries,
            source_url="https://bible.usccb.org/bible/readings/112225.cfm"
        )
        
        daily.validate()  # Should not raise
        assert len(daily.readings) == 3
