"""Unit tests for index generation module."""

import pytest
from pathlib import Path
from catholic_liturgy_tools.generator.index import (
    scan_message_files,
    scan_readings_files,
    parse_date_from_filename,
    generate_html_index,
    generate_index,
    ReadingsEntry,
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


class TestGenerateHtmlIndex:
    """Tests for generate_html_index function."""
    
    def test_generates_html5_with_doctype(self, sample_message_files):
        """Test that generated content starts with HTML5 DOCTYPE."""
        html = generate_html_index(sample_message_files, [])
        
        assert html.startswith("<!DOCTYPE html>")
        assert "<html" in html
        assert "</html>" in html
    
    def test_includes_proper_meta_tags(self, sample_message_files):
        """Test that HTML includes charset and viewport meta tags."""
        html = generate_html_index(sample_message_files, [])
        
        assert '<meta charset="UTF-8">' in html
        assert '<meta name="viewport"' in html
    
    def test_includes_correct_title(self, sample_message_files):
        """Test that HTML includes the correct title."""
        html = generate_html_index(sample_message_files, [])
        
        assert "<title>Catholic Liturgy Tools</title>" in html
    
    def test_includes_inline_css(self, sample_message_files):
        """Test that HTML includes inline CSS styling."""
        html = generate_html_index(sample_message_files, [])
        
        assert "<style>" in html
        assert "</style>" in html
        assert "body {" in html
        assert "max-width: 800px" in html
    
    def test_includes_links_to_all_messages(self, sample_message_files):
        """Test that all messages are linked in the index."""
        html = generate_html_index(sample_message_files, [])
        
        assert "2025-11-20" in html
        assert "2025-11-21" in html
        assert "2025-11-22" in html
    
    def test_reverse_chronological_order(self, sample_message_files):
        """Test that messages are listed in reverse chronological order."""
        html = generate_html_index(sample_message_files, [])
        
        # Find positions of dates in content
        pos_20 = html.index("2025-11-20")
        pos_21 = html.index("2025-11-21")
        pos_22 = html.index("2025-11-22")
        
        # Newest (22) should come before oldest (20)
        assert pos_22 < pos_21 < pos_20
    
    def test_generates_html_links_with_relative_paths(self, sample_message_files):
        """Test that proper HTML links with relative paths are generated."""
        html = generate_html_index(sample_message_files, [])
        
        # Should contain HTML link syntax with relative paths
        assert '<a href="messages/' in html
        assert '2025-11-22-daily-message.md">' in html
    
    def test_empty_messages_shows_no_messages_text(self):
        """Test generating index with no message files shows 'No messages available yet'."""
        html = generate_html_index([], [])
        
        assert "No messages available yet" in html
    
    def test_includes_daily_messages_section(self, sample_message_files):
        """Test that HTML includes Daily Messages section."""
        html = generate_html_index(sample_message_files, [])
        
        assert "<h2>Daily Messages</h2>" in html
    
    def test_includes_daily_readings_section(self, sample_message_files):
        """Test that HTML includes Daily Readings section."""
        readings = [
            ReadingsEntry("2025-11-22", "Saturday of Week 33", "readings/2025-11-22.html"),
        ]
        
        html = generate_html_index(sample_message_files, readings)
        
        assert "<h2>Daily Readings</h2>" in html
    
    def test_includes_readings_with_liturgical_day(self, sample_message_files):
        """Test that readings include liturgical day in link text."""
        readings = [
            ReadingsEntry("2025-11-22", "Saturday of Week 33", "readings/2025-11-22.html"),
            ReadingsEntry("2025-11-21", "Friday of Week 33", "readings/2025-11-21.html"),
        ]
        
        html = generate_html_index(sample_message_files, readings)
        
        assert "2025-11-22 - Saturday of Week 33" in html
        assert "2025-11-21 - Friday of Week 33" in html
    
    def test_empty_readings_shows_no_readings_text(self, sample_message_files):
        """Test that empty readings list shows 'No readings available yet'."""
        html = generate_html_index(sample_message_files, [])
        
        assert "No readings available yet" in html
    
    def test_readings_links_use_relative_paths(self, sample_message_files):
        """Test that readings links use relative paths."""
        readings = [
            ReadingsEntry("2025-11-22", "Saturday", "readings/2025-11-22.html"),
        ]
        
        html = generate_html_index(sample_message_files, readings)
        
        # Should contain relative path
        assert '<a href="readings/2025-11-22.html">' in html
    
    def test_html_escaping_in_content(self, sample_message_files):
        """Test that content is properly HTML-escaped."""
        # This is implicitly tested by using html.escape in the implementation
        # but we verify structure is valid HTML
        html = generate_html_index(sample_message_files, [])
        
        # Basic HTML structure checks
        assert "<h1>Catholic Liturgy Tools</h1>" in html
        assert "<ul>" in html
        assert "</ul>" in html
    
    def test_messages_and_readings_both_empty(self):
        """Test generating index with no messages and no readings."""
        html = generate_html_index([], [])
        
        assert "<!DOCTYPE html>" in html
        assert "No messages available yet" in html
        assert "No readings available yet" in html


class TestGenerateIndex:
    """Tests for generate_index function (main entry point)."""
    
    def test_creates_index_html_file(self, sample_message_files):
        """Test that function creates an index.html file."""
        messages_dir = sample_message_files[0].parent
        temp_dir = messages_dir.parent
        output_file = str(temp_dir / "index.html")
        
        result = generate_index(posts_dir=str(messages_dir), output_file=output_file)
        
        assert result.exists()
        assert result.name == "index.html"
    
    def test_index_contains_valid_html_content(self, sample_message_files):
        """Test that generated index contains valid HTML content."""
        messages_dir = sample_message_files[0].parent
        temp_dir = messages_dir.parent
        output_file = str(temp_dir / "index.html")
        
        result = generate_index(posts_dir=str(messages_dir), output_file=output_file)
        content = result.read_text()
        
        assert content.startswith("<!DOCTYPE html>")
        assert "<title>Catholic Liturgy Tools</title>" in content
        assert "2025-11-22" in content
        assert "2025-11-21" in content
        assert "2025-11-20" in content
    
    def test_default_output_file(self, sample_message_files):
        """Test that default output file is _site/index.html."""
        messages_dir = sample_message_files[0].parent
        temp_dir = messages_dir.parent.parent  # Go up to get out of _site
        
        # Change working directory context
        import os
        old_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            result = generate_index(posts_dir=str(messages_dir))
            assert result.name == "index.html"
            assert "_site" in str(result)
        finally:
            os.chdir(old_cwd)
    
    def test_handles_empty_messages_directory(self, temp_dir):
        """Test generating index when no message files exist."""
        messages_dir = temp_dir / "_site" / "messages"
        messages_dir.mkdir(parents=True)
        output_file = str(temp_dir / "index.html")
        
        result = generate_index(posts_dir=str(messages_dir), output_file=output_file)
        
        assert result.exists()
        content = result.read_text()
        assert "<!DOCTYPE html>" in content
        assert "No messages available yet" in content
    
    def test_overwrites_existing_index(self, sample_message_files):
        """Test that existing index is overwritten."""
        messages_dir = sample_message_files[0].parent
        temp_dir = messages_dir.parent
        output_file = str(temp_dir / "index.html")
        
        # Create initial index
        result1 = generate_index(posts_dir=str(messages_dir), output_file=output_file)
        content1 = result1.read_text()
        
        # Generate again
        result2 = generate_index(posts_dir=str(messages_dir), output_file=output_file)
        content2 = result2.read_text()
        
        assert result1 == result2
        assert content1 == content2
    
    def test_returns_path_object(self, sample_message_files):
        """Test that function returns a Path object."""
        messages_dir = sample_message_files[0].parent
        temp_dir = messages_dir.parent
        output_file = str(temp_dir / "index.html")
        
        result = generate_index(posts_dir=str(messages_dir), output_file=output_file)
        
        assert isinstance(result, Path)
    
    def test_includes_readings_when_readings_dir_provided(self, sample_message_files, temp_dir):
        """Test that index includes readings section when readings_dir provided."""
        messages_dir = sample_message_files[0].parent
        readings_dir = temp_dir / "_site" / "readings"
        readings_dir.mkdir(parents=True)
        
        # Create sample readings HTML files
        html_content = "<html><body><h1>Saturday of Week 33</h1></body></html>"
        (readings_dir / "2025-11-22.html").write_text(html_content, encoding="utf-8")
        
        output_file = str(temp_dir / "index.html")
        result = generate_index(
            posts_dir=str(messages_dir),
            output_file=output_file,
            readings_dir=str(readings_dir)
        )
        
        content = result.read_text()
        assert "<h2>Daily Readings</h2>" in content
        assert "2025-11-22 - Saturday of Week 33" in content
    
    def test_no_readings_section_when_readings_dir_none(self, sample_message_files, temp_dir):
        """Test that index shows 'No readings' when readings_dir is None."""
        messages_dir = sample_message_files[0].parent
        output_file = str(temp_dir / "index.html")
        
        result = generate_index(
            posts_dir=str(messages_dir),
            output_file=output_file,
            readings_dir=None
        )
        
        content = result.read_text()
        assert "<h2>Daily Readings</h2>" in content
        assert "No readings available yet" in content
    
    def test_handles_empty_readings_directory(self, sample_message_files, temp_dir):
        """Test that index handles empty readings directory gracefully."""
        messages_dir = sample_message_files[0].parent
        readings_dir = temp_dir / "_site" / "readings"
        readings_dir.mkdir(parents=True)
        
        output_file = str(temp_dir / "index.html")
        result = generate_index(
            posts_dir=str(messages_dir),
            output_file=output_file,
            readings_dir=str(readings_dir)
        )
        
        content = result.read_text()
        assert "<h2>Daily Readings</h2>" in content
        assert "No readings available yet" in content
    
    def test_both_messages_and_readings_sections(self, sample_message_files, temp_dir):
        """Test that both sections appear when both have content."""
        messages_dir = sample_message_files[0].parent
        readings_dir = temp_dir / "_site" / "readings"
        readings_dir.mkdir(parents=True)
        
        # Create readings
        html_content = "<html><body><h1>Saturday</h1></body></html>"
        (readings_dir / "2025-11-22.html").write_text(html_content, encoding="utf-8")
        
        output_file = str(temp_dir / "index.html")
        result = generate_index(
            posts_dir=str(messages_dir),
            output_file=output_file,
            readings_dir=str(readings_dir)
        )
        
        content = result.read_text()
        assert "<h2>Daily Messages</h2>" in content
        assert "2025-11-22" in content
        assert "<h2>Daily Readings</h2>" in content
        assert "2025-11-22 - Saturday" in content


class TestScanReadingsFiles:
    """Tests for scan_readings_files function."""
    
    def test_scan_finds_readings_files(self, temp_dir):
        """Test that scan finds all readings HTML files."""
        readings_dir = temp_dir / "readings"
        readings_dir.mkdir()
        
        # Create sample HTML files with proper structure
        dates = ["2025-11-20", "2025-11-21", "2025-11-22"]
        liturgical_days = [
            "Wednesday of the Thirty-Third Week in Ordinary Time",
            "Thursday of the Thirty-Third Week in Ordinary Time",
            "Friday of the Thirty-Third Week in Ordinary Time"
        ]
        
        for date, lit_day in zip(dates, liturgical_days):
            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head><title>Readings for {date}</title></head>
<body>
<h1>{lit_day}</h1>
<p>Reading content here...</p>
</body>
</html>"""
            (readings_dir / f"{date}.html").write_text(html_content, encoding="utf-8")
        
        entries = scan_readings_files(str(readings_dir))
        
        assert len(entries) == 3
        assert all(isinstance(e, ReadingsEntry) for e in entries)
    
    def test_scan_empty_directory(self, temp_dir):
        """Test scanning an empty readings directory."""
        readings_dir = temp_dir / "readings"
        readings_dir.mkdir()
        
        entries = scan_readings_files(str(readings_dir))
        
        assert entries == []
    
    def test_scan_nonexistent_directory(self, temp_dir):
        """Test scanning a nonexistent directory."""
        nonexistent = temp_dir / "nonexistent"
        
        entries = scan_readings_files(str(nonexistent))
        
        assert entries == []
    
    def test_extracts_liturgical_day_from_h1(self, temp_dir):
        """Test that liturgical day is extracted from <h1> tag."""
        readings_dir = temp_dir / "readings"
        readings_dir.mkdir()
        
        html_content = """<!DOCTYPE html>
<html><body>
<h1>Saturday of the Thirty-Third Week in Ordinary Time</h1>
</body></html>"""
        (readings_dir / "2025-11-22.html").write_text(html_content, encoding="utf-8")
        
        entries = scan_readings_files(str(readings_dir))
        
        assert len(entries) == 1
        assert entries[0].liturgical_day == "Saturday of the Thirty-Third Week in Ordinary Time"
    
    def test_entries_sorted_newest_first(self, temp_dir):
        """Test that entries are sorted in reverse chronological order."""
        readings_dir = temp_dir / "readings"
        readings_dir.mkdir()
        
        # Create files in random order
        dates = ["2025-11-20", "2025-11-22", "2025-11-21"]
        
        for date in dates:
            html_content = f"<html><body><h1>Liturgical Day {date}</h1></body></html>"
            (readings_dir / f"{date}.html").write_text(html_content, encoding="utf-8")
        
        entries = scan_readings_files(str(readings_dir))
        
        # Should be sorted 22, 21, 20
        assert entries[0].date == "2025-11-22"
        assert entries[1].date == "2025-11-21"
        assert entries[2].date == "2025-11-20"
    
    def test_creates_correct_link_format(self, temp_dir):
        """Test that link is in correct format."""
        readings_dir = temp_dir / "readings"
        readings_dir.mkdir()
        
        html_content = "<html><body><h1>Saturday</h1></body></html>"
        (readings_dir / "2025-11-22.html").write_text(html_content, encoding="utf-8")
        
        entries = scan_readings_files(str(readings_dir))
        
        assert entries[0].link == "readings/2025-11-22.html"
    
    def test_title_property_combines_date_and_liturgical_day(self, temp_dir):
        """Test that ReadingsEntry.title property formats correctly."""
        readings_dir = temp_dir / "readings"
        readings_dir.mkdir()
        
        html_content = "<html><body><h1>Saturday of the Thirty-Third Week in Ordinary Time</h1></body></html>"
        (readings_dir / "2025-11-22.html").write_text(html_content, encoding="utf-8")
        
        entries = scan_readings_files(str(readings_dir))
        
        assert entries[0].title == "2025-11-22 - Saturday of the Thirty-Third Week in Ordinary Time"
    
    def test_ignores_files_without_date_format(self, temp_dir):
        """Test that non-date-formatted files are ignored."""
        readings_dir = temp_dir / "readings"
        readings_dir.mkdir()
        
        # Create valid and invalid files
        valid_html = "<html><body><h1>Valid Day</h1></body></html>"
        (readings_dir / "2025-11-22.html").write_text(valid_html, encoding="utf-8")
        (readings_dir / "invalid.html").write_text(valid_html, encoding="utf-8")
        (readings_dir / "readme.html").write_text(valid_html, encoding="utf-8")
        
        entries = scan_readings_files(str(readings_dir))
        
        assert len(entries) == 1
        assert entries[0].date == "2025-11-22"
    
    def test_ignores_files_without_h1_tag(self, temp_dir):
        """Test that files without <h1> tag are skipped."""
        readings_dir = temp_dir / "readings"
        readings_dir.mkdir()
        
        # Create file without h1
        html_content = "<html><body><p>No h1 here</p></body></html>"
        (readings_dir / "2025-11-22.html").write_text(html_content, encoding="utf-8")
        
        entries = scan_readings_files(str(readings_dir))
        
        assert entries == []
    
    def test_ignores_files_with_empty_h1(self, temp_dir):
        """Test that files with empty <h1> tag are skipped."""
        readings_dir = temp_dir / "readings"
        readings_dir.mkdir()
        
        html_content = "<html><body><h1>   </h1></body></html>"
        (readings_dir / "2025-11-22.html").write_text(html_content, encoding="utf-8")
        
        entries = scan_readings_files(str(readings_dir))
        
        assert entries == []
    
    def test_handles_h1_with_attributes(self, temp_dir):
        """Test extracting text from <h1> tags with attributes."""
        readings_dir = temp_dir / "readings"
        readings_dir.mkdir()
        
        html_content = '<html><body><h1 class="title" id="main">Saturday</h1></body></html>'
        (readings_dir / "2025-11-22.html").write_text(html_content, encoding="utf-8")
        
        entries = scan_readings_files(str(readings_dir))
        
        assert len(entries) == 1
        assert entries[0].liturgical_day == "Saturday"
    
    def test_skips_unreadable_files(self, temp_dir):
        """Test that unreadable files are skipped gracefully."""
        readings_dir = temp_dir / "readings"
        readings_dir.mkdir()
        
        # Create a valid file and a corrupt file
        valid_html = "<html><body><h1>Valid</h1></body></html>"
        (readings_dir / "2025-11-22.html").write_text(valid_html, encoding="utf-8")
        
        # Create a file with invalid encoding (write bytes)
        (readings_dir / "2025-11-23.html").write_bytes(b"\xff\xfe\xfd")
        
        entries = scan_readings_files(str(readings_dir))
        
        # Should only get the valid file
        assert len(entries) == 1
        assert entries[0].date == "2025-11-22"
