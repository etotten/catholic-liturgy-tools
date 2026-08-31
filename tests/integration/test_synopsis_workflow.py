"""Integration tests for synopsis generation workflow.

These tests verify the end-to-end flow of generating synopses for Scripture readings,
including API interaction, cost tracking, and error handling.
"""

import pytest
from datetime import date
from catholic_liturgy_tools.ai.client import AnthropicClient
from catholic_liturgy_tools.ai.models import ReadingSynopsis
from catholic_liturgy_tools.scraper.models import ReadingEntry


class TestSynopsisWorkflowWithMockedAPI:
    """Integration tests using mocked Anthropic API."""
    
    def test_synopsis_generation_for_single_reading(self, mock_anthropic_client):
        """Test generating synopsis for a single Scripture reading."""
        client = mock_anthropic_client
        
        reading = ReadingEntry(
            title="First Reading",
            citation="Genesis 1:1-5",
            text="In the beginning, God created the heavens and the earth. The earth was without form and void..."
        )
        
        # Generate synopsis
        synopsis = client.generate_synopsis(
            reading_title=reading.title,
            reading_text=reading.text,
            citation=reading.citation
        )
        
        # Verify synopsis structure
        assert isinstance(synopsis, ReadingSynopsis)
        assert synopsis.reading_title == reading.title
        assert 10 <= len(synopsis.synopsis_text.split()) <= 25
        assert synopsis.tokens_used > 0
        
    def test_synopsis_generation_for_multiple_readings(self, mock_anthropic_client):
        """Test generating synopses for multiple Scripture readings."""
        client = mock_anthropic_client
        
        readings = [
            ReadingEntry(
                title="First Reading",
                citation="Isaiah 40:1-5",
                text="Comfort, give comfort to my people, says your God..."
            ),
            ReadingEntry(
                title="Responsorial Psalm",
                citation="Psalm 85:9-14",
                text="I will hear what God proclaims; the LORD—for he proclaims peace..."
            ),
            ReadingEntry(
                title="Gospel",
                citation="Mark 1:1-8",
                text="The beginning of the gospel of Jesus Christ the Son of God..."
            )
        ]
        
        synopses = []
        for reading in readings:
            synopsis = client.generate_synopsis(
                reading_title=reading.title,
                reading_text=reading.text,
                citation=reading.citation
            )
            synopses.append(synopsis)
        
        # Verify all synopses generated
        assert len(synopses) == 3
        assert all(isinstance(s, ReadingSynopsis) for s in synopses)
        assert all(s.tokens_used > 0 for s in synopses)
        
    def test_synopsis_workflow_tracks_cumulative_cost(self, mock_anthropic_client):
        """Test that generating multiple synopses tracks cumulative cost."""
        client = mock_anthropic_client
        
        readings = [
            ("First Reading", "Isaiah 40:1-5", "Comfort, give comfort..."),
            ("Gospel", "Mark 1:1-8", "The beginning of the gospel...")
        ]
        
        for title, citation, text in readings:
            client.generate_synopsis(
                reading_title=title,
                reading_text=text,
                citation=citation
            )
        
        # Verify cost tracking
        summary = client.get_cost_summary()
        assert summary["total_cost"] > 0
        assert len(summary["calls"]) == 2
        assert all(call["operation"] == "synopsis" for call in summary["calls"])


class TestSynopsisWorkflowErrorHandling:
    """Integration tests for error handling scenarios."""
    
    def test_synopsis_generation_with_invalid_reading_text(self, mock_anthropic_client):
        """Test that invalid reading text is handled gracefully."""
        client = mock_anthropic_client
        
        with pytest.raises(ValueError):
            client.generate_synopsis(
                reading_title="First Reading",
                reading_text="",  # Empty text
                citation="Genesis 1:1"
            )
            
    def test_synopsis_generation_with_missing_citation(self, mock_anthropic_client):
        """Test that missing citation is handled gracefully."""
        client = mock_anthropic_client
        
        with pytest.raises(ValueError):
            client.generate_synopsis(
                reading_title="Gospel",
                reading_text="Jesus said to his disciples...",
                citation=""  # Empty citation
            )
            
    def test_synopsis_generation_respects_cost_limit(self, mocker):
        """Test that synopsis generation respects cost limits."""
        # Create client with very low cost limit
        client = AnthropicClient(api_key="test-key", max_cost_per_reflection=0.001)
        
        # Mock API response with high token usage
        mock_response = mocker.MagicMock()
        mock_response.content = [mocker.MagicMock(text="God creates the heavens and earth in the beginning.")]
        mock_response.usage.input_tokens = 5000
        mock_response.usage.output_tokens = 5000  # High cost
        
        mocker.patch.object(client.client.messages, 'create', return_value=mock_response)
        
        with pytest.raises(RuntimeError, match="Cost limit exceeded"):
            client.generate_synopsis(
                reading_title="First Reading",
                reading_text="In the beginning, God created...",
                citation="Genesis 1:1-5"
            )


class TestSynopsisWorkflowIntegration:
    """Integration tests simulating real-world synopsis generation workflows."""
    
    def test_sunday_mass_synopsis_generation(self, mock_anthropic_client):
        """Test generating synopses for a complete Sunday Mass (4 readings)."""
        client = mock_anthropic_client
        
        sunday_readings = [
            ReadingEntry(
                title="First Reading",
                citation="Isaiah 40:1-5, 9-11",
                text="Comfort, give comfort to my people, says your God. Speak tenderly to Jerusalem..."
            ),
            ReadingEntry(
                title="Responsorial Psalm",
                citation="Psalm 85:9-10, 11-12, 13-14",
                text="I will hear what God proclaims; the LORD—for he proclaims peace to his people..."
            ),
            ReadingEntry(
                title="Second Reading",
                citation="2 Peter 3:8-14",
                text="Do not ignore this one fact, beloved, that with the Lord one day is like a thousand years..."
            ),
            ReadingEntry(
                title="Gospel",
                citation="Mark 1:1-8",
                text="The beginning of the gospel of Jesus Christ the Son of God. As it is written in Isaiah the prophet..."
            )
        ]
        
        synopses = []
        for reading in sunday_readings:
            synopsis = client.generate_synopsis(
                reading_title=reading.title,
                reading_text=reading.text,
                citation=reading.citation
            )
            synopses.append(synopsis)
        
        # Verify all synopses generated successfully
        assert len(synopses) == 4
        
        # Verify cost is within reasonable bounds for 4 synopses
        cost_summary = client.get_cost_summary()
        assert cost_summary["total_cost"] < 0.04  # Should be under daily limit
        
    def test_weekday_mass_synopsis_generation(self, mock_anthropic_client):
        """Test generating synopses for a weekday Mass (2-3 readings)."""
        client = mock_anthropic_client
        
        weekday_readings = [
            ReadingEntry(
                title="First Reading",
                citation="Daniel 7:15-27",
                text="I, Daniel, found my spirit anguished within its covering of flesh..."
            ),
            ReadingEntry(
                title="Responsorial Psalm",
                citation="Daniel 3:82-87",
                text="You sons of men, bless the Lord; praise and exalt him above all forever..."
            ),
            ReadingEntry(
                title="Gospel",
                citation="Luke 21:34-36",
                text="Jesus said to his disciples: Beware that your hearts do not become drowsy..."
            )
        ]
        
        synopses = []
        for reading in weekday_readings:
            synopsis = client.generate_synopsis(
                reading_title=reading.title,
                reading_text=reading.text,
                citation=reading.citation
            )
            synopses.append(synopsis)
        
        assert len(synopses) == 3
        
        # Verify cost tracking
        cost_summary = client.get_cost_summary()
        assert len(cost_summary["calls"]) == 3
        
    def test_synopsis_generation_preserves_reading_order(self, mock_anthropic_client):
        """Test that synopsis generation preserves the order of readings."""
        client = mock_anthropic_client
        
        readings = [
            ("First Reading", "Genesis 1:1", "In the beginning..."),
            ("Psalm", "Psalm 23:1", "The Lord is my shepherd..."),
            ("Gospel", "Matthew 5:1", "Blessed are the poor in spirit...")
        ]
        
        synopses = []
        for title, citation, text in readings:
            synopsis = client.generate_synopsis(
                reading_title=title,
                reading_text=text,
                citation=citation
            )
            synopses.append(synopsis)
        
        # Verify order preserved
        assert synopses[0].reading_title == "First Reading"
        assert synopses[1].reading_title == "Psalm"
        assert synopses[2].reading_title == "Gospel"


class TestSynopsisWorkflowWithFixtures:
    """Integration tests using fixture data."""
    
    def test_synopsis_generation_with_sample_readings(self, mock_anthropic_client, sample_readings_data):
        """Test synopsis generation using sample readings from fixtures."""
        client = mock_anthropic_client
        
        # Get first reading set from fixtures
        reading_data = sample_readings_data["readings"][0]
        
        synopses = []
        for reading_entry in reading_data["readings"]:
            synopsis = client.generate_synopsis(
                reading_title=reading_entry["title"],
                reading_text=reading_entry["text"],
                citation=reading_entry["citation"]
            )
            synopses.append(synopsis)
        
        # Verify synopses generated from fixture data
        assert len(synopses) == len(reading_data["readings"])
        assert all(isinstance(s, ReadingSynopsis) for s in synopses)
