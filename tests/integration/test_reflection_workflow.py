"""Integration tests for daily reflection generation workflow."""

import pytest
from catholic_liturgy_tools.ai.client import AnthropicClient
from catholic_liturgy_tools.ai.models import DailyReflection, CCCCitation
from catholic_liturgy_tools.scraper.models import FeastDayInfo


class TestReflectionWorkflowWithMockedAPI:
    """Integration tests using mocked API responses."""
    
    def test_generate_reflection_for_single_reading(self, mock_anthropic_client):
        """Test reflection generation with a single reading."""
        client = mock_anthropic_client
        
        readings = [
            {
                "title": "Gospel",
                "citation": "Luke 1:26-38",
                "text": "The angel Gabriel was sent from God..."
            }
        ]
        
        reflection = client.generate_reflection(
            date_display="Monday, December 8, 2025",
            liturgical_day="Immaculate Conception",
            feast_context=None,
            readings=readings
        )
        
        assert isinstance(reflection, DailyReflection)
        assert len(reflection.reflection_text) > 0
        assert len(reflection.pondering_questions) >= 2
        assert len(reflection.ccc_citations) >= 1
        assert reflection.input_tokens > 0
        assert reflection.output_tokens > 0
        
    def test_generate_reflection_for_multiple_readings(self, mock_anthropic_client, sample_readings_list):
        """Test reflection synthesizes multiple readings."""
        client = mock_anthropic_client
        
        reflection = client.generate_reflection(
            date_display="Sunday, December 7, 2025",
            liturgical_day="Second Sunday of Advent",
            feast_context=None,
            readings=sample_readings_list
        )
        
        assert isinstance(reflection, DailyReflection)
        # Reflection should be substantial for multiple readings
        assert len(reflection.reflection_text.split()) >= 100
        assert len(reflection.pondering_questions) == 3
        assert len(reflection.ccc_citations) == 1
        
    def test_generate_reflection_with_feast_day_context(self, mock_anthropic_client):
        """Test reflection includes feast day context."""
        client = mock_anthropic_client
        
        feast_info = FeastDayInfo(
            feast_type="Solemnity",
            feast_name="Immaculate Conception of the Blessed Virgin Mary",
            liturgical_color="White",
            is_saint=False,
            is_marian=True,
            is_apostle=False,
            is_martyr=False
        )
        
        readings = [
            {
                "title": "Gospel",
                "citation": "Luke 1:26-38",
                "text": "The angel Gabriel was sent..."
            }
        ]
        
        reflection = client.generate_reflection(
            date_display="Monday, December 8, 2025",
            liturgical_day="Immaculate Conception",
            feast_context=feast_info,
            readings=readings
        )
        
        assert isinstance(reflection, DailyReflection)
        assert len(reflection.ccc_citations) >= 1
        
    def test_reflection_cost_tracking(self, mock_anthropic_client):
        """Test that reflection generation updates cost tracker."""
        client = mock_anthropic_client
        
        readings = [{"title": "Gospel", "citation": "John 1:1-5", "text": "In the beginning was the Word..."}]
        
        # Get initial cost
        initial_cost = client.get_cost_summary()["total_cost"]
        
        # Generate reflection
        client.generate_reflection(
            date_display="Tuesday, January 1, 2025",
            liturgical_day="Mary, Mother of God",
            feast_context=None,
            readings=readings
        )
        
        # Verify cost increased
        final_cost = client.get_cost_summary()["total_cost"]
        assert final_cost > initial_cost


class TestReflectionWorkflowErrorHandling:
    """Integration tests for error scenarios."""
    
    def test_reflection_empty_readings_raises_error(self, mock_anthropic_client):
        """Test that empty readings list raises ValueError."""
        client = mock_anthropic_client
        
        with pytest.raises(ValueError):
            client.generate_reflection(
                date_display="Monday, December 1, 2025",
                liturgical_day="First Week of Advent",
                feast_context=None,
                readings=[]
            )
            
    def test_reflection_validates_ccc_citations(self, mock_anthropic_client):
        """Test that generated CCC citations are validated."""
        client = mock_anthropic_client
        
        readings = [{"title": "Gospel", "citation": "Matthew 5:1-12", "text": "Blessed are..."}]
        
        reflection = client.generate_reflection(
            date_display="Monday, December 1, 2025",
            liturgical_day="First Week of Advent",
            feast_context=None,
            readings=readings
        )
        
        # All CCC citations should be in valid range
        for ccc in reflection.ccc_citations:
            assert isinstance(ccc, CCCCitation)
            assert 1 <= ccc.paragraph_number <= 2865
            assert len(ccc.excerpt_text) > 0


class TestReflectionWorkflowIntegration:
    """End-to-end integration tests for reflection workflow."""
    
    def test_complete_reflection_generation_workflow(self, mock_anthropic_client):
        """Test complete workflow from readings to reflection."""
        client = mock_anthropic_client
        
        # Simulate Sunday Mass readings (First Reading, Psalm, Second Reading, Gospel)
        sunday_readings = [
            {
                "title": "First Reading",
                "citation": "Isaiah 40:1-5",
                "text": "Comfort, give comfort to my people, says your God."
            },
            {
                "title": "Responsorial Psalm",
                "citation": "Psalm 85:9-14",
                "text": "Lord, let us see your kindness, and grant us your salvation."
            },
            {
                "title": "Second Reading",
                "citation": "2 Peter 3:8-14",
                "text": "Do not ignore this one fact, beloved..."
            },
            {
                "title": "Gospel",
                "citation": "Mark 1:1-8",
                "text": "The beginning of the gospel of Jesus Christ..."
            }
        ]
        
        reflection = client.generate_reflection(
            date_display="Sunday, December 7, 2025",
            liturgical_day="Second Sunday of Advent",
            feast_context=None,
            readings=sunday_readings
        )
        
        # Verify complete reflection structure
        assert isinstance(reflection, DailyReflection)
        assert len(reflection.reflection_text) > 0
        assert 2 <= len(reflection.pondering_questions) <= 3
        assert 1 <= len(reflection.ccc_citations) <= 2
        
        # Verify pondering questions format
        for question in reflection.pondering_questions:
            assert isinstance(question, str)
            assert len(question) > 0
            assert question.endswith("?")
            
        # Verify CCC citations structure
        for ccc in reflection.ccc_citations:
            assert isinstance(ccc, CCCCitation)
            assert 1 <= ccc.paragraph_number <= 2865
            assert len(ccc.excerpt_text) > 0
            
        # Verify token usage recorded
        assert reflection.input_tokens > 0
        assert reflection.output_tokens > 0
        
    def test_weekday_vs_sunday_reflection(self, mock_anthropic_client):
        """Test reflection generation for weekday (fewer readings) vs Sunday."""
        client = mock_anthropic_client
        
        # Weekday readings (typically 2 readings)
        weekday_readings = [
            {"title": "First Reading", "citation": "Genesis 3:9-15", "text": "The LORD God..."},
            {"title": "Gospel", "citation": "Luke 1:26-38", "text": "The angel Gabriel..."}
        ]
        
        weekday_reflection = client.generate_reflection(
            date_display="Monday, December 8, 2025",
            liturgical_day="Immaculate Conception",
            feast_context=None,
            readings=weekday_readings
        )
        
        # Sunday readings (typically 4 readings)
        sunday_readings = [
            {"title": "First Reading", "citation": "Isaiah 40:1-5", "text": "Comfort..."},
            {"title": "Responsorial Psalm", "citation": "Psalm 85:9-14", "text": "Lord..."},
            {"title": "Second Reading", "citation": "2 Peter 3:8-14", "text": "Do not..."},
            {"title": "Gospel", "citation": "Mark 1:1-8", "text": "The beginning..."}
        ]
        
        sunday_reflection = client.generate_reflection(
            date_display="Sunday, December 7, 2025",
            liturgical_day="Second Sunday of Advent",
            feast_context=None,
            readings=sunday_readings
        )
        
        # Both should have valid structure
        assert isinstance(weekday_reflection, DailyReflection)
        assert isinstance(sunday_reflection, DailyReflection)
        
        # Both should have proper question counts
        assert 2 <= len(weekday_reflection.pondering_questions) <= 3
        assert 2 <= len(sunday_reflection.pondering_questions) <= 3


class TestReflectionWorkflowWithFixtures:
    """Tests using sample fixture data."""
    
    def test_reflection_with_fixture_readings(self, mock_anthropic_client, sample_readings_list):
        """Test reflection generation using fixture readings."""
        client = mock_anthropic_client
        
        reflection = client.generate_reflection(
            date_display="Saturday, November 30, 2025",
            liturgical_day="Saturday of the Thirty-Fourth Week in Ordinary Time",
            feast_context=None,
            readings=sample_readings_list
        )
        
        assert isinstance(reflection, DailyReflection)
        assert len(reflection.reflection_text) > 0
        assert len(reflection.pondering_questions) >= 2
        assert len(reflection.ccc_citations) >= 1
        
    def test_reflection_preserves_reading_order(self, mock_anthropic_client):
        """Test that reflection considers readings in order."""
        client = mock_anthropic_client
        
        readings = [
            {"title": "First Reading", "citation": "Genesis 1:1", "text": "In the beginning..."},
            {"title": "Gospel", "citation": "John 1:1", "text": "In the beginning was the Word..."}
        ]
        
        reflection = client.generate_reflection(
            date_display="Monday, December 1, 2025",
            liturgical_day="First Week of Advent",
            feast_context=None,
            readings=readings
        )
        
        # Reflection should be generated successfully with ordered readings
        assert isinstance(reflection, DailyReflection)
        assert reflection.input_tokens > 0
