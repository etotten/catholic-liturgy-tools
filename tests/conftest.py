"""Pytest configuration and shared fixtures."""

import json
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import MagicMock


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests that is cleaned up after use."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def posts_dir(temp_dir):
    """Create a _posts directory within the temp directory."""
    posts_path = temp_dir / "_posts"
    posts_path.mkdir(parents=True, exist_ok=True)
    return posts_path


@pytest.fixture
def sample_message_files(posts_dir):
    """Create sample message files for testing."""
    dates = ["2025-11-20", "2025-11-21", "2025-11-22"]
    files = []
    
    for date in dates:
        filename = f"{date}-daily-message.md"
        filepath = posts_dir / filename
        content = f"""---
layout: post
title: "Daily Message for {date}"
date: {date}
---

# {date}

Hello Catholic World
"""
        filepath.write_text(content, encoding="utf-8")
        files.append(filepath)
    
    return files


# AI Module Fixtures (Feature 005)

@pytest.fixture
def mock_anthropic_response():
    """Mock Anthropic API response for testing."""
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text='{"synopsis": "God offers comfort and forgiveness to His people through Christ."}')]
    mock_response.usage = MagicMock(input_tokens=100, output_tokens=20)
    return mock_response


@pytest.fixture
def mock_anthropic_client(mocker):
    """Mock AnthropicClient for testing without API calls."""
    from catholic_liturgy_tools.ai.client import AnthropicClient
    
    # Mock the underlying Anthropic API client
    mock_api_client = mocker.patch('catholic_liturgy_tools.ai.client.Anthropic')
    mock_instance = mock_api_client.return_value
    
    # Create a side effect function that returns different responses based on system prompt
    def mock_create(**kwargs):
        mock_response = MagicMock()
        system_prompt = kwargs.get('system', '')
        
        if 'spiritual director' in system_prompt.lower():
            # Return reflection response
            reflection_json = json.dumps({
                "reflection_text": "<p>" + "Today's readings invite us to consider God's mercy and providence. " * 40 + "</p>",
                "pondering_questions": [
                    "How does God's call challenge me today?",
                    "Where do I need to trust more in God's providence?",
                    "What does it mean to speak tenderly to others?"
                ],
                "ccc_citations": [
                    {
                        "paragraph_number": 2558,
                        "excerpt_text": "Prayer is the raising of one's mind and heart to God.",
                        "context_note": "This connects to today's Gospel call to prayer."
                    }
                ]
            })
            mock_response.content = [MagicMock(text=reflection_json)]
            mock_response.usage = MagicMock(input_tokens=500, output_tokens=400)
        else:
            # Return synopsis response
            mock_response.content = [MagicMock(text='{"synopsis": "God offers comfort and forgiveness to His people through Christ."}')]
            mock_response.usage = MagicMock(input_tokens=100, output_tokens=20)
        
        return mock_response
    
    mock_instance.messages.create.side_effect = mock_create
    
    # Create real AnthropicClient with mocked API
    client = AnthropicClient(api_key="test-api-key")
    return client


@pytest.fixture
def sample_synopsis_response():
    """Sample synopsis response data for testing."""
    return {
        "synopsis": "God offers comfort and forgiveness to His people."
    }


@pytest.fixture
def sample_reflection_response():
    """Sample reflection response data for testing."""
    return {
        "reflection_text": "<p>Today's readings invite us to consider God's mercy...</p>",
        "pondering_questions": [
            "How does God's call challenge me today?",
            "Where do I need to trust more in God's providence?",
            "What does it mean to speak tenderly to others?"
        ],
        "ccc_citations": [
            {
                "paragraph_number": 2558,
                "excerpt_text": "Prayer is the raising of one's mind and heart to God.",
                "context_note": "This connects to today's Gospel call to prayer."
            }
        ]
    }


@pytest.fixture
def sample_reading_entry():
    """Sample reading entry for testing."""
    return {
        "title": "First Reading",
        "citation": "Isaiah 40:1-5",
        "text": "Comfort, give comfort to my people, says your God."
    }


@pytest.fixture
def sample_readings_list():
    """Sample list of readings for testing."""
    return [
        {
            "title": "First Reading",
            "citation": "Isaiah 40:1-5",
            "text": "Comfort, give comfort to my people, says your God."
        },
        {
            "title": "Responsorial Psalm",
            "citation": "Psalm 23:1-3",
            "text": "The LORD is my shepherd; I shall not want."
        },
        {
            "title": "Gospel",
            "citation": "Luke 21:5-11",
            "text": "While some people were speaking about the temple..."
        }
    ]


@pytest.fixture
def fixtures_dir():
    """Get the fixtures directory path."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_prayers_data(fixtures_dir):
    """Load sample prayers from fixtures."""
    prayers_file = fixtures_dir / "sample_prayers.json"
    if prayers_file.exists():
        with open(prayers_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"version": "1.0.0", "prayers": []}


@pytest.fixture
def sample_readings_data(fixtures_dir):
    """Load sample readings from fixtures."""
    readings_file = fixtures_dir / "sample_readings.json"
    if readings_file.exists():
        with open(readings_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"readings": []}
