"""Integration tests for index generation workflow."""

import pytest
from pathlib import Path
from catholic_liturgy_tools.generator.index import generate_index
from catholic_liturgy_tools.generator.message import generate_message_content, get_message_file_path
from catholic_liturgy_tools.utils.file_ops import write_file_safe


class TestIndexWorkflow:
    """Integration tests for the complete index generation workflow."""
    
    def test_index_generation_with_multiple_messages(self, temp_dir):
        """Test generating index with multiple message files."""
        posts_dir = temp_dir / "_posts"
        posts_dir.mkdir()
        
        # Create several message files
        dates = ["2025-11-20", "2025-11-21", "2025-11-22", "2025-11-23"]
        for date in dates:
            content = generate_message_content(date)
            filepath = get_message_file_path(date, output_dir=str(posts_dir))
            write_file_safe(filepath, content)
        
        # Generate index
        index_path = generate_index(posts_dir=str(posts_dir), output_file=str(temp_dir / "index.md"))
        
        # Verify index exists and contains all dates
        assert index_path.exists()
        index_content = index_path.read_text()
        
        for date in dates:
            assert date in index_content
    
    def test_index_reverse_chronological_order(self, temp_dir):
        """Test that index lists messages in reverse chronological order."""
        posts_dir = temp_dir / "_posts"
        posts_dir.mkdir()
        
        # Create messages in random order
        dates = ["2025-11-22", "2025-11-20", "2025-11-23", "2025-11-21"]
        for date in dates:
            content = generate_message_content(date)
            filepath = get_message_file_path(date, output_dir=str(posts_dir))
            write_file_safe(filepath, content)
        
        # Generate index
        index_path = generate_index(posts_dir=str(posts_dir), output_file=str(temp_dir / "index.md"))
        index_content = index_path.read_text()
        
        # Check order in content (newest first)
        pos_20 = index_content.index("2025-11-20")
        pos_21 = index_content.index("2025-11-21")
        pos_22 = index_content.index("2025-11-22")
        pos_23 = index_content.index("2025-11-23")
        
        assert pos_23 < pos_22 < pos_21 < pos_20
    
    def test_index_deduplication(self, temp_dir):
        """Test that duplicate dates don't appear multiple times in index."""
        posts_dir = temp_dir / "_posts"
        posts_dir.mkdir()
        
        # Create message files
        date = "2025-11-22"
        content = generate_message_content(date)
        filepath = get_message_file_path(date, output_dir=str(posts_dir))
        write_file_safe(filepath, content)
        
        # Generate index twice
        index_path = generate_index(posts_dir=str(posts_dir), output_file=str(temp_dir / "index.html"))
        index_content1 = index_path.read_text()
        
        # Regenerate index
        generate_index(posts_dir=str(posts_dir), output_file=str(temp_dir / "index.html"))
        index_content2 = index_path.read_text()
        
        # Content should be identical (no duplicates)
        assert index_content1 == index_content2
        
        # Count occurrences of date in HTML link format (just the date text, which appears once per link)
        # HTML format: <a href="messages/2025-11-22-daily-message.md">2025-11-22</a>
        link_pattern = f'<a href="messages/{date}-daily-message.md">{date}</a>'
        assert index_content2.count(link_pattern) == 1
    
    def test_index_updates_when_new_message_added(self, temp_dir):
        """Test that index can be regenerated with new messages."""
        posts_dir = temp_dir / "_posts"
        posts_dir.mkdir()
        
        # Create initial messages
        initial_dates = ["2025-11-20", "2025-11-21"]
        for date in initial_dates:
            content = generate_message_content(date)
            filepath = get_message_file_path(date, output_dir=str(posts_dir))
            write_file_safe(filepath, content)
        
        # Generate initial index (explicitly set readings_dir to avoid picking up real readings)
        index_path = generate_index(
            posts_dir=str(posts_dir), 
            readings_dir=str(temp_dir / "readings"),
            output_file=str(temp_dir / "index.md")
        )
        initial_content = index_path.read_text()
        
        assert "2025-11-20" in initial_content
        assert "2025-11-21" in initial_content
        assert "2025-11-22" not in initial_content
        
        # Add new message
        new_date = "2025-11-22"
        content = generate_message_content(new_date)
        filepath = get_message_file_path(new_date, output_dir=str(posts_dir))
        write_file_safe(filepath, content)
        
        # Regenerate index
        generate_index(posts_dir=str(posts_dir), output_file=str(temp_dir / "index.md"))
        updated_content = index_path.read_text()
        
        # New message should now appear
        assert "2025-11-22" in updated_content
        assert "2025-11-20" in updated_content
        assert "2025-11-21" in updated_content
    
    def test_complete_workflow_generate_and_index(self, temp_dir):
        """Test the complete workflow: generate messages then create index."""
        posts_dir = temp_dir / "_posts"
        
        # Generate messages using the message generator
        from catholic_liturgy_tools.generator.message import generate_message
        
        # Simulate generating messages over several days
        dates = ["2025-11-20", "2025-11-21", "2025-11-22"]
        for date in dates:
            content = generate_message_content(date)
            filepath = get_message_file_path(date, output_dir=str(posts_dir))
            write_file_safe(filepath, content)
        
        # Generate index
        index_path = generate_index(posts_dir=str(posts_dir), output_file=str(temp_dir / "index.html"))
        
        # Verify complete structure
        assert index_path.exists()
        assert (posts_dir / "2025-11-20-daily-message.md").exists()
        assert (posts_dir / "2025-11-21-daily-message.md").exists()
        assert (posts_dir / "2025-11-22-daily-message.md").exists()
        
        # Verify index content
        index_content = index_path.read_text()
        assert "<!DOCTYPE html>" in index_content  # HTML5 document
        for date in dates:
            assert date in index_content
            assert f"{date}-daily-message.md" in index_content
