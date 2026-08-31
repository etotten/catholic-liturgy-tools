"""Unit tests for AI prompt templates."""

import pytest
from catholic_liturgy_tools.ai.prompts import (
    build_synopsis_user_prompt,
    build_reflection_user_prompt,
    format_readings_list,
    SYNOPSIS_SYSTEM_PROMPT,
    REFLECTION_SYSTEM_PROMPT
)


class TestSynopsisPrompts:
    """Tests for synopsis generation prompts."""
    
    def test_synopsis_system_prompt_structure(self):
        """Test that synopsis system prompt follows contract requirements."""
        assert isinstance(SYNOPSIS_SYSTEM_PROMPT, str)
        assert len(SYNOPSIS_SYSTEM_PROMPT) > 50  # Should have meaningful instructions
        assert "10-25 words" in SYNOPSIS_SYSTEM_PROMPT or "10 to 25" in SYNOPSIS_SYSTEM_PROMPT
        assert "Catholic" in SYNOPSIS_SYSTEM_PROMPT or "Church" in SYNOPSIS_SYSTEM_PROMPT
        
    def test_build_synopsis_user_prompt_valid_input(self):
        """Test synopsis user prompt generation with valid inputs."""
        prompt = build_synopsis_user_prompt(
            reading_title="First Reading",
            reading_text="In the beginning, God created the heavens and the earth...",
            citation="Genesis 1:1-5"
        )
        
        assert isinstance(prompt, str)
        assert "First Reading" in prompt
        assert "Genesis 1:1-5" in prompt
        assert "In the beginning" in prompt
        
    def test_build_synopsis_user_prompt_includes_citation(self):
        """Test that user prompt includes Scripture citation."""
        prompt = build_synopsis_user_prompt(
            reading_title="Gospel",
            reading_text="Jesus said to his disciples...",
            citation="Matthew 5:1-12"
        )
        
        assert "Matthew 5:1-12" in prompt
        
    def test_build_synopsis_user_prompt_empty_text_raises_error(self):
        """Test that empty reading text raises ValueError."""
        with pytest.raises(ValueError):
            build_synopsis_user_prompt(
                reading_title="First Reading",
                reading_text="",
                citation="Genesis 1:1"
            )
            
    def test_build_synopsis_user_prompt_empty_citation_raises_error(self):
        """Test that empty citation raises ValueError."""
        with pytest.raises(ValueError):
            build_synopsis_user_prompt(
                reading_title="Gospel",
                reading_text="Jesus said...",
                citation=""
            )


class TestReflectionPrompts:
    """Tests for daily reflection generation prompts."""
    
    def test_reflection_system_prompt_structure(self):
        """Test that reflection system prompt follows contract requirements."""
        assert isinstance(REFLECTION_SYSTEM_PROMPT, str)
        assert len(REFLECTION_SYSTEM_PROMPT) > 100  # Should have detailed instructions
        assert "300-500 words" in REFLECTION_SYSTEM_PROMPT or "300 to 500" in REFLECTION_SYSTEM_PROMPT
        assert "CCC" in REFLECTION_SYSTEM_PROMPT or "Catechism" in REFLECTION_SYSTEM_PROMPT
        assert "questions" in REFLECTION_SYSTEM_PROMPT.lower()
        
    def test_reflection_system_prompt_mentions_ccc_range(self):
        """Test that system prompt specifies valid CCC paragraph range."""
        assert "1-2865" in REFLECTION_SYSTEM_PROMPT or "1 to 2865" in REFLECTION_SYSTEM_PROMPT or "2865" in REFLECTION_SYSTEM_PROMPT
        
    def test_build_reflection_user_prompt_valid_input(self):
        """Test reflection user prompt generation with valid inputs."""
        readings = [
            {"title": "First Reading", "citation": "Genesis 1:1-5", "text": "In the beginning..."},
            {"title": "Gospel", "citation": "Matthew 5:1-12", "text": "Jesus said..."}
        ]
        
        prompt = build_reflection_user_prompt(
            date_display="Monday, December 1, 2025",
            liturgical_day="First Week of Advent",
            feast_context=None,
            readings=readings
        )
        
        assert isinstance(prompt, str)
        assert "Monday, December 1, 2025" in prompt
        assert "First Week of Advent" in prompt
        assert "Genesis 1:1-5" in prompt
        assert "Matthew 5:1-12" in prompt
        
    def test_build_reflection_user_prompt_with_feast_day(self):
        """Test reflection prompt includes feast day context."""
        from catholic_liturgy_tools.scraper.models import FeastDayInfo
        
        feast_info = FeastDayInfo(
            feast_type="solemnity",
            feast_name="Immaculate Conception of the Blessed Virgin Mary",
            liturgical_color="white",
            is_saint=False,
            is_marian=True,
            is_apostle=False,
            is_martyr=False
        )
        
        readings = [
            {"title": "Gospel", "citation": "Luke 1:26-38", "text": "The angel Gabriel..."}
        ]
        
        prompt = build_reflection_user_prompt(
            date_display="Monday, December 8, 2025",
            liturgical_day="Immaculate Conception",
            feast_context=feast_info,
            readings=readings
        )
        
        assert "Immaculate Conception" in prompt
        assert "solemnity" in prompt.lower()
        
    def test_build_reflection_user_prompt_empty_readings_raises_error(self):
        """Test that empty readings list raises ValueError."""
        with pytest.raises(ValueError):
            build_reflection_user_prompt(
                date_display="Monday, December 1, 2025",
                liturgical_day="First Week of Advent",
                feast_context=None,
                readings=[]
            )
            
    def test_build_reflection_user_prompt_invalid_reading_format_does_not_raise(self):
        """Test that readings without required keys don't raise errors (graceful handling)."""
        # This should not raise because format_readings_list uses get() with defaults
        try:
            prompt = build_reflection_user_prompt(
                date_display="Monday, December 1, 2025",
                liturgical_day="First Week of Advent",
                feast_context=None,
                readings=[{"title": "Gospel"}]  # Missing 'citation' and 'text'
            )
            # Should succeed and produce a prompt
            assert isinstance(prompt, str)
            assert "Gospel" in prompt
        except Exception:
            pytest.fail("Should not raise exception for readings with missing keys")


class TestHelperFunctions:
    """Tests for prompt helper functions."""
    
    def test_format_readings_list_basic(self):
        """Test formatting of readings list for prompt."""
        readings = [
            {"title": "First Reading", "citation": "Genesis 1:1-5", "text": "In the beginning..."},
            {"title": "Gospel", "citation": "Matthew 5:1-12", "text": "Jesus said..."}
        ]
        
        formatted = format_readings_list(readings)
        
        assert isinstance(formatted, str)
        assert "First Reading" in formatted
        assert "Genesis 1:1-5" in formatted
        assert "Gospel" in formatted
        assert "Matthew 5:1-12" in formatted
        
    def test_format_readings_list_preserves_order(self):
        """Test that readings are formatted in the correct order."""
        readings = [
            {"title": "First Reading", "citation": "Gen 1:1", "text": "Text 1"},
            {"title": "Psalm", "citation": "Ps 23", "text": "Text 2"},
            {"title": "Second Reading", "citation": "Rom 1:1", "text": "Text 3"},
            {"title": "Gospel", "citation": "Matt 1:1", "text": "Text 4"}
        ]
        
        formatted = format_readings_list(readings)
        
        # Check order by finding indices
        first_idx = formatted.find("First Reading")
        psalm_idx = formatted.find("Psalm")
        second_idx = formatted.find("Second Reading")
        gospel_idx = formatted.find("Gospel")
        
        assert first_idx < psalm_idx < second_idx < gospel_idx
        
    def test_format_readings_list_empty_raises_error(self):
        """Test that empty readings list raises ValueError."""
        with pytest.raises(ValueError):
            format_readings_list([])
            
    def test_format_readings_list_handles_responsorial_psalm(self):
        """Test that Responsorial Psalm is formatted correctly."""
        readings = [
            {"title": "Responsorial Psalm", "citation": "Psalm 23:1-6", "text": "The Lord is my shepherd..."}
        ]
        
        formatted = format_readings_list(readings)
        
        assert "Responsorial Psalm" in formatted
        assert "Psalm 23:1-6" in formatted
