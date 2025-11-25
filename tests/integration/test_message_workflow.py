"""Integration tests for message generation workflow."""

import pytest
from pathlib import Path
from datetime import date
from catholic_liturgy_tools.generator.message import generate_message


class TestMessageWorkflow:
    """Integration tests for the complete message generation workflow."""
    
    def test_message_generation_creates_file_with_correct_structure(self, temp_dir):
        """Test that message generation creates a properly structured file."""
        output_dir = str(temp_dir / "_site" / "messages")
        
        # Generate message
        result_path = generate_message(output_dir=output_dir)
        
        # Verify file exists
        assert result_path.exists()
        
        # Verify file structure
        content = result_path.read_text()
        lines = content.split("\n")
        
        # Check YAML frontmatter
        assert lines[0] == "---"
        assert any("layout: post" in line for line in lines[:10])
        assert any("title:" in line for line in lines[:10])
        assert any("date:" in line for line in lines[:10])
        
        # Find closing frontmatter delimiter
        closing_delimiter_index = None
        for i in range(1, len(lines)):
            if lines[i] == "---":
                closing_delimiter_index = i
                break
        
        assert closing_delimiter_index is not None, "YAML frontmatter not properly closed"
        
        # Check content after frontmatter
        content_lines = lines[closing_delimiter_index + 1:]
        content_text = "\n".join(content_lines)
        
        assert "Hello Catholic World" in content_text
        assert date.today().isoformat() in content_text
    
    def test_message_generation_in_specific_directory(self, temp_dir):
        """Test message generation in a specified directory."""
        custom_dir = temp_dir / "custom_output"
        output_dir = str(custom_dir)
        
        result_path = generate_message(output_dir=output_dir)
        
        # Verify file is in the custom directory
        assert result_path.parent == custom_dir
        assert result_path.exists()
    
    def test_message_overwrite_idempotency(self, temp_dir):
        """Test that running generation multiple times is idempotent."""
        output_dir = str(temp_dir / "_site" / "messages")
        
        # Generate first time
        result1 = generate_message(output_dir=output_dir)
        content1 = result1.read_text()
        mtime1 = result1.stat().st_mtime
        
        # Small delay to ensure different mtime if file is modified
        import time
        time.sleep(0.01)
        
        # Generate second time
        result2 = generate_message(output_dir=output_dir)
        content2 = result2.read_text()
        
        # Same file path
        assert result1 == result2
        
        # Content should be identical for same day
        assert content1 == content2
        
        # File was updated (idempotent overwrite)
        assert result2.stat().st_mtime >= mtime1
    
    def test_multiple_days_create_separate_files(self, temp_dir):
        """Test that messages for different days create separate files (simulation)."""
        output_dir = str(temp_dir / "_site" / "messages")
        
        # Generate today's message
        result_today = generate_message(output_dir=output_dir)
        
        # Manually create a message for a different date to simulate multiple days
        from catholic_liturgy_tools.generator.message import generate_message_content, get_message_file_path
        from catholic_liturgy_tools.utils.file_ops import write_file_safe
        
        yesterday = "2025-11-21"
        yesterday_content = generate_message_content(yesterday)
        yesterday_path = get_message_file_path(yesterday, output_dir=output_dir)
        write_file_safe(yesterday_path, yesterday_content)
        
        # Verify both files exist
        assert result_today.exists()
        assert yesterday_path.exists()
        assert result_today != yesterday_path
        
        # Verify they have different dates in content
        today_content = result_today.read_text()
        yesterday_file_content = yesterday_path.read_text()
        
        assert date.today().isoformat() in today_content
        assert yesterday in yesterday_file_content
