"""Unit tests for AI client module (synopsis and reflection generation)."""

import pytest
from unittest.mock import MagicMock
from catholic_liturgy_tools.ai.client import AnthropicClient
from catholic_liturgy_tools.ai.models import ReadingSynopsis, DailyReflection, CCCCitation


class TestAnthropicClientSynopsis:
    """Tests for synopsis generation."""
    
    def test_generate_synopsis_success(self, mock_anthropic_client, sample_synopsis_response):
        """Test successful synopsis generation with valid API response."""
        client = mock_anthropic_client
        
        # Call generate_synopsis
        result = client.generate_synopsis(
            reading_title="First Reading",
            reading_text="In those days, the people of Israel...",
            citation="Genesis 1:1-5"
        )
        
        # Verify result structure
        assert isinstance(result, ReadingSynopsis)
        assert result.reading_title == "First Reading"
        assert len(result.synopsis_text.split()) >= 10  # At least 10 words
        assert len(result.synopsis_text.split()) <= 25  # At most 25 words
        assert result.tokens_used > 0
        
    def test_generate_synopsis_cost_tracking(self, mock_anthropic_client):
        """Test that synopsis generation is tracked in cost tracker."""
        client = mock_anthropic_client
        
        # Generate synopsis
        client.generate_synopsis(
            reading_title="Gospel",
            reading_text="Jesus said to his disciples...",
            citation="Matthew 5:1-12"
        )
        
        # Verify cost tracking
        cost_summary = client.get_cost_summary()
        assert cost_summary["total_cost"] > 0
        assert "synopsis" in [op["operation"] for op in cost_summary["calls"]]
        
    def test_generate_synopsis_empty_text_raises_error(self, mock_anthropic_client):
        """Test that empty reading text raises ValueError."""
        client = mock_anthropic_client
        
        with pytest.raises(ValueError, match="reading_text cannot be empty"):
            client.generate_synopsis(
                reading_title="First Reading",
                reading_text="",
                citation="Genesis 1:1"
            )
            
    def test_generate_synopsis_empty_citation_raises_error(self, mock_anthropic_client):
        """Test that empty citation raises ValueError."""
        client = mock_anthropic_client
        
        with pytest.raises(ValueError):
            client.generate_synopsis(
                reading_title="Gospel",
                reading_text="Jesus said...",
                citation=""  # Empty citation
            )


class TestAnthropicClientReflection:
    """Tests for daily reflection generation."""
    
    def test_generate_reflection_success(self, mock_anthropic_client, sample_reflection_response, sample_readings_list):
        """Test successful reflection generation with valid API response."""
        client = mock_anthropic_client
        
        # Call generate_reflection
        result = client.generate_reflection(
            date_display="Monday, December 1, 2025",
            liturgical_day="First Week of Advent",
            feast_context=None,
            readings=sample_readings_list
        )
        
        # Verify result structure
        assert isinstance(result, DailyReflection)
        assert len(result.reflection_text.split()) >= 300  # At least 300 words
        assert len(result.reflection_text.split()) <= 500  # At most 500 words
        assert len(result.pondering_questions) >= 2  # At least 2 questions
        assert len(result.pondering_questions) <= 3  # At most 3 questions
        assert len(result.ccc_citations) >= 1  # At least 1 CCC citation
        assert len(result.ccc_citations) <= 2  # At most 2 CCC citations
        assert result.input_tokens > 0
        assert result.output_tokens > 0
        
    def test_generate_reflection_with_feast_day(self, mock_anthropic_client, sample_readings_list):
        """Test reflection generation with feast day context."""
        client = mock_anthropic_client
        from catholic_liturgy_tools.scraper.models import FeastDayInfo
        
        feast_info = FeastDayInfo(
            feast_name="Immaculate Conception of the Blessed Virgin Mary",
            feast_type="Solemnity",
            liturgical_color="White",
            is_saint=False,
            is_marian=True,
            is_apostle=False,
            is_martyr=False
        )
        
        result = client.generate_reflection(
            date_display="Monday, December 8, 2025",
            liturgical_day="Immaculate Conception",
            feast_context=feast_info,
            readings=sample_readings_list
        )
        
        assert isinstance(result, DailyReflection)
        assert len(result.ccc_citations) >= 1
        
    def test_generate_reflection_cost_limit_enforcement(self, mocker):
        """Test that cost limit is enforced for reflection generation."""
        # Create client with very low cost limit
        client = AnthropicClient(api_key="test-key", max_cost_per_reflection=0.001)
        
        # Mock the API call to return a valid response
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text='{"reflection_text": "' + "word " * 400 + '", "pondering_questions": ["Q1?", "Q2?"], "ccc_citations": [{"paragraph_number": 1234, "excerpt_text": "Test", "context_note": "Note"}]}')]
        mock_response.usage.input_tokens = 10000  # High token count to exceed limit
        mock_response.usage.output_tokens = 10000
        
        mocker.patch.object(client.client.messages, 'create', return_value=mock_response)
        
        with pytest.raises(RuntimeError, match="Cost limit exceeded"):
            client.generate_reflection(
                date_display="Monday, December 1, 2025",
                liturgical_day="First Week of Advent",
                feast_context=None,
                readings=[{"title": "Gospel", "citation": "Matthew 1:1-2", "text": "Test reading"}]
            )
            
    def test_generate_reflection_retry_on_invalid_ccc(self, mock_anthropic_client):
        """Test that reflection generation retries on invalid CCC citations."""
        client = mock_anthropic_client
        
        # This test will verify retry logic when implemented
        # For now, we just check that valid CCC citations are returned
        result = client.generate_reflection(
            date_display="Monday, December 1, 2025",
            liturgical_day="First Week of Advent",
            feast_context=None,
            readings=[{"title": "Gospel", "citation": "Matthew 1:1-2", "text": "Test reading"}],
            max_retries=3
        )
        
        # All CCC citations should be valid (1-2865)
        for ccc in result.ccc_citations:
            assert isinstance(ccc, CCCCitation)
            assert 1 <= ccc.paragraph_number <= 2865


class TestAnthropicClientConfiguration:
    """Tests for client configuration and initialization."""
    
    def test_client_initialization_with_env_vars(self, mocker):
        """Test client initialization loads from .env file."""
        mocker.patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key-from-env'})
        
        client = AnthropicClient()
        
        # Should have loaded API key from environment
        assert client.client is not None
        
    def test_client_initialization_with_explicit_key(self):
        """Test client initialization with explicit API key."""
        client = AnthropicClient(api_key="explicit-test-key")
        
        assert client.client is not None
        
    def test_client_initialization_missing_key_raises_error(self, mocker):
        """Test that missing API key raises ValueError."""
        mocker.patch.dict('os.environ', {}, clear=True)
        
        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
            AnthropicClient()
            
    def test_client_uses_correct_model(self):
        """Test that client uses Claude 3.5 Sonnet model."""
        client = AnthropicClient(api_key="test-key")
        
        assert client.model == "claude-3-5-sonnet-20241022"
