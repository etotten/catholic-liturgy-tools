"""End-to-end tests for generate-index CLI command."""

import pytest
import subprocess
import sys
from pathlib import Path
from catholic_liturgy_tools.generator.message import generate_message_content, get_message_file_path
from catholic_liturgy_tools.utils.file_ops import write_file_safe


class TestGenerateIndexCLI:
    """E2E tests for the generate-index CLI command."""
    
    def test_generate_index_command_success(self, temp_dir, monkeypatch):
        """Test that generate-index command runs successfully."""
        # Create some message files first
        posts_dir = temp_dir / "_posts"
        posts_dir.mkdir()
        
        dates = ["2025-11-20", "2025-11-21", "2025-11-22"]
        for date in dates:
            content = generate_message_content(date)
            filepath = get_message_file_path(date, output_dir=str(posts_dir))
            write_file_safe(filepath, content)
        
        # Change to temp directory
        monkeypatch.chdir(temp_dir)
        
        # Run CLI command
        result = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", "generate-index"],
            capture_output=True,
            text=True,
        )
        
        # Verify command succeeded
        assert result.returncode == 0
        assert "Generated index" in result.stdout
        assert "index.md" in result.stdout
    
    def test_generate_index_command_creates_file(self, temp_dir, monkeypatch):
        """Test that generate-index command creates the expected file."""
        # Create message files
        posts_dir = temp_dir / "_posts"
        posts_dir.mkdir()
        
        date = "2025-11-22"
        content = generate_message_content(date)
        filepath = get_message_file_path(date, output_dir=str(posts_dir))
        write_file_safe(filepath, content)
        
        # Change to temp directory
        monkeypatch.chdir(temp_dir)
        
        # Run CLI command
        result = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", "generate-index"],
            capture_output=True,
            text=True,
        )
        
        assert result.returncode == 0
        
        # Verify index file was created
        index_file = temp_dir / "index.md"
        assert index_file.exists()
        
        # Verify file content
        content = index_file.read_text()
        assert "layout: page" in content
        assert "2025-11-22" in content
    
    def test_generate_index_with_no_messages(self, temp_dir, monkeypatch):
        """Test generate-index when no message files exist."""
        # Create empty _posts directory
        posts_dir = temp_dir / "_posts"
        posts_dir.mkdir()
        
        monkeypatch.chdir(temp_dir)
        
        # Run CLI command
        result = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", "generate-index"],
            capture_output=True,
            text=True,
        )
        
        # Should succeed even with no messages
        assert result.returncode == 0
        
        # Index file should still be created
        index_file = temp_dir / "index.md"
        assert index_file.exists()
    
    def test_generate_index_without_posts_directory(self, temp_dir, monkeypatch):
        """Test generate-index when _posts directory doesn't exist."""
        monkeypatch.chdir(temp_dir)
        
        # Run CLI command (no _posts directory exists)
        result = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", "generate-index"],
            capture_output=True,
            text=True,
        )
        
        # Should succeed (create empty index)
        assert result.returncode == 0
        
        # Index should be created
        index_file = temp_dir / "index.md"
        assert index_file.exists()
    
    def test_generate_index_idempotent(self, temp_dir, monkeypatch):
        """Test that running generate-index multiple times is idempotent."""
        # Create message files
        posts_dir = temp_dir / "_posts"
        posts_dir.mkdir()
        
        date = "2025-11-22"
        content = generate_message_content(date)
        filepath = get_message_file_path(date, output_dir=str(posts_dir))
        write_file_safe(filepath, content)
        
        monkeypatch.chdir(temp_dir)
        
        # Run first time
        result1 = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", "generate-index"],
            capture_output=True,
            text=True,
        )
        assert result1.returncode == 0
        
        index_file = temp_dir / "index.md"
        content1 = index_file.read_text()
        
        # Run second time
        result2 = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", "generate-index"],
            capture_output=True,
            text=True,
        )
        assert result2.returncode == 0
        
        content2 = index_file.read_text()
        
        # Content should be identical
        assert content1 == content2
    
    def test_cli_help_shows_generate_index(self):
        """Test that CLI help shows generate-index command."""
        result = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", "--help"],
            capture_output=True,
            text=True,
        )
        
        assert result.returncode == 0
        assert "generate-index" in result.stdout
