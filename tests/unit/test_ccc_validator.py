"""Unit tests for CCC (Catechism of the Catholic Church) validator."""

import pytest
from catholic_liturgy_tools.liturgy.ccc_validator import (
    validate_ccc_paragraph,
    get_ccc_url,
    MIN_PARAGRAPH,
    MAX_PARAGRAPH
)


class TestValidateCCCParagraph:
    """Tests for CCC paragraph validation."""
    
    def test_validate_minimum_paragraph(self):
        """Test that paragraph 1 (minimum) is valid."""
        assert validate_ccc_paragraph(1) is True
        
    def test_validate_maximum_paragraph(self):
        """Test that paragraph 2865 (maximum) is valid."""
        assert validate_ccc_paragraph(2865) is True
        
    def test_validate_mid_range_paragraph(self):
        """Test that mid-range paragraphs are valid."""
        assert validate_ccc_paragraph(1000) is True
        assert validate_ccc_paragraph(1500) is True
        assert validate_ccc_paragraph(2558) is True  # Prayer paragraph
        
    def test_validate_zero_paragraph_invalid(self):
        """Test that paragraph 0 is invalid."""
        assert validate_ccc_paragraph(0) is False
        
    def test_validate_negative_paragraph_invalid(self):
        """Test that negative paragraph numbers are invalid."""
        assert validate_ccc_paragraph(-1) is False
        assert validate_ccc_paragraph(-100) is False
        
    def test_validate_above_maximum_invalid(self):
        """Test that paragraphs above 2865 are invalid."""
        assert validate_ccc_paragraph(2866) is False
        assert validate_ccc_paragraph(3000) is False
        assert validate_ccc_paragraph(10000) is False


class TestGetCCCUrl:
    """Tests for CCC URL generation."""
    
    def test_get_url_for_valid_paragraph(self):
        """Test URL generation for valid paragraph."""
        url = get_ccc_url(1)
        assert url.startswith("https://www.vatican.va/archive/ENG0015/")
        assert "_P" in url
        assert url.endswith(".HTM")
        
    def test_get_url_for_paragraph_2558(self):
        """Test URL generation for specific paragraph (prayer definition)."""
        url = get_ccc_url(2558)
        # Hex for 2558 is 9FE
        assert "https://www.vatican.va/archive/ENG0015/_P9FE.HTM" == url
        
    def test_get_url_for_maximum_paragraph(self):
        """Test URL generation for maximum paragraph."""
        url = get_ccc_url(2865)
        # Hex for 2865 is B31
        assert "https://www.vatican.va/archive/ENG0015/_PB31.HTM" == url
        
    def test_get_url_invalid_paragraph_raises_error(self):
        """Test that invalid paragraph raises ValueError."""
        with pytest.raises(ValueError, match="Invalid CCC paragraph number"):
            get_ccc_url(0)
            
        with pytest.raises(ValueError, match="Invalid CCC paragraph number"):
            get_ccc_url(2866)
            
        with pytest.raises(ValueError, match="Invalid CCC paragraph number"):
            get_ccc_url(-1)


class TestCCCConstants:
    """Tests for CCC module constants."""
    
    def test_min_paragraph_constant(self):
        """Test MIN_PARAGRAPH constant value."""
        assert MIN_PARAGRAPH == 1
        
    def test_max_paragraph_constant(self):
        """Test MAX_PARAGRAPH constant value."""
        assert MAX_PARAGRAPH == 2865


class TestCCCValidatorIntegration:
    """Integration tests for CCC validator."""
    
    def test_validate_common_citations(self):
        """Test validation of commonly cited CCC paragraphs."""
        # Prayer paragraphs
        assert validate_ccc_paragraph(2558) is True  # Definition of prayer
        assert validate_ccc_paragraph(2559) is True  # Prayer as gift
        
        # Ten Commandments
        assert validate_ccc_paragraph(2083) is True  # First Commandment
        
        # Sacraments
        assert validate_ccc_paragraph(1210) is True  # Sacraments introduction
        assert validate_ccc_paragraph(1213) is True  # Baptism
        
        # Eucharist
        assert validate_ccc_paragraph(1322) is True  # Eucharist summary
        
    def test_boundary_validation(self):
        """Test validation at boundaries."""
        # Just below minimum
        assert validate_ccc_paragraph(0) is False
        
        # Minimum
        assert validate_ccc_paragraph(1) is True
        
        # Maximum
        assert validate_ccc_paragraph(2865) is True
        
        # Just above maximum
        assert validate_ccc_paragraph(2866) is False
        
    def test_url_generation_for_common_citations(self):
        """Test URL generation for commonly cited paragraphs."""
        # Should not raise for valid paragraphs
        url_2558 = get_ccc_url(2558)
        assert isinstance(url_2558, str)
        assert len(url_2558) > 0
        
        url_1 = get_ccc_url(1)
        assert isinstance(url_1, str)
        assert len(url_1) > 0
