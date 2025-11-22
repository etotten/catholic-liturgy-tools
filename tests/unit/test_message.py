"""Unit tests for message generation module."""

import pytest
from datetime import date
from pathlib import Path
from catholic_liturgy_tools.generator.message import (
    generate_message_content,
    get_message_file_path,
    generate_message,
)


class TestGenerateMessageContent:
    """Tests for generate_message_content function."""
    
    def test_generates_markdown_with_yaml_frontmatter(self):
        """Test that generated content includes YAML frontmatter."""
        content = generate_message_content("2025-11-22")
        
        assert content.startswith("---")
        assert "layout: post" in content
        assert "---" in content.split("\n", 3)[3]  # Closing frontmatter
    
    def test_includes_date_in_frontmatter(self):
        """Test that date is included in YAML frontmatter."""
        test_date = "2025-11-22"
        content = generate_message_content(test_date)
        
        assert f"date: {test_date}" in content
    
    def test_includes_title_in_frontmatter(self):
        """Test that title is included in YAML frontmatter."""
        test_date = "2025-11-22"
        content = generate_message_content(test_date)
        
        assert f'title: "Daily Message for {test_date}"' in content
    
    def test_includes_date_heading_in_content(self):
        """Test that content includes date as heading."""
        test_date = "2025-11-22"
        content = generate_message_content(test_date)
        
        assert f"# {test_date}" in content
    
    def test_includes_greeting_in_content(self):
        """Test that content includes the greeting."""
        content = generate_message_content("2025-11-22")
        
        assert "Hello Catholic World" in content
    
    def test_different_dates_produce_different_content(self):
        """Test that different dates produce different content."""
        content1 = generate_message_content("2025-11-22")
        content2 = generate_message_content("2025-11-23")
        
        assert content1 != content2
        assert "2025-11-22" in content1
        assert "2025-11-23" in content2


class TestGetMessageFilePath:
    """Tests for get_message_file_path function."""
    
    def test_generates_correct_filename_format(self):
        """Test that filename follows YYYY-MM-DD-daily-message.md format."""
        test_date = "2025-11-22"
        filepath = get_message_file_path(test_date)
        
        assert filepath.name == "2025-11-22-daily-message.md"
    
    def test_default_output_directory_is_posts(self):
        """Test that default output directory is _posts."""
        filepath = get_message_file_path("2025-11-22")
        
        assert filepath.parent.name == "_posts"
    
    def test_custom_output_directory(self):
        """Test that custom output directory can be specified."""
        filepath = get_message_file_path("2025-11-22", output_dir="custom_dir")
        
        assert filepath.parent.name == "custom_dir"
    
    def test_returns_path_object(self):
        """Test that function returns a Path object."""
        filepath = get_message_file_path("2025-11-22")
        
        assert isinstance(filepath, Path)
    
    def test_different_dates_produce_different_paths(self):
        """Test that different dates produce different file paths."""
        path1 = get_message_file_path("2025-11-22")
        path2 = get_message_file_path("2025-11-23")
        
        assert path1 != path2


class TestGenerateMessage:
    """Tests for generate_message function (main entry point)."""
    
    def test_creates_message_file(self, temp_dir):
        """Test that function creates a message file."""
        output_dir = str(temp_dir / "_posts")
        
        result = generate_message(output_dir=output_dir)
        
        assert result.exists()
        assert result.is_file()
    
    def test_file_contains_valid_content(self, temp_dir):
        """Test that generated file contains valid content."""
        output_dir = str(temp_dir / "_posts")
        
        result = generate_message(output_dir=output_dir)
        content = result.read_text()
        
        assert content.startswith("---")
        assert "Hello Catholic World" in content
        assert "layout: post" in content
    
    def test_uses_todays_date(self, temp_dir):
        """Test that function uses today's date."""
        output_dir = str(temp_dir / "_posts")
        today = date.today().isoformat()
        
        result = generate_message(output_dir=output_dir)
        content = result.read_text()
        
        assert today in content
        assert today in result.name
    
    def test_creates_output_directory_if_missing(self, temp_dir):
        """Test that output directory is created if it doesn't exist."""
        output_dir = str(temp_dir / "new_posts")
        
        result = generate_message(output_dir=output_dir)
        
        assert Path(output_dir).exists()
        assert result.exists()
    
    def test_overwrites_existing_file(self, temp_dir):
        """Test that existing file is overwritten (idempotency)."""
        output_dir = str(temp_dir / "_posts")
        
        # Generate first time
        result1 = generate_message(output_dir=output_dir)
        original_content = result1.read_text()
        
        # Generate second time
        result2 = generate_message(output_dir=output_dir)
        new_content = result2.read_text()
        
        assert result1 == result2  # Same file path
        assert result2.exists()
        # Content should be identical for same day
        assert new_content == original_content
    
    def test_returns_path_object(self, temp_dir):
        """Test that function returns a Path object."""
        output_dir = str(temp_dir / "_posts")
        
        result = generate_message(output_dir=output_dir)
        
        assert isinstance(result, Path)
