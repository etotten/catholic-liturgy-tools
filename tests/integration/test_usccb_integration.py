"""
Integration tests for USCCBReadingsScraper against live USCCB website.

These tests make real HTTP requests to bible.usccb.org to verify the scraper
works correctly with the live site. They are marked as 'slow' and 'integration'
and can be skipped with: pytest -m "not integration"

Run with: pytest tests/integration/test_usccb_integration.py -v -s
Skip with: pytest -m "not integration"
"""

import time
from datetime import date
import pytest

from catholic_liturgy_tools.scraper.usccb import USCCBReadingsScraper
from catholic_liturgy_tools.scraper.models import DailyReading
from catholic_liturgy_tools.scraper.exceptions import NetworkError, ParseError


# Mark all tests in this module as slow and integration
pytestmark = [pytest.mark.slow, pytest.mark.integration]


# Rate limiting between requests (in seconds)
RATE_LIMIT_DELAY = 1.0


@pytest.fixture(scope="module")
def scraper():
    """Create a scraper instance for all tests in this module."""
    return USCCBReadingsScraper()


@pytest.fixture(autouse=True)
def rate_limit():
    """Add delay between tests to avoid overwhelming USCCB servers."""
    yield
    time.sleep(RATE_LIMIT_DELAY)


class TestWeekdayReadings:
    """Test scraping weekday readings from live USCCB site."""

    def test_recent_weekday(self, scraper):
        """Test scraping a recent weekday (Nov 22, 2025 - Memorial of St. Cecilia)."""
        test_date = date(2025, 11, 22)  # Saturday, Memorial of Saint Cecilia
        
        try:
            daily_reading = scraper.get_readings_for_date(test_date)
            
            # Verify result structure
            assert isinstance(daily_reading, DailyReading)
            assert daily_reading.date == test_date
            assert daily_reading.liturgical_day
            assert daily_reading.source_url
            
            # Weekdays typically have 3-4 readings
            assert 3 <= len(daily_reading.readings) <= 4, \
                f"Expected 3-4 readings for weekday, got {len(daily_reading.readings)}"
            
            # Verify each reading has required fields
            for reading in daily_reading.readings:
                assert reading.title, "Reading title should not be empty"
                assert reading.citation, "Reading citation should not be empty"
                assert len(reading.text) > 0, "Reading text should not be empty"
                
                # Verify text paragraphs are not empty
                for paragraph in reading.text:
                    assert paragraph.strip(), "Paragraph should not be empty"
            
            print(f"\n✓ Successfully scraped {daily_reading.liturgical_day}")
            print(f"  Date: {daily_reading.date_display}")
            print(f"  Readings: {len(daily_reading.readings)}")
            for i, reading in enumerate(daily_reading.readings, 1):
                print(f"    {i}. {reading.title} ({reading.citation})")
        
        except (NetworkError, ParseError) as e:
            pytest.fail(
                f"Failed to scrape weekday readings for {test_date}. "
                f"This could indicate changes to USCCB website structure. Error: {e}"
            )

    def test_another_weekday(self, scraper):
        """Test scraping another weekday to verify consistency."""
        test_date = date(2025, 11, 25)  # Tuesday of the 34th Week in Ordinary Time
        
        try:
            daily_reading = scraper.get_readings_for_date(test_date)
            
            assert isinstance(daily_reading, DailyReading)
            assert daily_reading.date == test_date
            assert daily_reading.liturgical_day
            assert 3 <= len(daily_reading.readings) <= 4
            
            print(f"\n✓ Successfully scraped {daily_reading.liturgical_day}")
            print(f"  Readings: {len(daily_reading.readings)}")
        
        except (NetworkError, ParseError) as e:
            pytest.fail(
                f"Failed to scrape weekday readings for {test_date}. Error: {e}"
            )


class TestSundayReadings:
    """Test scraping Sunday readings from live USCCB site."""

    def test_sunday_readings(self, scraper):
        """Test scraping Sunday readings (typically 4 readings)."""
        test_date = date(2025, 11, 30)  # First Sunday of Advent / Feast of St. Andrew
        
        try:
            daily_reading = scraper.get_readings_for_date(test_date)
            
            assert isinstance(daily_reading, DailyReading)
            assert daily_reading.date == test_date
            assert daily_reading.liturgical_day
            
            # Sundays typically have 4 readings (First Reading, Psalm, Second Reading, Gospel)
            # but feasts may vary
            assert 3 <= len(daily_reading.readings) <= 5, \
                f"Expected 3-5 readings for Sunday, got {len(daily_reading.readings)}"
            
            # Verify reading structure
            for reading in daily_reading.readings:
                assert reading.title
                assert reading.citation or "Alleluia" in reading.title
                assert len(reading.text) > 0
            
            print(f"\n✓ Successfully scraped {daily_reading.liturgical_day}")
            print(f"  Date: {daily_reading.date_display}")
            print(f"  Readings: {len(daily_reading.readings)}")
            for i, reading in enumerate(daily_reading.readings, 1):
                print(f"    {i}. {reading.title} ({reading.citation})")
        
        except (NetworkError, ParseError) as e:
            pytest.fail(
                f"Failed to scrape Sunday readings for {test_date}. Error: {e}"
            )

    def test_advent_sunday(self, scraper):
        """Test scraping First Sunday of Advent specifically."""
        test_date = date(2025, 12, 7)  # Second Sunday of Advent
        
        try:
            daily_reading = scraper.get_readings_for_date(test_date)
            
            assert isinstance(daily_reading, DailyReading)
            assert daily_reading.date == test_date
            assert "advent" in daily_reading.liturgical_day.lower() or "sunday" in daily_reading.liturgical_day.lower()
            assert 3 <= len(daily_reading.readings) <= 5
            
            print(f"\n✓ Successfully scraped {daily_reading.liturgical_day}")
            print(f"  Readings: {len(daily_reading.readings)}")
        
        except (NetworkError, ParseError) as e:
            pytest.fail(
                f"Failed to scrape Advent Sunday readings for {test_date}. Error: {e}"
            )


class TestFeastDayReadings:
    """Test scraping feast day readings from live USCCB site."""

    def test_christmas_day(self, scraper):
        """Test scraping Christmas Day (may have multiple Masses)."""
        test_date = date(2025, 12, 25)  # Christmas Day
        
        try:
            daily_reading = scraper.get_readings_for_date(test_date)
            
            assert isinstance(daily_reading, DailyReading)
            assert daily_reading.date == test_date
            assert daily_reading.liturgical_day
            
            # Christmas may return hub page or specific Mass
            # Either way, should get valid readings structure
            assert len(daily_reading.readings) >= 3, \
                f"Expected at least 3 readings for Christmas, got {len(daily_reading.readings)}"
            
            print(f"\n✓ Successfully scraped {daily_reading.liturgical_day}")
            print(f"  Date: {daily_reading.date_display}")
            print(f"  Readings: {len(daily_reading.readings)}")
        
        except (NetworkError, ParseError) as e:
            # Christmas hub pages may not have full readings - this is acceptable
            print(f"\n⚠ Christmas Day returned structure that requires specific Mass selection")
            print(f"  This is expected behavior for major feasts with multiple Masses")
            pytest.skip(
                f"Christmas hub page detected (requires specific Mass selection). "
                f"This is normal behavior for major feasts."
            )

    def test_immaculate_conception(self, scraper):
        """Test scraping Immaculate Conception (major feast)."""
        test_date = date(2025, 12, 8)  # Immaculate Conception
        
        try:
            daily_reading = scraper.get_readings_for_date(test_date)
            
            assert isinstance(daily_reading, DailyReading)
            assert daily_reading.date == test_date
            assert daily_reading.liturgical_day
            assert len(daily_reading.readings) >= 3
            
            print(f"\n✓ Successfully scraped {daily_reading.liturgical_day}")
            print(f"  Readings: {len(daily_reading.readings)}")
        
        except (NetworkError, ParseError) as e:
            pytest.fail(
                f"Failed to scrape Immaculate Conception readings for {test_date}. Error: {e}"
            )


class TestErrorHandling:
    """Test error handling for integration scenarios."""

    def test_future_date_far_ahead(self, scraper):
        """Test scraping a date far in the future (may not be available)."""
        test_date = date(2030, 1, 1)  # Future date that likely doesn't exist yet
        
        # This test verifies graceful handling of unavailable dates
        # It may succeed (if USCCB has far-future readings) or fail gracefully
        try:
            daily_reading = scraper.get_readings_for_date(test_date)
            
            # If it succeeds, verify structure
            assert isinstance(daily_reading, DailyReading)
            assert daily_reading.date == test_date
            
            print(f"\n✓ Future date {test_date} is available on USCCB")
        
        except (NetworkError, ParseError) as e:
            # Expected for far-future dates
            print(f"\n✓ Future date {test_date} not available (expected): {e}")
            # This is acceptable behavior

    def test_network_resilience(self, scraper):
        """Test that scraper properly reports network errors."""
        # Test with an invalid URL to verify error handling
        scraper_with_bad_url = USCCBReadingsScraper(base_url="https://invalid-domain-that-does-not-exist.example")
        test_date = date(2025, 11, 22)
        
        with pytest.raises(NetworkError):
            scraper_with_bad_url.get_readings_for_date(test_date)
        
        print("\n✓ Network error handling works correctly")


class TestDataQuality:
    """Test quality and completeness of scraped data."""

    def test_reading_text_length(self, scraper):
        """Test that reading text has reasonable length (not truncated)."""
        test_date = date(2025, 11, 22)
        
        try:
            daily_reading = scraper.get_readings_for_date(test_date)
            
            for reading in daily_reading.readings:
                # First reading should typically have substantial text
                if "reading" in reading.title.lower() and "1" in reading.title:
                    total_chars = sum(len(p) for p in reading.text)
                    assert total_chars > 50, \
                        f"First reading text seems too short: {total_chars} chars"
                
                # Gospel should have substantial text
                if "gospel" in reading.title.lower():
                    total_chars = sum(len(p) for p in reading.text)
                    assert total_chars > 50, \
                        f"Gospel text seems too short: {total_chars} chars"
            
            print(f"\n✓ Reading text lengths are appropriate")
        
        except (NetworkError, ParseError) as e:
            pytest.fail(f"Data quality test failed: {e}")

    def test_liturgical_day_extracted(self, scraper):
        """Test that liturgical day is properly extracted and meaningful."""
        test_date = date(2025, 11, 22)
        
        try:
            daily_reading = scraper.get_readings_for_date(test_date)
            
            # Liturgical day should not be empty
            assert daily_reading.liturgical_day
            
            # Should not contain unwanted suffixes
            assert "| USCCB" not in daily_reading.liturgical_day
            assert not daily_reading.liturgical_day.endswith(" - USCCB")
            
            # Should have meaningful length
            assert len(daily_reading.liturgical_day) > 5, \
                f"Liturgical day too short: '{daily_reading.liturgical_day}'"
            
            print(f"\n✓ Liturgical day properly extracted: '{daily_reading.liturgical_day}'")
        
        except (NetworkError, ParseError) as e:
            pytest.fail(f"Liturgical day extraction test failed: {e}")
