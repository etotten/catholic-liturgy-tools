"""Unit tests for HTML utilities module."""

import pytest
from catholic_liturgy_tools.utils.html_utils import (
    sanitize_text,
    format_paragraph,
    format_paragraphs,
)


class TestSanitizeText:
    """Test suite for sanitize_text function."""
    
    def test_sanitize_angle_brackets(self):
        """Test that angle brackets are escaped."""
        result = sanitize_text("<script>alert('XSS')</script>")
        assert result == "&lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;"
        assert "<" not in result
        assert ">" not in result
    
    def test_sanitize_ampersand(self):
        """Test that ampersands are escaped."""
        result = sanitize_text("John 3:16 & Romans 8:28")
        assert result == "John 3:16 &amp; Romans 8:28"
        # Should not double-escape
        assert "&amp;amp;" not in result
    
    def test_sanitize_quotes(self):
        """Test that both single and double quotes are escaped."""
        result = sanitize_text('He said "Peace" and I replied \'Amen\'')
        assert result == "He said &quot;Peace&quot; and I replied &#x27;Amen&#x27;"
        assert '"' not in result
        assert "'" not in result
    
    def test_sanitize_all_special_chars(self):
        """Test with all special characters together."""
        result = sanitize_text("<tag attr=\"value\" & 'content'>")
        assert "&lt;" in result
        assert "&gt;" in result
        assert "&amp;" in result
        assert "&quot;" in result
        assert "&#x27;" in result
    
    def test_sanitize_normal_text(self):
        """Test that normal text without special characters passes through."""
        text = "King Antiochus was traversing the inland provinces."
        result = sanitize_text(text)
        assert result == text
    
    def test_sanitize_empty_string(self):
        """Test with empty string."""
        result = sanitize_text("")
        assert result == ""
    
    def test_sanitize_unicode_characters(self):
        """Test that Unicode characters are preserved."""
        text = "Café résumé naïve"
        result = sanitize_text(text)
        assert result == text
    
    def test_sanitize_numbers_and_symbols(self):
        """Test with numbers and non-HTML symbols."""
        text = "1 + 2 = 3, cost: $100, temperature: -5°C"
        result = sanitize_text(text)
        assert result == text


class TestFormatParagraph:
    """Test suite for format_paragraph function."""
    
    def test_format_with_leading_whitespace(self):
        """Test that leading whitespace is stripped."""
        result = format_paragraph("   King Antiochus was traversing.")
        assert result == "King Antiochus was traversing."
        assert not result.startswith(" ")
    
    def test_format_with_trailing_whitespace(self):
        """Test that trailing whitespace is stripped."""
        result = format_paragraph("King Antiochus was traversing.   ")
        assert result == "King Antiochus was traversing."
        assert not result.endswith(" ")
    
    def test_format_with_both_whitespace(self):
        """Test with both leading and trailing whitespace."""
        result = format_paragraph("   King Antiochus was traversing.   ")
        assert result == "King Antiochus was traversing."
    
    def test_format_empty_string(self):
        """Test with empty string."""
        result = format_paragraph("")
        assert result == ""
    
    def test_format_whitespace_only(self):
        """Test with whitespace-only string."""
        result = format_paragraph("   \n  \t  ")
        assert result == ""
    
    def test_format_line_breaks_replaced(self):
        """Test that line breaks are replaced with spaces."""
        result = format_paragraph("First line\nSecond line")
        assert result == "First line Second line"
        assert "\n" not in result
    
    def test_format_carriage_returns_replaced(self):
        """Test that carriage returns are replaced with spaces."""
        result = format_paragraph("First line\rSecond line")
        assert result == "First line Second line"
        assert "\r" not in result
    
    def test_format_mixed_line_breaks(self):
        """Test with mixed line break types."""
        result = format_paragraph("First\nSecond\r\nThird")
        assert "First Second  Third" in result or "First Second Third" in result
        assert "\n" not in result
        assert "\r" not in result
    
    def test_format_preserves_internal_spacing(self):
        """Test that internal spacing is preserved."""
        result = format_paragraph("Word  with  double  spaces")
        assert "double  spaces" in result
    
    def test_format_normal_paragraph(self):
        """Test with normal paragraph text."""
        text = "This is a normal paragraph with no extra whitespace."
        result = format_paragraph(text)
        assert result == text


class TestFormatParagraphs:
    """Test suite for format_paragraphs function."""
    
    def test_format_multiple_paragraphs(self):
        """Test formatting a list of paragraphs."""
        paragraphs = ["  First para  ", "  Second para  ", "  Third para  "]
        result = format_paragraphs(paragraphs)
        assert result == ["First para", "Second para", "Third para"]
    
    def test_format_with_empty_paragraphs(self):
        """Test that empty paragraphs are filtered out."""
        paragraphs = ["First para", "", "Second para", "   ", "Third para"]
        result = format_paragraphs(paragraphs)
        assert result == ["First para", "Second para", "Third para"]
        assert len(result) == 3
    
    def test_format_all_empty(self):
        """Test with all empty paragraphs."""
        paragraphs = ["", "   ", "\n", "  \t  "]
        result = format_paragraphs(paragraphs)
        assert result == []
    
    def test_format_empty_list(self):
        """Test with empty list."""
        result = format_paragraphs([])
        assert result == []
    
    def test_format_with_line_breaks(self):
        """Test that line breaks in paragraphs are handled."""
        paragraphs = ["First\nline", "Second\nline"]
        result = format_paragraphs(paragraphs)
        assert result == ["First line", "Second line"]
        assert all("\n" not in p for p in result)
    
    def test_format_preserves_order(self):
        """Test that paragraph order is preserved."""
        paragraphs = ["Third", "First", "Second"]
        result = format_paragraphs(paragraphs)
        assert result == ["Third", "First", "Second"]


class TestEdgeCases:
    """Test suite for edge cases and unusual inputs."""
    
    def test_sanitize_and_format_together(self):
        """Test using both functions together (common workflow)."""
        raw = "  <tag>Content with 'quotes'</tag>  \n"
        formatted = format_paragraph(raw)
        sanitized = sanitize_text(formatted)
        
        assert "&lt;" in sanitized
        assert "&gt;" in sanitized
        assert "&#x27;" in sanitized
        assert not sanitized.startswith(" ")
        assert not sanitized.endswith(" ")
    
    def test_very_long_text(self):
        """Test with very long text (performance check)."""
        long_text = "A" * 10000
        result = sanitize_text(long_text)
        assert len(result) == 10000
        assert result == long_text
    
    def test_special_characters_in_context(self):
        """Test special characters in realistic biblical text context."""
        text = 'Jesus said to them, "Render to Caesar what is Caesar\'s & to God what is God\'s."'
        sanitized = sanitize_text(text)
        
        # Should escape quotes and ampersand
        assert "&quot;" in sanitized
        assert "&#x27;" in sanitized
        assert "&amp;" in sanitized
        # But should not create actual HTML tags
        assert "<" not in sanitized or "&lt;" in sanitized
