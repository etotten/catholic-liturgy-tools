# HTML Format Contract

**Feature**: Daily Readings from Catholic Lectionary  
**Branch**: 002-daily-readings  
**Phase**: 1 (Design & Contracts)  
**Date**: 2025-11-22

## Purpose

This document specifies the HTML structure, styling, and content format for generated daily readings pages. It serves as a contract between the generator and consumers (browsers, tests, future enhancements).

---

## File Naming Convention

**Pattern**: `{YYYY-MM-DD}.html`

**Examples**:
- `2025-11-22.html`
- `2025-12-25.html`
- `2026-01-01.html`

**Location**: `readings/` directory (relative to repository root)

**Full Path Example**: `readings/2025-11-22.html`

---

## HTML Document Structure

### Complete Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Catholic liturgical readings for {date_display}">
    <title>{liturgical_day} | Catholic Liturgy Tools</title>
    <style>
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
        }
    </style>
</head>
<body>
    <a href="../index.html" class="nav-link">← Back to Index</a>
    
    <h1>{liturgical_day}</h1>
    <p class="date">{date_display}</p>
    
    <!-- Reading entries repeated for each reading -->
    <div class="reading-entry">
        <h2 class="reading-title">{reading_title}</h2>
        <div class="reading-text">
            <!-- Paragraphs repeated for each paragraph in reading -->
            <p>{paragraph_text}</p>
        </div>
    </div>
    
    <div class="attribution">
        <p>Readings from <a href="{source_url}" target="_blank" rel="noopener noreferrer">USCCB.org</a></p>
    </div>
</body>
</html>
```

---

## Element Specifications

### `<head>` Section

**Required Elements**:

1. **DOCTYPE Declaration**:
   ```html
   <!DOCTYPE html>
   ```
   - Must be HTML5 doctype
   - First line of document

2. **HTML Root Element**:
   ```html
   <html lang="en">
   ```
   - Language attribute must be "en" (English)

3. **Character Encoding**:
   ```html
   <meta charset="UTF-8">
   ```
   - Must be UTF-8 encoding

4. **Viewport Meta Tag**:
   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   ```
   - Enables responsive design on mobile devices

5. **Description Meta Tag**:
   ```html
   <meta name="description" content="Catholic liturgical readings for {date_display}">
   ```
   - Variable: `{date_display}` = Human-readable date (e.g., "November 22, 2025")

6. **Title Tag**:
   ```html
   <title>{liturgical_day} | Catholic Liturgy Tools</title>
   ```
   - Variable: `{liturgical_day}` = Full liturgical day name
   - Example: "Saturday of the Thirty-Third Week in Ordinary Time | Catholic Liturgy Tools"

7. **Embedded Styles**:
   ```html
   <style>
       /* CSS rules as specified above */
   </style>
   ```
   - All styles must be embedded (no external stylesheet)
   - Allows standalone HTML file (no dependencies)

---

### `<body>` Section

**Required Elements**:

1. **Navigation Link**:
   ```html
   <a href="../index.html" class="nav-link">← Back to Index</a>
   ```
   - Class: `nav-link`
   - Href: Relative path to index page
   - Text: "← Back to Index" (left arrow + text)

2. **Page Heading (H1)**:
   ```html
   <h1>{liturgical_day}</h1>
   ```
   - Variable: `{liturgical_day}` = Full liturgical day name
   - Example: "Saturday of the Thirty-Third Week in Ordinary Time"

3. **Date Display**:
   ```html
   <p class="date">{date_display}</p>
   ```
   - Class: `date`
   - Variable: `{date_display}` = Human-readable date
   - Format: "Month DD, YYYY"
   - Example: "November 22, 2025"

4. **Reading Entries** (1 or more):
   ```html
   <div class="reading-entry">
       <h2 class="reading-title">{reading_title}</h2>
       <div class="reading-text">
           <p>{paragraph_1}</p>
           <p>{paragraph_2}</p>
           <!-- ... more paragraphs as needed -->
       </div>
   </div>
   ```
   - Container class: `reading-entry`
   - Title class: `reading-title` (H2 element)
   - Text container class: `reading-text`
   - Paragraphs: Each paragraph wrapped in `<p>` tag

5. **Attribution Section**:
   ```html
   <div class="attribution">
       <p>Readings from <a href="{source_url}" target="_blank" rel="noopener noreferrer">USCCB.org</a></p>
   </div>
   ```
   - Class: `attribution`
   - Link to source USCCB page
   - Attributes: `target="_blank"` (open in new tab), `rel="noopener noreferrer"` (security)
   - Variable: `{source_url}` = Full USCCB URL

---

## Variable Specifications

### Template Variables

| Variable | Type | Format | Example | Source |
|----------|------|--------|---------|--------|
| `{liturgical_day}` | string | Free text | "Saturday of the Thirty-Third Week in Ordinary Time" | USCCB page title or H1 |
| `{date_display}` | string | "Month DD, YYYY" | "November 22, 2025" | Formatted from date |
| `{reading_title}` | string | Free text | "First Reading: 1 Maccabees 6:1-13" | USCCB reading header |
| `{paragraph_text}` | string | Free text | "King Antiochus was traversing..." | USCCB reading body |
| `{source_url}` | string | URL | "https://bible.usccb.org/bible/readings/112225.cfm" | USCCB readings URL |

### Reading Title Format

**Pattern**: `"{title}: {citation}"` or just `"{title}"` if citation already included

**Examples**:
- "First Reading: 1 Maccabees 6:1-13"
- "Responsorial Psalm: Psalm 9:2-3, 4, 6, 16, 19"
- "Gospel: Luke 20:27-40"

**Rules**:
- If citation is not already part of title, append with colon separator
- If citation is already in title, use as-is
- Prefer combined format for consistency

---

## CSS Styling Contract

### Color Palette

| Element | Color | Hex | Usage |
|---------|-------|-----|-------|
| Body text | Dark gray | `#333` | Main text content |
| Headings (H1) | Dark red | `#5d1a1a` | Page title |
| Subheadings (H2) | Medium red | `#8b3a3a` | Reading titles |
| Links | Dark red | `#5d1a1a` | Navigation and attribution links |
| Date text | Gray | `#666` | Date display, attribution |
| Background (body) | White | `#fff` | Page background |
| Background (readings) | Light gray | `#fafafa` | Reading entry background |
| Borders | Medium red | `#8b3a3a` | H1 underline, reading border-left |
| Border (attribution) | Light gray | `#ccc` | Top border |

**Design Rationale**: Traditional liturgical color scheme using burgundy/maroon tones, evoking reverence and solemnity.

### Typography

**Font Family**: 
```css
font-family: Georgia, 'Times New Roman', serif;
```
- Primary: Georgia (serif, widely available)
- Fallback: Times New Roman (serif)
- Final fallback: System serif font

**Font Sizes**:
- Body text: Default (16px typically)
- H1: 2em (32px typically)
- H2: 1.5em (24px typically)
- Attribution: 0.9em (14.4px typically)

**Line Height**: `1.6` for body text (optimal readability)

**Text Alignment**: `justify` for reading text (traditional typographic style)

### Layout

**Container**: 
```css
max-width: 800px;
margin: 40px auto;
padding: 0 20px;
```
- Maximum width for readability
- Centered on page
- Side padding for mobile devices

**Spacing**:
- Reading entries: `30px` vertical margin
- Paragraphs: `10px` vertical margin
- Attribution: `40px` top margin

### Responsive Design

**Breakpoint**: 600px

**Mobile Styles**:
```css
@media (max-width: 600px) {
    body {
        padding: 0 10px;
        margin: 20px auto;
    }
    h1 { font-size: 1.5em; }
    .reading-title { font-size: 1.2em; }
}
```

**Changes on Mobile**:
- Reduced padding (20px → 10px)
- Reduced margins (40px → 20px)
- Smaller H1 (2em → 1.5em)
- Smaller H2 (1.5em → 1.2em)

---

## Content Requirements

### Text Sanitization

**All text content MUST be HTML-escaped to prevent XSS**:

```python
import html

sanitized_text = html.escape(raw_text, quote=True)
```

**Characters to Escape**:
- `<` → `&lt;`
- `>` → `&gt;`
- `&` → `&amp;`
- `"` → `&quot;`
- `'` → `&#x27;`

**Exception**: HTML structure tags (only the ones we generate, not from external source)

### Paragraph Formatting

**Rules**:
1. Each paragraph from source wrapped in `<p>` tag
2. Empty paragraphs skipped
3. Whitespace trimmed from paragraph edges
4. Multiple consecutive spaces preserved (may be intentional formatting)
5. Line breaks (`<br>`) within paragraphs replaced with single space

**Example Transformation**:
```python
# Input (from USCCB)
paragraphs = [
    "King Antiochus was traversing  the inland provinces.",
    "",  # Empty
    "When the king heard this news, he was struck with fear."
]

# Output (in HTML)
<p>King Antiochus was traversing  the inland provinces.</p>
<p>When the king heard this news, he was struck with fear.</p>
```

---

## Validation Requirements

### HTML5 Validation

Generated HTML MUST pass W3C HTML5 validation:
- Valid doctype
- Valid structure (proper nesting)
- Required attributes present
- No deprecated elements or attributes

**Validation Tool**: https://validator.w3.org/nu/

### Accessibility Requirements

**Current Requirements** (basic):
- Semantic HTML (H1, H2, P tags)
- Alt text for images (if added in future)
- Sufficient color contrast (WCAG AA recommended)
- Responsive design (viewport meta tag)

**Future Enhancements** (not required now):
- ARIA labels for screen readers
- Skip navigation links
- Focus indicators for keyboard navigation

### Browser Compatibility

**Supported Browsers** (latest stable versions):
- Chrome/Chromium
- Firefox
- Safari
- Microsoft Edge

**Required Testing**: Visual inspection in at least 2 browsers

---

## Example Instances

### Example 1: Weekday with 3 Readings

**Filename**: `readings/2025-11-22.html`

**Variables**:
- `{liturgical_day}`: "Saturday of the Thirty-Third Week in Ordinary Time"
- `{date_display}`: "November 22, 2025"
- `{source_url}`: "https://bible.usccb.org/bible/readings/112225.cfm"

**Reading Entries**:
1. "First Reading: 1 Maccabees 6:1-13" (3 paragraphs)
2. "Responsorial Psalm: Psalm 9:2-3, 4, 6, 16, 19" (2 paragraphs)
3. "Gospel: Luke 20:27-40" (2 paragraphs)

**Total Size**: ~12 KB

---

### Example 2: Sunday with 4 Readings

**Filename**: `readings/2025-11-24.html`

**Variables**:
- `{liturgical_day}`: "Our Lord Jesus Christ, King of the Universe"
- `{date_display}`: "November 24, 2025"
- `{source_url}`: "https://bible.usccb.org/bible/readings/112425.cfm"

**Reading Entries**:
1. "First Reading: Daniel 7:13-14" (1 paragraph)
2. "Responsorial Psalm: Psalm 93:1, 1-2, 5" (1 paragraph)
3. "Second Reading: Revelation 1:5-8" (1 paragraph)
4. "Gospel: John 18:33b-37" (2 paragraphs)

**Total Size**: ~11 KB

---

### Example 3: Major Feast Day

**Filename**: `readings/2025-12-25.html`

**Variables**:
- `{liturgical_day}`: "The Nativity of the Lord (Christmas) - Mass During the Day"
- `{date_display}`: "December 25, 2025"
- `{source_url}`: "https://bible.usccb.org/bible/readings/122525-Day.cfm"

**Note**: Multiple Mass option detected and resolved to "Day" Mass

**Reading Entries**:
1. "First Reading: Isaiah 52:7-10" (1 paragraph)
2. "Responsorial Psalm: Psalm 98:1, 2-3, 3-4, 5-6" (1 paragraph)
3. "Second Reading: Hebrews 1:1-6" (2 paragraphs)
4. "Gospel: John 1:1-18" (3 paragraphs)

**Total Size**: ~14 KB

---

## Testing Requirements

### Manual Testing Checklist

- [ ] HTML validates as HTML5 (W3C validator)
- [ ] Page displays correctly in Chrome
- [ ] Page displays correctly in Firefox
- [ ] Page displays correctly in Safari (if on macOS)
- [ ] Responsive design works (resize browser window)
- [ ] Navigation link works (goes to index)
- [ ] Attribution link works (opens USCCB in new tab)
- [ ] Text is readable (contrast, font size)
- [ ] Colors match specification
- [ ] All readings display completely
- [ ] No JavaScript errors in console
- [ ] Page loads quickly (< 2 seconds)

### Automated Testing Requirements

**Structure Tests**:
```python
def test_html_structure():
    """Verify generated HTML has required structure."""
    html = generate_readings_html(sample_reading)
    soup = BeautifulSoup(html, 'html.parser')
    
    # Required elements
    assert soup.doctype == "html"
    assert soup.find('html', lang='en')
    assert soup.find('meta', charset='UTF-8')
    assert soup.find('meta', attrs={'name': 'viewport'})
    assert soup.find('title')
    assert soup.find('h1')
    assert soup.find('a', class_='nav-link')
    assert soup.find_all('div', class_='reading-entry')
    assert soup.find('div', class_='attribution')
```

**Content Tests**:
```python
def test_html_content():
    """Verify HTML contains correct content."""
    html = generate_readings_html(sample_reading)
    
    # Check liturgical day
    assert sample_reading.liturgical_day in html
    
    # Check each reading
    for reading_entry in sample_reading.readings:
        assert reading_entry.title_with_citation in html
        for paragraph in reading_entry.text:
            assert paragraph in html
```

**Sanitization Tests**:
```python
def test_html_sanitization():
    """Verify HTML special characters are escaped."""
    # Create reading with special characters
    reading = DailyReading(
        date="2025-11-22",
        date_display="November 22, 2025",
        liturgical_day="Test <script>alert('XSS')</script>",
        readings=[...],
        source_url="..."
    )
    
    html = generate_readings_html(reading)
    
    # Should NOT contain raw script tag
    assert "<script>" not in html
    # Should contain escaped version
    assert "&lt;script&gt;" in html
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-22 | Initial specification for feature 002-daily-readings |

---

## Future Enhancements (Out of Scope)

**Potential Future Changes**:
- External CSS stylesheet (for easier customization)
- Dark mode support (with `@media (prefers-color-scheme: dark)`)
- Print stylesheet (optimized for printing)
- Enhanced typography (web fonts via Google Fonts)
- Advanced responsive design (additional breakpoints)
- Interactive features (collapsible sections, search highlighting)
- Liturgical color indicators (visual representation)
- Multiple language support (i18n)

**Breaking Changes Require**:
- Major version bump (e.g., 2.0.0)
- Migration guide for existing HTML files
- Regeneration of all existing readings

---

**Document Status**: Complete - ready for implementation
