"""Unit tests for readings HTML generator."""

import pytest
from datetime import date
from pathlib import Path
from bs4 import BeautifulSoup
from catholic_liturgy_tools.generator.readings import (
    generate_readings_html,
    generate_readings_page,
)
from catholic_liturgy_tools.scraper.models import DailyReading, ReadingEntry


@pytest.fixture
def sample_reading():
    """Create a sample DailyReading for testing."""
    return DailyReading(
        date=date(2025, 11, 22),
        date_display="November 22, 2025",
        liturgical_day="Saturday of the Thirty-Third Week in Ordinary Time",
        readings=[
            ReadingEntry(
                title="First Reading",
                citation="1 Maccabees 6:1-13",
                text=[
                    "King Antiochus was traversing the inland provinces.",
                    "When the king heard this news, he was struck with fear."
                ]
            ),
            ReadingEntry(
                title="Responsorial Psalm",
                citation="Psalm 9:2-3, 4, 6, 16, 19",
                text=[
                    "I will rejoice in your salvation, O LORD."
                ]
            ),
            ReadingEntry(
                title="Gospel",
                citation="Luke 20:27-40",
                text=[
                    "Some Sadducees came forward to pose this problem to Jesus.",
                    "Jesus said to them in reply."
                ]
            )
        ],
        source_url="https://bible.usccb.org/bible/readings/112225.cfm"
    )


@pytest.fixture
def reading_with_special_chars():
    """Create a reading with special HTML characters for testing sanitization."""
    return DailyReading(
        date=date(2025, 12, 25),
        date_display="December 25, 2025",
        liturgical_day="Christmas <Day> & Feast",
        readings=[
            ReadingEntry(
                title="Gospel",
                citation="John 1:1-18",
                text=[
                    "In the beginning was the Word, & the Word was with God.",
                    "He said, \"Let there be light\" and there was light."
                ]
            )
        ],
        source_url="https://bible.usccb.org/bible/readings/122525.cfm"
    )


class TestGenerateReadingsHTML:
    """Test suite for generate_readings_html function."""
    
    def test_html_structure(self, sample_reading):
        """Verify generated HTML has required HTML5 structure."""
        html = generate_readings_html(sample_reading)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check doctype (BeautifulSoup handles this specially)
        assert html.startswith("<!DOCTYPE html>")
        
        # Check required meta tags
        assert soup.find('html', lang='en')
        assert soup.find('meta', charset='UTF-8')
        assert soup.find('meta', attrs={'name': 'viewport'})
        assert soup.find('meta', attrs={'name': 'description'})
        
        # Check title
        title = soup.find('title')
        assert title is not None
        assert "Catholic Liturgy Tools" in title.string
    
    def test_embedded_css(self, sample_reading):
        """Verify CSS styles are embedded in the HTML."""
        html = generate_readings_html(sample_reading)
        soup = BeautifulSoup(html, 'html.parser')
        
        style_tag = soup.find('style')
        assert style_tag is not None
        
        # Check for key CSS rules
        css_content = style_tag.string
        assert "font-family: Georgia" in css_content
        assert "max-width: 800px" in css_content
        assert ".reading-entry" in css_content
        assert ".reading-title" in css_content
        assert "@media (max-width: 600px)" in css_content
    
    def test_navigation_link(self, sample_reading):
        """Verify navigation link is present and correct."""
        html = generate_readings_html(sample_reading)
        soup = BeautifulSoup(html, 'html.parser')
        
        nav_link = soup.find('a', class_='nav-link')
        assert nav_link is not None
        assert nav_link['href'] == "../index.html"
        assert "← Back to Index" in nav_link.get_text()
    
    def test_page_heading(self, sample_reading):
        """Verify H1 heading contains liturgical day."""
        html = generate_readings_html(sample_reading)
        soup = BeautifulSoup(html, 'html.parser')
        
        h1 = soup.find('h1')
        assert h1 is not None
        assert sample_reading.liturgical_day in h1.get_text()
    
    def test_date_display(self, sample_reading):
        """Verify date display is present and formatted correctly."""
        html = generate_readings_html(sample_reading)
        soup = BeautifulSoup(html, 'html.parser')
        
        date_para = soup.find('p', class_='date')
        assert date_para is not None
        assert sample_reading.date_display in date_para.get_text()
    
    def test_reading_entries(self, sample_reading):
        """Verify all reading entries are present."""
        html = generate_readings_html(sample_reading)
        soup = BeautifulSoup(html, 'html.parser')
        
        reading_divs = soup.find_all('div', class_='reading-entry')
        assert len(reading_divs) == 3  # Sample has 3 readings
        
        # Check each reading has title and text
        for reading_div in reading_divs:
            assert reading_div.find('h2', class_='reading-title')
            assert reading_div.find('div', class_='reading-text')
    
    def test_reading_titles(self, sample_reading):
        """Verify reading titles include citations."""
        html = generate_readings_html(sample_reading)
        soup = BeautifulSoup(html, 'html.parser')
        
        titles = soup.find_all('h2', class_='reading-title')
        assert len(titles) == 3
        
        # Check that citations are included
        assert "1 Maccabees 6:1-13" in titles[0].get_text()
        assert "Psalm 9:2-3, 4, 6, 16, 19" in titles[1].get_text()
        assert "Luke 20:27-40" in titles[2].get_text()
    
    def test_reading_paragraphs(self, sample_reading):
        """Verify reading text is split into paragraphs."""
        html = generate_readings_html(sample_reading)
        soup = BeautifulSoup(html, 'html.parser')
        
        # First reading has 2 paragraphs
        first_reading = soup.find_all('div', class_='reading-entry')[0]
        paragraphs = first_reading.find_all('p')
        
        # Should have 2 paragraphs
        assert len(paragraphs) == 2
        assert "King Antiochus" in paragraphs[0].get_text()
        assert "When the king heard" in paragraphs[1].get_text()
    
    def test_attribution_section(self, sample_reading):
        """Verify attribution section is present with correct link."""
        html = generate_readings_html(sample_reading)
        soup = BeautifulSoup(html, 'html.parser')
        
        attribution = soup.find('div', class_='attribution')
        assert attribution is not None
        
        link = attribution.find('a')
        assert link is not None
        assert link['href'] == sample_reading.source_url
        assert link['target'] == "_blank"
        assert link['rel'] == ["noopener", "noreferrer"]
        assert "USCCB.org" in link.get_text()
    
    def test_html_sanitization(self, reading_with_special_chars):
        """Verify HTML special characters are properly escaped."""
        html = generate_readings_html(reading_with_special_chars)
        
        # Check that raw HTML tags are not present
        assert "<Day>" not in html
        assert "<script>" not in html
        
        # Check that escaped versions are present
        assert "&lt;Day&gt;" in html or "Christmas" in html
        assert "&amp;" in html
        assert "&quot;" in html
    
    def test_meta_description(self, sample_reading):
        """Verify meta description contains date."""
        html = generate_readings_html(sample_reading)
        soup = BeautifulSoup(html, 'html.parser')
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        assert meta_desc is not None
        assert sample_reading.date_display in meta_desc['content']
    
    def test_title_tag(self, sample_reading):
        """Verify title tag format."""
        html = generate_readings_html(sample_reading)
        soup = BeautifulSoup(html, 'html.parser')
        
        title = soup.find('title')
        assert title is not None
        title_text = title.get_text()
        assert sample_reading.liturgical_day in title_text
        assert "Catholic Liturgy Tools" in title_text
        assert "|" in title_text  # Separator
    
    def test_empty_paragraphs_filtered(self):
        """Verify empty paragraphs are filtered out."""
        reading = DailyReading(
            date=date(2025, 11, 22),
            date_display="November 22, 2025",
            liturgical_day="Test Day",
            readings=[
                ReadingEntry(
                    title="Reading",
                    citation="Test 1:1",
                    text=["First paragraph", "", "  ", "Third paragraph"]
                )
            ],
            source_url="https://example.com"
        )
        
        html = generate_readings_html(reading)
        soup = BeautifulSoup(html, 'html.parser')
        
        reading_div = soup.find('div', class_='reading-entry')
        paragraphs = reading_div.find_all('p')
        
        # Should only have 2 paragraphs (empty ones filtered)
        assert len(paragraphs) == 2
        assert "First paragraph" in paragraphs[0].get_text()
        assert "Third paragraph" in paragraphs[1].get_text()
    
    def test_invalid_reading_raises_error(self):
        """Verify that invalid reading data raises ValidationError."""
        from catholic_liturgy_tools.scraper.exceptions import ValidationError
        
        invalid_reading = DailyReading(
            date="invalid-date",  # Invalid format
            date_display="",
            liturgical_day="",
            readings=[],
            source_url=""
        )
        
        with pytest.raises(ValidationError):
            generate_readings_html(invalid_reading)


class TestGenerateReadingsPage:
    """Test suite for generate_readings_page function."""
    
    def test_file_creation(self, sample_reading, tmp_path):
        """Verify that HTML file is created with correct name."""
        output_dir = tmp_path / "readings"
        file_path = generate_readings_page(sample_reading, str(output_dir))
        
        assert file_path.exists()
        assert file_path.name == "2025-11-22.html"
        assert file_path.parent == output_dir
    
    def test_directory_creation(self, sample_reading, tmp_path):
        """Verify that output directory is created if it doesn't exist."""
        output_dir = tmp_path / "new_readings_dir"
        assert not output_dir.exists()
        
        file_path = generate_readings_page(sample_reading, str(output_dir))
        
        assert output_dir.exists()
        assert file_path.exists()
    
    def test_file_content(self, sample_reading, tmp_path):
        """Verify that file contains correct HTML content."""
        output_dir = tmp_path / "readings"
        file_path = generate_readings_page(sample_reading, str(output_dir))
        
        content = file_path.read_text(encoding='utf-8')
        
        # Check for key elements
        assert "<!DOCTYPE html>" in content
        assert sample_reading.liturgical_day in content
        assert sample_reading.date_display in content
    
    def test_utf8_encoding(self, tmp_path):
        """Verify that file is written with UTF-8 encoding."""
        reading = DailyReading(
            date=date(2025, 12, 25),
            date_display="December 25, 2025",
            liturgical_day="Café with résumé",  # Unicode characters
            readings=[
                ReadingEntry(
                    title="Reading",
                    citation="Test 1:1",
                    text=["Naïve text with ü and é"]
                )
            ],
            source_url="https://example.com"
        )
        
        output_dir = tmp_path / "readings"
        file_path = generate_readings_page(reading, str(output_dir))
        
        # Read back with UTF-8 encoding
        content = file_path.read_text(encoding='utf-8')
        assert "Café" in content
        assert "résumé" in content
        assert "Naïve" in content
    
    def test_idempotent_operation(self, sample_reading, tmp_path):
        """Verify that function overwrites existing files (idempotent)."""
        output_dir = tmp_path / "readings"
        
        # Generate file first time
        file_path1 = generate_readings_page(sample_reading, str(output_dir))
        content1 = file_path1.read_text()
        mtime1 = file_path1.stat().st_mtime
        
        # Wait a tiny bit to ensure different mtime
        import time
        time.sleep(0.01)
        
        # Generate again (should overwrite)
        file_path2 = generate_readings_page(sample_reading, str(output_dir))
        content2 = file_path2.read_text()
        mtime2 = file_path2.stat().st_mtime
        
        assert file_path1 == file_path2  # Same path
        assert content1 == content2  # Same content
        assert mtime2 >= mtime1  # File was modified
    
    def test_default_output_dir(self, sample_reading, tmp_path, monkeypatch):
        """Verify default output directory is '_site/readings'."""
        # Change to temp directory for this test
        monkeypatch.chdir(tmp_path)
        
        file_path = generate_readings_page(sample_reading)
        
        assert file_path.parent.name == "readings"
        assert file_path.parent.parent.name == "_site"
        assert file_path.exists()
    
    def test_returns_path_object(self, sample_reading, tmp_path):
        """Verify that function returns a Path object."""
        output_dir = tmp_path / "readings"
        file_path = generate_readings_page(sample_reading, str(output_dir))
        
        assert isinstance(file_path, Path)
    
    def test_invalid_reading_raises_error(self, tmp_path):
        """Verify that invalid reading data raises ValidationError."""
        from catholic_liturgy_tools.scraper.exceptions import ValidationError
        
        invalid_reading = DailyReading(
            date="",
            date_display="",
            liturgical_day="",
            readings=[],
            source_url=""
        )
        
        output_dir = tmp_path / "readings"
        
        with pytest.raises(ValidationError):
            generate_readings_page(invalid_reading, str(output_dir))


class TestHTMLValidation:
    """Test suite for HTML5 validation requirements."""
    
    def test_wellformed_html(self, sample_reading):
        """Verify generated HTML is well-formed (parseable)."""
        html = generate_readings_html(sample_reading)
        
        # BeautifulSoup should parse without errors
        soup = BeautifulSoup(html, 'html.parser')
        assert soup is not None
        
        # Check that we have the basic structure
        assert soup.html is not None
        assert soup.head is not None
        assert soup.body is not None
    
    def test_required_attributes(self, sample_reading):
        """Verify required HTML attributes are present."""
        html = generate_readings_html(sample_reading)
        soup = BeautifulSoup(html, 'html.parser')
        
        # HTML element should have lang attribute
        html_tag = soup.find('html')
        assert html_tag.get('lang') == 'en'
        
        # Meta charset should be UTF-8
        meta_charset = soup.find('meta', charset=True)
        assert meta_charset.get('charset') == 'UTF-8'
        
        # Viewport meta should exist
        meta_viewport = soup.find('meta', attrs={'name': 'viewport'})
        assert meta_viewport is not None
    
    def test_proper_nesting(self, sample_reading):
        """Verify HTML elements are properly nested."""
        html = generate_readings_html(sample_reading)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check that style is in head
        assert soup.head.find('style') is not None
        
        # Check that content divs are in body
        assert soup.body.find('div', class_='reading-entry') is not None
        assert soup.body.find('div', class_='attribution') is not None
        
        # Check that H2 is inside reading-entry div
        reading_entry = soup.body.find('div', class_='reading-entry')
        assert reading_entry.find('h2') is not None
