"""Pytest configuration and shared fixtures."""

import pytest
import tempfile
import shutil
from pathlib import Path


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
