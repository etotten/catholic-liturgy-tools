"""Integration tests for content accumulation across multiple runs (User Story 1).

This test module verifies that content accumulates in _site/ directory over time,
which is the core behavior for feature 004-preserve-site-history.
"""

import pytest
from pathlib import Path
from datetime import datetime
from catholic_liturgy_tools.generator.message import generate_message
from catholic_liturgy_tools.generator.readings import generate_readings_page
from catholic_liturgy_tools.generator.index import generate_index
from catholic_liturgy_tools.scraper.models import DailyReading, ReadingEntry


def parse_date_string(date_str: str):
    """Helper to convert YYYY-MM-DD string to datetime.date object."""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


class TestContentAccumulation:
    """Test that content accumulates across multiple generation runs."""
    
    def test_message_accumulation_across_runs(self, temp_dir):
        """Verify that message files accumulate when generating for different dates.
        
        This simulates multiple workflow runs where each run generates content
        for a different date. All previous content should be preserved.
        """
        messages_dir = temp_dir / "_site" / "messages"
        
        # Run 1: Generate message for Day 1
        date1 = "2025-11-23"
        msg_file1 = generate_message(output_dir=str(messages_dir), date=date1)
        
        # Verify Day 1 exists
        assert msg_file1.exists()
        assert msg_file1.name == f"{date1}-daily-message.md"
        assert len(list(messages_dir.glob("*-daily-message.md"))) == 1
        
        # Run 2: Generate message for Day 2
        date2 = "2025-11-24"
        msg_file2 = generate_message(output_dir=str(messages_dir), date=date2)
        
        # Verify BOTH Day 1 and Day 2 exist (accumulation)
        assert msg_file1.exists(), "Day 1 message should still exist"
        assert msg_file2.exists(), "Day 2 message should exist"
        assert msg_file2.name == f"{date2}-daily-message.md"
        assert len(list(messages_dir.glob("*-daily-message.md"))) == 2
        
        # Run 3: Generate message for Day 3
        date3 = "2025-11-25"
        msg_file3 = generate_message(output_dir=str(messages_dir), date=date3)
        
        # Verify ALL THREE days exist (continued accumulation)
        assert msg_file1.exists(), "Day 1 message should still exist"
        assert msg_file2.exists(), "Day 2 message should still exist"
        assert msg_file3.exists(), "Day 3 message should exist"
        assert msg_file3.name == f"{date3}-daily-message.md"
        assert len(list(messages_dir.glob("*-daily-message.md"))) == 3
    
    def test_readings_accumulation_across_runs(self, temp_dir):
        """Verify that readings files accumulate when generating for different dates.
        
        This simulates multiple workflow runs where each run generates readings
        for a different date. All previous content should be preserved.
        """
        readings_dir = temp_dir / "_site" / "readings"
        readings_dir.mkdir(parents=True, exist_ok=True)
        
        # Helper function to create a minimal DailyReading
        def create_test_reading(date: str, liturgical_day: str) -> DailyReading:
            return DailyReading(
                date=parse_date_string(date),
                date_display=f"{date} Display",
                liturgical_day=liturgical_day,
                readings=[
                    ReadingEntry(
                        title="First Reading",
                        citation="Genesis 1:1-2",
                        text="In the beginning..."
                    )
                ],
                source_url="https://bible.usccb.org/bible/readings/test.cfm"
            )
        
        # Run 1: Generate readings for Day 1
        date1 = "2025-11-23"
        reading1 = create_test_reading(date1, "Saturday of the Thirty-fourth Week in Ordinary Time")
        reading_file1 = generate_readings_page(reading1, output_dir=str(readings_dir))
        
        # Verify Day 1 exists
        assert reading_file1.exists()
        assert reading_file1.name == f"{date1}.html"
        assert len(list(readings_dir.glob("*.html"))) == 1
        
        # Run 2: Generate readings for Day 2
        date2 = "2025-11-24"
        reading2 = create_test_reading(date2, "First Sunday of Advent")
        reading_file2 = generate_readings_page(reading2, output_dir=str(readings_dir))
        
        # Verify BOTH Day 1 and Day 2 exist (accumulation)
        assert reading_file1.exists(), "Day 1 reading should still exist"
        assert reading_file2.exists(), "Day 2 reading should exist"
        assert reading_file2.name == f"{date2}.html"
        assert len(list(readings_dir.glob("*.html"))) == 2
        
        # Run 3: Generate readings for Day 3
        date3 = "2025-11-25"
        reading3 = create_test_reading(date3, "Monday of the First Week of Advent")
        reading_file3 = generate_readings_page(reading3, output_dir=str(readings_dir))
        
        # Verify ALL THREE days exist (continued accumulation)
        assert reading_file1.exists(), "Day 1 reading should still exist"
        assert reading_file2.exists(), "Day 2 reading should still exist"
        assert reading_file3.exists(), "Day 3 reading should exist"
        assert reading_file3.name == f"{date3}.html"
        assert len(list(readings_dir.glob("*.html"))) == 3
    
    def test_index_reflects_accumulated_content(self, temp_dir):
        """Verify that index page lists all accumulated content correctly.
        
        This tests the complete workflow: generate messages, generate readings,
        then generate index - and verify the index lists all content.
        """
        site_dir = temp_dir / "_site"
        messages_dir = site_dir / "messages"
        readings_dir = site_dir / "readings"
        
        # Helper for creating readings
        def create_test_reading(date: str, liturgical_day: str) -> DailyReading:
            return DailyReading(
                date=parse_date_string(date),
                date_display=f"{date} Display",
                liturgical_day=liturgical_day,
                readings=[
                    ReadingEntry(
                        title="First Reading",
                        citation="Genesis 1:1-2",
                        text="In the beginning..."
                    )
                ],
                source_url="https://bible.usccb.org/bible/readings/test.cfm"
            )
        
        # Generate content for 3 dates
        dates = ["2025-11-23", "2025-11-24", "2025-11-25"]
        liturgical_days = [
            "Saturday of the Thirty-fourth Week in Ordinary Time",
            "First Sunday of Advent",
            "Monday of the First Week of Advent"
        ]
        
        for date, liturgical_day in zip(dates, liturgical_days):
            # Generate message
            generate_message(output_dir=str(messages_dir), date=parse_date_string(date))
            
            # Generate reading
            reading = create_test_reading(date, liturgical_day)
            generate_readings_page(reading, output_dir=str(readings_dir))
        
        # Generate index
        index_path = generate_index(
            posts_dir=str(messages_dir),
            readings_dir=str(readings_dir),
            output_file=str(site_dir / "index.html")
        )
        
        # Verify index was created
        assert index_path.exists()
        index_content = index_path.read_text()
        
        # Verify all dates appear in the index
        for date in dates:
            assert date in index_content, f"Date {date} should appear in index"
        
        # Verify all liturgical days appear in the index
        for liturgical_day in liturgical_days:
            assert liturgical_day in index_content, f"Liturgical day '{liturgical_day}' should appear in index"
        
        # Verify messages section has all 3 links
        assert index_content.count('<a href="messages/') == 3, "Should have 3 message links"
        
        # Verify readings section has all 3 links
        assert index_content.count('<a href="readings/') == 3, "Should have 3 readings links"
