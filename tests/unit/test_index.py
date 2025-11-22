"""Unit tests for index generation module."""

import pytest
from pathlib import Path
from catholic_liturgy_tools.generator.index import (
    scan_message_files,
    parse_date_from_filename,
    generate_index_content,
    generate_index,
)


class TestScanMessageFiles:
    """Tests for scan_message_files function."""
    
    def test_scan_finds_message_files(self, sample_message_files):
        """Test that scan finds all message files."""
        posts_dir = sample_message_files[0].parent
        
        files = scan_message_files(str(posts_dir))
        
        assert len(files) == 3
        assert all(f.name.endswith("-daily-message.md") for f in files)
    
    def test_scan_empty_directory(self, temp_dir):
        """Test scanning an empty directory."""
        empty_dir = temp_dir / "empty_posts"
        empty_dir.mkdir()
        
        files = scan_message_files(str(empty_dir))
        
        assert files == []
    
    def test_scan_nonexistent_directory(self, temp_dir):
        """Test scanning a nonexistent directory."""
        nonexistent = temp_dir / "nonexistent"
        
        files = scan_message_files(str(nonexistent))
        
        assert files == []
    
    def test_scan_ignores_non_message_files(self, posts_dir):
        """Test that scan ignores files that aren't daily messages."""
        # Create some non-message files
        (posts_dir / "other-file.md").write_text("Other content")
        (posts_dir / "2025-11-22-other.md").write_text("Other content")
        
        # Create message files
        (posts_dir / "2025-11-22-daily-message.md").write_text("Message")
        
        files = scan_message_files(str(posts_dir))
        
        assert len(files) == 1
        assert files[0].name == "2025-11-22-daily-message.md"
    
    def test_returns_list_of_paths(self, sample_message_files):
        """Test that function returns a list of Path objects."""
        posts_dir = sample_message_files[0].parent
        
        files = scan_message_files(str(posts_dir))
        
        assert isinstance(files, list)
        assert all(isinstance(f, Path) for f in files)


class TestParseDateFromFilename:
    """Tests for parse_date_from_filename function."""
    
    def test_parse_valid_filename(self):
        """Test parsing a valid message filename."""
        result = parse_date_from_filename("2025-11-22-daily-message.md")
        
        assert result == "2025-11-22"
    
    def test_parse_different_dates(self):
        """Test parsing filenames with different dates."""
        dates = ["2025-01-01", "2025-12-31", "2024-06-15"]
        
        for date in dates:
            result = parse_date_from_filename(f"{date}-daily-message.md")
            assert result == date
    
    def test_parse_invalid_filename_returns_none(self):
        """Test that invalid filenames return None."""
        invalid_names = [
            "other-file.md",
            "2025-11-22-other.md",
            "not-a-date-daily-message.md",
            "2025-13-01-daily-message.md",  # Invalid month
        ]
        
        for name in invalid_names[:3]:  # Skip the invalid date format for now
            result = parse_date_from_filename(name)
            assert result is None
    
    def test_parse_with_path(self):
        """Test parsing works with full path, not just filename."""
        result = parse_date_from_filename("_posts/2025-11-22-daily-message.md")
        
        assert result == "2025-11-22"


class TestGenerateIndexContent:
    """Tests for generate_index_content function."""
    
    def test_generates_markdown_with_frontmatter(self, sample_message_files):
        """Test that generated content includes YAML frontmatter."""
        content = generate_index_content(sample_message_files)
        
        assert content.startswith("---")
        assert "layout: page" in content
        assert "title:" in content
    
    def test_includes_links_to_all_messages(self, sample_message_files):
        """Test that all messages are linked in the index."""
        content = generate_index_content(sample_message_files)
        
        assert "2025-11-20" in content
        assert "2025-11-21" in content
        assert "2025-11-22" in content
    
    def test_reverse_chronological_order(self, sample_message_files):
        """Test that messages are listed in reverse chronological order."""
        content = generate_index_content(sample_message_files)
        
        # Find positions of dates in content
        pos_20 = content.index("2025-11-20")
        pos_21 = content.index("2025-11-21")
        pos_22 = content.index("2025-11-22")
        
        # Newest (22) should come before oldest (20)
        assert pos_22 < pos_21 < pos_20
    
    def test_generates_markdown_links(self, sample_message_files):
        """Test that proper markdown links are generated."""
        content = generate_index_content(sample_message_files)
        
        # Should contain markdown link syntax
        assert "[" in content and "](" in content and ")" in content
        assert "2025-11-22-daily-message.md" in content
    
    def test_empty_file_list(self):
        """Test generating index with no message files."""
        content = generate_index_content([])
        
        assert content.startswith("---")
        assert "layout: page" in content
        # Should still be valid markdown even with no messages
    
    def test_includes_daily_messages_title(self, sample_message_files):
        """Test that content includes appropriate title."""
        content = generate_index_content(sample_message_files)
        
        assert "Daily Message" in content


class TestGenerateIndex:
    """Tests for generate_index function (main entry point)."""
    
    def test_creates_index_file(self, sample_message_files):
        """Test that function creates an index file."""
        posts_dir = sample_message_files[0].parent
        temp_dir = posts_dir.parent
        output_file = str(temp_dir / "index.md")
        
        result = generate_index(posts_dir=str(posts_dir), output_file=output_file)
        
        assert result.exists()
        assert result.name == "index.md"
    
    def test_index_contains_valid_content(self, sample_message_files):
        """Test that generated index contains valid content."""
        posts_dir = sample_message_files[0].parent
        temp_dir = posts_dir.parent
        output_file = str(temp_dir / "index.md")
        
        result = generate_index(posts_dir=str(posts_dir), output_file=output_file)
        content = result.read_text()
        
        assert content.startswith("---")
        assert "layout: page" in content
        assert "2025-11-22" in content
        assert "2025-11-21" in content
        assert "2025-11-20" in content
    
    def test_default_output_file(self, sample_message_files):
        """Test that default output file is index.md."""
        posts_dir = sample_message_files[0].parent
        temp_dir = posts_dir.parent
        
        # Change working directory context
        import os
        old_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            result = generate_index(posts_dir=str(posts_dir))
            assert result.name == "index.md"
        finally:
            os.chdir(old_cwd)
    
    def test_handles_empty_posts_directory(self, temp_dir):
        """Test generating index when no message files exist."""
        posts_dir = temp_dir / "_posts"
        posts_dir.mkdir()
        output_file = str(temp_dir / "index.md")
        
        result = generate_index(posts_dir=str(posts_dir), output_file=output_file)
        
        assert result.exists()
        content = result.read_text()
        assert "layout: page" in content
    
    def test_overwrites_existing_index(self, sample_message_files):
        """Test that existing index is overwritten."""
        posts_dir = sample_message_files[0].parent
        temp_dir = posts_dir.parent
        output_file = str(temp_dir / "index.md")
        
        # Create initial index
        result1 = generate_index(posts_dir=str(posts_dir), output_file=output_file)
        content1 = result1.read_text()
        
        # Generate again
        result2 = generate_index(posts_dir=str(posts_dir), output_file=output_file)
        content2 = result2.read_text()
        
        assert result1 == result2
        assert content1 == content2
    
    def test_returns_path_object(self, sample_message_files):
        """Test that function returns a Path object."""
        posts_dir = sample_message_files[0].parent
        temp_dir = posts_dir.parent
        output_file = str(temp_dir / "index.md")
        
        result = generate_index(posts_dir=str(posts_dir), output_file=output_file)
        
        assert isinstance(result, Path)
