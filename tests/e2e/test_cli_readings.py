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


class TestGenerateReadingsWithReflections:
    """E2E tests for generate-readings command with --with-reflections flag."""
    
    def test_generate_readings_with_reflections_flag(self, temp_dir, monkeypatch, mock_anthropic_client):
        """Test generate-readings command with --with-reflections flag generates AI content."""
        monkeypatch.chdir(temp_dir)
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-api-key")
        
        # Mock the AnthropicClient in the generator module
        with patch("catholic_liturgy_tools.generator.readings.AnthropicClient", return_value=mock_anthropic_client):
            result = subprocess.run(
                [sys.executable, "-m", "catholic_liturgy_tools.cli", 
                 "generate-readings", "--date", "2025-11-22", 
                 "--output-dir", "readings", "--with-reflections"],
                capture_output=True,
                text=True,
            )
        
        assert result.returncode == 0
        assert "Generating AI-augmented content" in result.stdout
        assert "Successfully fetched readings" in result.stdout
        assert "Generated HTML page: readings/2025-11-22.html" in result.stdout
        
        # Verify file contains AI-generated content
        output_file = temp_dir / "readings" / "2025-11-22.html"
        assert output_file.exists()
        
        content = output_file.read_text()
        assert "<!DOCTYPE html>" in content
        
        # Check for synopses (italicized text above readings)
        assert "<em>" in content or "<i>" in content  # Synopsis formatting
        
    def test_generate_readings_with_reflections_includes_synopses(self, temp_dir, monkeypatch, mock_anthropic_client):
        """Test that --with-reflections flag generates synopses for each reading."""
        monkeypatch.chdir(temp_dir)
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-api-key")
        
        with patch("catholic_liturgy_tools.generator.readings.AnthropicClient", return_value=mock_anthropic_client):
            result = subprocess.run(
                [sys.executable, "-m", "catholic_liturgy_tools.cli", 
                 "generate-readings", "--date", "2025-11-22", 
                 "--output-dir", "readings", "--with-reflections"],
                capture_output=True,
                text=True,
            )
        
        assert result.returncode == 0
        
        output_file = temp_dir / "readings" / "2025-11-22.html"
        content = output_file.read_text()
        
        # Verify synopses appear in HTML
        # Synopses should be in italics and appear before each reading
        assert "synopsis" in content.lower() or "<em>" in content
        
    def test_generate_readings_without_api_key_fails_gracefully(self, temp_dir, monkeypatch):
        """Test that --with-reflections without API key fails gracefully."""
        monkeypatch.chdir(temp_dir)
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        
        result = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", 
             "generate-readings", "--date", "2025-11-22", 
             "--output-dir", "readings", "--with-reflections"],
            capture_output=True,
            text=True,
        )
        
        # Should either fail or fall back to non-reflection mode
        # Depending on implementation, this could return error code or succeed without AI
        assert result.returncode in [0, 1]
        
        if result.returncode == 0:
            # Graceful degradation: file created without AI content
            output_file = temp_dir / "readings" / "2025-11-22.html"
            assert output_file.exists()
        else:
            # Error case: should show helpful message
            assert "ANTHROPIC_API_KEY" in result.stderr or "API key" in result.stderr
            
    def test_generate_readings_help_includes_reflections_flag(self):
        """Test that help message includes --with-reflections flag."""
        result = subprocess.run(
            [sys.executable, "-m", "catholic_liturgy_tools.cli", 
             "generate-readings", "--help"],
            capture_output=True,
            text=True,
        )
        
        assert result.returncode == 0
        assert "--with-reflections" in result.stdout
        assert "AI" in result.stdout or "reflection" in result.stdout.lower()
        
    def test_generate_readings_with_reflections_cost_tracking(self, temp_dir, monkeypatch, mock_anthropic_client):
        """Test that --with-reflections tracks and reports API costs."""
        monkeypatch.chdir(temp_dir)
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-api-key")
        
        with patch("catholic_liturgy_tools.generator.readings.AnthropicClient", return_value=mock_anthropic_client):
            result = subprocess.run(
                [sys.executable, "-m", "catholic_liturgy_tools.cli", 
                 "generate-readings", "--date", "2025-11-22", 
                 "--output-dir", "readings", "--with-reflections"],
                capture_output=True,
                text=True,
            )
        
        assert result.returncode == 0
        
        # Should report cost information
        assert "cost" in result.stdout.lower() or "$" in result.stdout
