"""End-to-end tests for generate-message CLI command."""

import pytest
import subprocess
import sys
from pathlib import Path
from datetime import date


class TestGenerateMessageCLI:
    """E2E tests for the generate-message CLI command."""
    
    def test_generate_message_command_success(self, temp_dir, monkeypatch):
        """Test that generate-message command runs successfully."""
        # Change to temp directory to generate message there
        monkeypatch.chdir(temp_dir)
        
        # Run CLI command
        result = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", "generate-message"],
            capture_output=True,
            text=True,
        )
        
        # Verify command succeeded
        assert result.returncode == 0
        
        # Verify success message in output
        assert "Generated daily message" in result.stdout
        assert date.today().isoformat() in result.stdout
    
    def test_generate_message_command_creates_file(self, temp_dir, monkeypatch):
        """Test that generate-message command creates the expected file."""
        # Change to temp directory
        monkeypatch.chdir(temp_dir)
        
        # Run CLI command
        result = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", "generate-message"],
            capture_output=True,
            text=True,
        )
        
        assert result.returncode == 0
        
        # Verify file was created
        today = date.today().isoformat()
        expected_file = temp_dir / "_site" / "messages" / f"{today}-daily-message.md"
        
        assert expected_file.exists()
        
        # Verify file content
        content = expected_file.read_text()
        assert "Hello Catholic World" in content
        assert today in content
        assert "layout: post" in content
    
    def test_generate_message_command_idempotent(self, temp_dir, monkeypatch):
        """Test that running generate-message multiple times is idempotent."""
        monkeypatch.chdir(temp_dir)
        
        # Run first time
        result1 = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", "generate-message"],
            capture_output=True,
            text=True,
        )
        assert result1.returncode == 0
        
        # Run second time
        result2 = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", "generate-message"],
            capture_output=True,
            text=True,
        )
        assert result2.returncode == 0
        
        # Verify file still exists and is valid
        today = date.today().isoformat()
        expected_file = temp_dir / "_site" / "messages" / f"{today}-daily-message.md"
        
        assert expected_file.exists()
        content = expected_file.read_text()
        assert "Hello Catholic World" in content
    
    def test_generate_message_command_without_args(self, temp_dir, monkeypatch):
        """Test that generate-message works without additional arguments."""
        monkeypatch.chdir(temp_dir)
        
        result = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", "generate-message"],
            capture_output=True,
            text=True,
        )
        
        assert result.returncode == 0
        assert "error" not in result.stdout.lower()
        assert "error" not in result.stderr.lower()
    
    def test_cli_help_shows_generate_message(self):
        """Test that CLI help shows generate-message command."""
        result = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", "--help"],
            capture_output=True,
            text=True,
        )
        
        assert result.returncode == 0
        assert "generate-message" in result.stdout
