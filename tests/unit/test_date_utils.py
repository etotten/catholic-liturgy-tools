"""Unit tests for date_utils module."""

import pytest
from datetime import date
from catholic_liturgy_tools.utils.date_utils import get_today


class TestGetToday:
    """Tests for get_today function."""
    
    def test_get_today_returns_string(self):
        """Test that get_today returns a string."""
        result = get_today()
        assert isinstance(result, str)
    
    def test_get_today_format(self):
        """Test that get_today returns date in YYYY-MM-DD format."""
        result = get_today()
        # Should match YYYY-MM-DD format
        assert len(result) == 10
        assert result[4] == "-"
        assert result[7] == "-"
        
        # Should be parseable as a date
        year, month, day = result.split("-")
        assert year.isdigit() and len(year) == 4
        assert month.isdigit() and len(month) == 2
        assert day.isdigit() and len(day) == 2
    
    def test_get_today_matches_date_today(self):
        """Test that get_today returns today's actual date."""
        result = get_today()
        expected = date.today().isoformat()
        assert result == expected
    
    def test_get_today_is_valid_date(self):
        """Test that get_today returns a valid date that can be parsed."""
        result = get_today()
        # Should not raise an exception
        parsed_date = date.fromisoformat(result)
        assert isinstance(parsed_date, date)
