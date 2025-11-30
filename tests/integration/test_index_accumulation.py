"""Integration tests for index page accumulation (User Story 2).

This test module verifies that the index page correctly lists all accumulated
historical content in reverse chronological order.
"""

import pytest
from pathlib import Path
from datetime import datetime
from catholic_liturgy_tools.generator.message import generate_message
from catholic_liturgy_tools.generator.readings import generate_readings_page
from catholic_liturgy_tools.generator.index import generate_index, scan_message_files, scan_readings_files
from catholic_liturgy_tools.scraper.models import DailyReading, ReadingEntry


def parse_date_string(date_str: str):
    """Helper to convert YYYY-MM-DD string to datetime.date object."""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


class TestIndexAccumulation:
    """Test that index page correctly displays all accumulated content."""
    
    def test_index_lists_multiple_message_entries(self, temp_dir):
        """Verify that index lists all message files when multiple dates exist."""
        site_dir = temp_dir / "_site"
        messages_dir = site_dir / "messages"
        readings_dir = site_dir / "readings"
        
        # Generate messages for 5 different dates
        dates = ["2025-11-20", "2025-11-21", "2025-11-22", "2025-11-23", "2025-11-24"]
        for date in dates:
            generate_message(output_dir=str(messages_dir), date=parse_date_string(date))
        
        # Generate empty readings directory (to avoid errors)
        readings_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate index
        index_path = generate_index(
            posts_dir=str(messages_dir),
            readings_dir=str(readings_dir),
            output_file=str(site_dir / "index.html")
        )
        
        # Verify index exists
        assert index_path.exists()
        index_content = index_path.read_text()
        
        # Count message links in index
        message_link_count = index_content.count('<a href="messages/')
        assert message_link_count == 5, f"Expected 5 message links, found {message_link_count}"
        
        # Verify all dates appear in index
        for date in dates:
            assert date in index_content, f"Date {date} should appear in index"
    
    def test_index_lists_multiple_readings_entries(self, temp_dir):
        """Verify that index lists all readings files when multiple dates exist."""
        site_dir = temp_dir / "_site"
        messages_dir = site_dir / "messages"
        readings_dir = site_dir / "readings"
        
        # Generate messages directory (empty)
        messages_dir.mkdir(parents=True, exist_ok=True)
        
        # Helper to create readings
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
        
        # Generate readings for 5 different dates
        dates_and_days = [
            ("2025-11-20", "Wednesday of Week 34"),
            ("2025-11-21", "Thursday of Week 34"),
            ("2025-11-22", "Friday of Week 34"),
            ("2025-11-23", "Saturday of Week 34"),
            ("2025-11-24", "First Sunday of Advent"),
        ]
        
        for date, liturgical_day in dates_and_days:
            reading = create_test_reading(date, liturgical_day)
            generate_readings_page(reading, output_dir=str(readings_dir))
        
        # Generate index
        index_path = generate_index(
            posts_dir=str(messages_dir),
            readings_dir=str(readings_dir),
            output_file=str(site_dir / "index.html")
        )
        
        # Verify index exists
        assert index_path.exists()
        index_content = index_path.read_text()
        
        # Count readings links in index
        readings_link_count = index_content.count('<a href="readings/')
        assert readings_link_count == 5, f"Expected 5 readings links, found {readings_link_count}"
        
        # Verify all dates and liturgical days appear in index
        for date, liturgical_day in dates_and_days:
            assert date in index_content, f"Date {date} should appear in index"
            assert liturgical_day in index_content, f"Liturgical day '{liturgical_day}' should appear in index"
    
    def test_index_maintains_reverse_chronological_order(self, temp_dir):
        """Verify that index maintains reverse chronological order (newest first)."""
        site_dir = temp_dir / "_site"
        messages_dir = site_dir / "messages"
        readings_dir = site_dir / "readings"
        
        # Generate messages in random order
        dates = ["2025-11-22", "2025-11-20", "2025-11-24", "2025-11-21", "2025-11-23"]
        for date in dates:
            generate_message(output_dir=str(messages_dir), date=parse_date_string(date))
        
        # Generate empty readings directory
        readings_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate index
        index_path = generate_index(
            posts_dir=str(messages_dir),
            readings_dir=str(readings_dir),
            output_file=str(site_dir / "index.html")
        )
        
        # Read index content
        index_content = index_path.read_text()
        
        # Find positions of each date in the index
        # Expected order: 2025-11-24, 2025-11-23, 2025-11-22, 2025-11-21, 2025-11-20
        pos_20 = index_content.index("2025-11-20")
        pos_21 = index_content.index("2025-11-21")
        pos_22 = index_content.index("2025-11-22")
        pos_23 = index_content.index("2025-11-23")
        pos_24 = index_content.index("2025-11-24")
        
        # Verify order (newer dates appear earlier = lower position)
        assert pos_24 < pos_23, "2025-11-24 should appear before 2025-11-23"
        assert pos_23 < pos_22, "2025-11-23 should appear before 2025-11-22"
        assert pos_22 < pos_21, "2025-11-22 should appear before 2025-11-21"
        assert pos_21 < pos_20, "2025-11-21 should appear before 2025-11-20"
    
    def test_scan_functions_discover_all_files(self, temp_dir):
        """Verify that scan functions discover ALL files, not just latest."""
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
        
        # Generate 10 messages
        message_dates = [f"2025-11-{i:02d}" for i in range(15, 25)]  # 15-24
        for date in message_dates:
            generate_message(output_dir=str(messages_dir), date=parse_date_string(date))
        
        # Generate 10 readings
        reading_dates = [f"2025-11-{i:02d}" for i in range(15, 25)]  # 15-24
        for date in reading_dates:
            reading = create_test_reading(date, f"Day {date}")
            generate_readings_page(reading, output_dir=str(readings_dir))
        
        # Test scan_message_files
        discovered_messages = scan_message_files(str(messages_dir))
        assert len(discovered_messages) == 10, f"Expected 10 messages, found {len(discovered_messages)}"
        
        # Test scan_readings_files
        discovered_readings = scan_readings_files(str(readings_dir))
        assert len(discovered_readings) == 10, f"Expected 10 readings, found {len(discovered_readings)}"
        
        # Verify all discovered messages are in reverse chronological order
        for i in range(len(discovered_messages) - 1):
            current_date = discovered_messages[i].stem.split("-daily-message")[0]
            next_date = discovered_messages[i + 1].stem.split("-daily-message")[0]
            assert current_date > next_date, f"Messages not in reverse chronological order: {current_date} vs {next_date}"
        
        # Verify all discovered readings are in reverse chronological order
        for i in range(len(discovered_readings) - 1):
            current_date = discovered_readings[i].date
            next_date = discovered_readings[i + 1].date
            assert current_date > next_date, f"Readings not in reverse chronological order: {current_date} vs {next_date}"
    
    def test_index_includes_both_messages_and_readings_links(self, temp_dir):
        """Verify that index includes links to both messages and readings."""
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
        
        # Generate 3 messages and 3 readings
        dates = ["2025-11-22", "2025-11-23", "2025-11-24"]
        liturgical_days = ["Friday of Week 34", "Saturday of Week 34", "First Sunday of Advent"]
        
        for date in dates:
            generate_message(output_dir=str(messages_dir), date=parse_date_string(date))
        
        for date, liturgical_day in zip(dates, liturgical_days):
            reading = create_test_reading(date, liturgical_day)
            generate_readings_page(reading, output_dir=str(readings_dir))
        
        # Generate index
        index_path = generate_index(
            posts_dir=str(messages_dir),
            readings_dir=str(readings_dir),
            output_file=str(site_dir / "index.html")
        )
        
        # Read index content
        index_content = index_path.read_text()
        
        # Verify both sections exist
        assert "Daily Messages" in index_content or "Messages" in index_content, "Should have messages section"
        assert "Daily Readings" in index_content or "Readings" in index_content, "Should have readings section"
        
        # Verify correct number of links
        message_links = index_content.count('<a href="messages/')
        readings_links = index_content.count('<a href="readings/')
        
        assert message_links == 3, f"Expected 3 message links, found {message_links}"
        assert readings_links == 3, f"Expected 3 readings links, found {readings_links}"
        
        # Verify all dates appear
        for date in dates:
            # Each date should appear twice: once in messages, once in readings
            assert index_content.count(date) >= 2, f"Date {date} should appear at least twice (messages and readings)"
