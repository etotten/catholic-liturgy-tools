"""HTML generation for daily liturgical readings pages."""

from pathlib import Path
from typing import Optional
from catholic_liturgy_tools.scraper.models import DailyReading
from catholic_liturgy_tools.utils.html_utils import sanitize_text, format_paragraphs


# CSS styles matching the HTML format contract specification
CSS_STYLES = """
        body {
            font-family: Georgia, 'Times New Roman', serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
            line-height: 1.6;
            color: #333;
            background-color: #fff;
        }
        
        h1 {
            color: #5d1a1a;
            border-bottom: 2px solid #8b3a3a;
            padding-bottom: 10px;
            margin-bottom: 10px;
            font-size: 2em;
        }
        
        .date {
            color: #666;
            font-style: italic;
            margin-bottom: 30px;
        }
        
        .reading-entry {
            margin: 30px 0;
            padding: 20px;
            background-color: #fafafa;
            border-left: 4px solid #8b3a3a;
        }
        
        .reading-title {
            color: #8b3a3a;
            margin-bottom: 15px;
            font-size: 1.5em;
        }
        
        .reading-synopsis {
            color: #666;
            font-style: italic;
            margin: 10px 0;
            padding-left: 10px;
            border-left: 3px solid #ccc;
        }
        
        .reading-text p {
            margin: 10px 0;
            text-align: justify;
        }
        
        .nav-link {
            display: inline-block;
            margin-bottom: 20px;
            color: #5d1a1a;
            text-decoration: none;
            font-weight: bold;
        }
        
        .nav-link:hover {
            text-decoration: underline;
        }
        
        .attribution {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ccc;
            font-size: 0.9em;
            color: #666;
            text-align: center;
        }
        
        .attribution a {
            color: #5d1a1a;
        }
        
        .reflection-section {
            margin: 40px 0;
            padding: 30px;
            background-color: #f5f0e8;
            border: 2px solid #8b3a3a;
            border-radius: 5px;
        }
        
        .reflection-section h2 {
            color: #5d1a1a;
            margin-top: 0;
            margin-bottom: 20px;
            font-size: 1.8em;
        }
        
        .reflection-section h3 {
            color: #8b3a3a;
            margin-top: 25px;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .reflection-text {
            margin-bottom: 25px;
            line-height: 1.8;
        }
        
        .reflection-text p {
            margin: 15px 0;
            text-align: justify;
        }
        
        .pondering-questions ul {
            list-style-type: none;
            padding-left: 0;
        }
        
        .pondering-questions li {
            margin: 12px 0;
            padding-left: 25px;
            position: relative;
            line-height: 1.6;
        }
        
        .pondering-questions li:before {
            content: "❖";
            position: absolute;
            left: 0;
            color: #8b3a3a;
            font-weight: bold;
        }
        
        .ccc-citations ul {
            list-style-type: none;
            padding-left: 0;
        }
        
        .ccc-citations li {
            margin: 15px 0;
            padding: 12px;
            background-color: #fff;
            border-left: 3px solid #8b3a3a;
            line-height: 1.6;
        }
        
        .ccc-citations strong {
            color: #5d1a1a;
        }
        
        @media (max-width: 600px) {
            body {
                padding: 0 10px;
                margin: 20px auto;
            }
            
            h1 {
                font-size: 1.5em;
            }
            
            .reading-title {
                font-size: 1.2em;
            }
            
            .reflection-section {
                padding: 20px 15px;
            }
            
            .reflection-section h2 {
                font-size: 1.5em;
            }
            
            .reflection-section h3 {
                font-size: 1.2em;
            }
        }
"""


def generate_readings_html(reading: DailyReading) -> str:
    """Generate complete HTML page for a daily reading.
    
    Creates a standalone HTML5 document with embedded CSS styles according
    to the HTML format contract specification. All text content is properly
    sanitized to prevent XSS attacks.
    
    Args:
        reading: DailyReading object containing all reading data
        
    Returns:
        Complete HTML document as a string
        
    Raises:
        ValidationError: If reading data is invalid (fails validation)
        
    Examples:
        >>> reading = DailyReading(date="2025-11-22", ...)
        >>> html = generate_readings_html(reading)
        >>> assert "<!DOCTYPE html>" in html
        >>> assert reading.liturgical_day in html
    """
    # Validate the reading data
    reading.validate()
    
    # Sanitize template variables
    liturgical_day_safe = sanitize_text(reading.liturgical_day)
    date_display_safe = sanitize_text(reading.date_display)
    source_url_safe = sanitize_text(reading.source_url)
    
    # Build reading entries HTML
    reading_entries_html = []
    for idx, reading_entry in enumerate(reading.readings):
        # Get title with citation
        title_safe = sanitize_text(reading_entry.title_with_citation)
        
        # Check for synopsis (AI-generated summary)
        synopsis_html = ""
        if reading.synopses and idx < len(reading.synopses):
            synopsis_data = reading.synopses[idx]
            synopsis_text = synopsis_data.get("synopsis_text", "")
            if synopsis_text:
                synopsis_safe = sanitize_text(synopsis_text)
                synopsis_html = f'\n        <p class="reading-synopsis"><em>{synopsis_safe}</em></p>'
        
        # Format and sanitize paragraphs
        paragraphs = format_paragraphs(reading_entry.text)
        paragraphs_html = "\n            ".join(
            f"<p>{sanitize_text(para)}</p>" for para in paragraphs
        )
        
        # Build reading entry
        entry_html = f"""    <div class="reading-entry">
        <h2 class="reading-title">{title_safe}</h2>{synopsis_html}
        <div class="reading-text">
            {paragraphs_html}
        </div>
    </div>"""
        reading_entries_html.append(entry_html)
    
    # Join all reading entries
    all_readings_html = "\n    \n".join(reading_entries_html)
    
    # Build reflection section HTML if reflection is present
    reflection_html = ""
    if hasattr(reading, 'reflection') and reading.reflection:
        reflection = reading.reflection
        
        # Format reflection text (already HTML from AI)
        reflection_text_safe = sanitize_text(reflection.reflection_text) if isinstance(reflection.reflection_text, str) else reflection.reflection_text
        
        # Format pondering questions
        questions_html = ""
        if reflection.pondering_questions:
            questions_list = "\n            ".join(
                f"<li>{sanitize_text(q)}</li>" for q in reflection.pondering_questions
            )
            questions_html = f"""
        <div class="pondering-questions">
            <h3>Pondering Questions</h3>
            <ul>
            {questions_list}
            </ul>
        </div>"""
        
        # Format CCC citations
        citations_html = ""
        if reflection.ccc_citations:
            citations_list = "\n            ".join(
                f'<li><strong>CCC {cit.paragraph_number}:</strong> {sanitize_text(cit.excerpt_text)}'
                + (f' <em>({sanitize_text(cit.context_note)})</em>' if cit.context_note else '')
                + '</li>'
                for cit in reflection.ccc_citations
            )
            citations_html = f"""
        <div class="ccc-citations">
            <h3>From the Catechism</h3>
            <ul>
            {citations_list}
            </ul>
        </div>"""
        
        # Build complete reflection section
        reflection_html = f"""
    
    <div class="reflection-section">
        <h2>Daily Reflection</h2>
        <div class="reflection-text">
            {reflection_text_safe}
        </div>{questions_html}{citations_html}
    </div>"""
    
    # Build complete HTML document
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Catholic liturgical readings for {date_display_safe}">
    <title>{liturgical_day_safe} | Catholic Liturgy Tools</title>
    <style>{CSS_STYLES}
    </style>
</head>
<body>
    <a href="../index.html" class="nav-link">← Back to Index</a>
    
    <h1>{liturgical_day_safe}</h1>
    <p class="date">{date_display_safe}</p>
    
{all_readings_html}{reflection_html}
    
    <div class="attribution">
        <p>Readings from <a href="{source_url_safe}" target="_blank" rel="noopener noreferrer">USCCB.org</a></p>
    </div>
</body>
</html>"""
    
    return html


def generate_readings_page(
    reading: DailyReading,
    output_dir: str = "_site/readings"
) -> Path:
    """Generate and save HTML page for a daily reading.
    
    Creates the output directory if it doesn't exist, generates the HTML
    content, and writes it to a file with UTF-8 encoding. The filename is
    derived from the reading's date in YYYY-MM-DD.html format.
    
    This function is idempotent - it will overwrite existing files with
    the same name.
    
    Args:
        reading: DailyReading object containing all reading data
        output_dir: Directory path where HTML file will be saved (default: "_site/readings")
        
    Returns:
        Path object pointing to the created HTML file
        
    Raises:
        ValidationError: If reading data is invalid (fails validation)
        OSError: If unable to create directory or write file
        
    Examples:
        >>> reading = DailyReading(date="2025-11-22", ...)
        >>> path = generate_readings_page(reading)
        >>> assert path.exists()
        >>> assert path.name == "2025-11-22.html"
    """
    # Generate the HTML content
    html_content = generate_readings_html(reading)
    
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Determine output filename from reading's filename property
    filename = reading.filename
    file_path = output_path / filename
    
    # Write HTML to file with UTF-8 encoding
    file_path.write_text(html_content, encoding='utf-8')
    
    return file_path
