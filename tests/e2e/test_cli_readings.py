"""End-to-end tests for generate-readings CLI command."""

import pytest
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch
from datetime import date


class TestGenerateReadingsCommand:
    """Tests for the generate-readings command."""
    
    def test_generate_readings_with_date(self, temp_dir, monkeypatch):
        """Test generate-readings command with specific date."""
        monkeypatch.chdir(temp_dir)
        
        # Run command with a date that we know exists
        result = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", 
             "generate-readings", "--date", "2025-11-22", 
             "--output-dir", "readings"],
            capture_output=True,
            text=True,
        )
        
        assert result.returncode == 0
        assert "Fetching readings for November 22, 2025" in result.stdout
        assert "Successfully fetched readings" in result.stdout
        assert "Generated HTML page: readings/2025-11-22.html" in result.stdout
        
        # Verify file was created
        output_file = temp_dir / "readings" / "2025-11-22.html"
        assert output_file.exists()
        
        # Verify file contains expected content
        content = output_file.read_text()
        assert "<!DOCTYPE html>" in content
        assert "November 22, 2025" in content
    
    def test_generate_readings_without_date_uses_today(self, temp_dir, monkeypatch):
        """Test generate-readings command without date uses today."""
        monkeypatch.chdir(temp_dir)
        
        # Run command without date
        result = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", 
             "generate-readings", "--output-dir", "readings"],
            capture_output=True,
            text=True,
        )
        
        assert result.returncode == 0
        assert "Fetching readings for" in result.stdout
        assert "Successfully fetched readings" in result.stdout
        assert "Generated HTML page:" in result.stdout
        
        # Verify a file was created
        readings_dir = temp_dir / "readings"
        assert readings_dir.exists()
        html_files = list(readings_dir.glob("*.html"))
        assert len(html_files) == 1
    
    def test_generate_readings_creates_output_directory(self, temp_dir, monkeypatch):
        """Test that output directory is created if it doesn't exist."""
        monkeypatch.chdir(temp_dir)
        
        custom_dir = "custom_readings"
        
        result = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", 
             "generate-readings", "--date", "2025-11-22", 
             "--output-dir", custom_dir],
            capture_output=True,
            text=True,
        )
        
        assert result.returncode == 0
        assert (temp_dir / custom_dir).exists()
        assert (temp_dir / custom_dir / "2025-11-22.html").exists()
    
    def test_generate_readings_invalid_date_format(self, temp_dir, monkeypatch):
        """Test error handling with invalid date format."""
        monkeypatch.chdir(temp_dir)
        
        result = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", 
             "generate-readings", "--date", "11/22/2025"],
            capture_output=True,
            text=True,
        )
        
        assert result.returncode == 2
        assert "Error: Invalid date format" in result.stderr
        assert "Expected format: YYYY-MM-DD" in result.stderr
    
    def test_generate_readings_invalid_date_values(self, temp_dir, monkeypatch):
        """Test error handling with invalid date values."""
        monkeypatch.chdir(temp_dir)
        
        # Invalid month
        result = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", 
             "generate-readings", "--date", "2025-13-01"],
            capture_output=True,
            text=True,
        )
        
        assert result.returncode == 2
        assert "Error: Invalid date format" in result.stderr
    
    def test_generate_readings_idempotent(self, temp_dir, monkeypatch):
        """Test that running command twice is idempotent."""
        monkeypatch.chdir(temp_dir)
        
        # Run command first time
        result1 = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", 
             "generate-readings", "--date", "2025-11-22", 
             "--output-dir", "readings"],
            capture_output=True,
            text=True,
        )
        
        assert result1.returncode == 0
        
        # Run command second time
        result2 = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", 
             "generate-readings", "--date", "2025-11-22", 
             "--output-dir", "readings"],
            capture_output=True,
            text=True,
        )
        
        assert result2.returncode == 0
        
        # Verify file still exists and is valid
        output_file = temp_dir / "readings" / "2025-11-22.html"
        assert output_file.exists()
        content = output_file.read_text()
        assert "<!DOCTYPE html>" in content
    
    def test_generate_readings_with_short_options(self, temp_dir, monkeypatch):
        """Test generate-readings command with short options."""
        monkeypatch.chdir(temp_dir)
        
        result = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", 
             "generate-readings", "-d", "2025-11-22", 
             "-o", "readings"],
            capture_output=True,
            text=True,
        )
        
        assert result.returncode == 0
        assert "Successfully fetched readings" in result.stdout
    
    def test_generate_readings_help(self):
        """Test generate-readings help message."""
        result = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", 
             "generate-readings", "--help"],
            capture_output=True,
            text=True,
        )
        
        assert result.returncode == 0
        assert "generate-readings" in result.stdout
        assert "--date" in result.stdout
        assert "--output-dir" in result.stdout
        assert "YYYY-MM-DD" in result.stdout
