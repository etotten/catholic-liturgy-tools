"""Unit tests for file_ops module."""

import pytest
from pathlib import Path
from catholic_liturgy_tools.utils.file_ops import ensure_directory_exists, write_file_safe


class TestEnsureDirectoryExists:
    """Tests for ensure_directory_exists function."""
    
    def test_create_directory_from_string(self, temp_dir):
        """Test creating a directory from a string path."""
        test_dir = temp_dir / "test_dir"
        result = ensure_directory_exists(str(test_dir))
        
        assert result == test_dir
        assert test_dir.exists()
        assert test_dir.is_dir()
    
    def test_create_directory_from_path(self, temp_dir):
        """Test creating a directory from a Path object."""
        test_dir = temp_dir / "test_dir"
        result = ensure_directory_exists(test_dir)
        
        assert result == test_dir
        assert test_dir.exists()
        assert test_dir.is_dir()
    
    def test_create_nested_directories(self, temp_dir):
        """Test creating nested directories."""
        nested_dir = temp_dir / "parent" / "child" / "grandchild"
        result = ensure_directory_exists(nested_dir)
        
        assert result == nested_dir
        assert nested_dir.exists()
        assert nested_dir.is_dir()
    
    def test_directory_already_exists(self, temp_dir):
        """Test that existing directory is handled correctly."""
        test_dir = temp_dir / "existing"
        test_dir.mkdir()
        
        # Should not raise an error
        result = ensure_directory_exists(test_dir)
        
        assert result == test_dir
        assert test_dir.exists()
    
    def test_returns_path_object(self, temp_dir):
        """Test that function returns a Path object."""
        test_dir = temp_dir / "test_dir"
        result = ensure_directory_exists(test_dir)
        
        assert isinstance(result, Path)


class TestWriteFileSafe:
    """Tests for write_file_safe function."""
    
    def test_write_file_from_string_path(self, temp_dir):
        """Test writing a file from a string path."""
        filepath = temp_dir / "test.txt"
        content = "Hello, World!"
        
        result = write_file_safe(str(filepath), content)
        
        assert result == filepath
        assert filepath.exists()
        assert filepath.read_text() == content
    
    def test_write_file_from_path_object(self, temp_dir):
        """Test writing a file from a Path object."""
        filepath = temp_dir / "test.txt"
        content = "Hello, World!"
        
        result = write_file_safe(filepath, content)
        
        assert result == filepath
        assert filepath.exists()
        assert filepath.read_text() == content
    
    def test_write_file_creates_parent_directories(self, temp_dir):
        """Test that parent directories are created if they don't exist."""
        filepath = temp_dir / "parent" / "child" / "test.txt"
        content = "Nested file"
        
        result = write_file_safe(filepath, content)
        
        assert result == filepath
        assert filepath.exists()
        assert filepath.read_text() == content
        assert filepath.parent.exists()
    
    def test_write_file_with_utf8_encoding(self, temp_dir):
        """Test writing a file with UTF-8 encoding (including special characters)."""
        filepath = temp_dir / "utf8.txt"
        content = "Hello Catholic World 🙏 †"
        
        result = write_file_safe(filepath, content, encoding="utf-8")
        
        assert result == filepath
        assert filepath.exists()
        assert filepath.read_text(encoding="utf-8") == content
    
    def test_write_file_overwrites_existing(self, temp_dir):
        """Test that existing files are overwritten."""
        filepath = temp_dir / "test.txt"
        original_content = "Original"
        new_content = "Updated"
        
        # Write original content
        filepath.write_text(original_content)
        
        # Overwrite with new content
        result = write_file_safe(filepath, new_content)
        
        assert result == filepath
        assert filepath.read_text() == new_content
    
    def test_returns_path_object(self, temp_dir):
        """Test that function returns a Path object."""
        filepath = temp_dir / "test.txt"
        
        result = write_file_safe(filepath, "content")
        
        assert isinstance(result, Path)
    
    def test_write_multiline_content(self, temp_dir):
        """Test writing multiline content."""
        filepath = temp_dir / "multiline.txt"
        content = """Line 1
Line 2
Line 3"""
        
        result = write_file_safe(filepath, content)
        
        assert result == filepath
        assert filepath.read_text() == content
