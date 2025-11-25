# Research & Technical Decisions

**Feature**: Daily Readings from Catholic Lectionary  
**Branch**: 002-daily-readings  
**Phase**: 0 (Research)  
**Date**: 2025-11-22

## Purpose

This document captures research findings, technical decisions, and rationale for implementation choices for the Daily Readings feature. It serves as a reference for developers working on this feature and documents the "why" behind key decisions.

---

## USCCB Website Analysis

### Base URL Structure

**Primary readings URL**: `https://bible.usccb.org/bible/readings/{MMDDYY}.cfm`

**Examples**:
- November 22, 2025: `https://bible.usccb.org/bible/readings/112225.cfm`
- December 25, 2025: `https://bible.usccb.org/bible/readings/122525.cfm`
- January 1, 2026: `https://bible.usccb.org/bible/readings/010126.cfm`

**Format**: `MMDDYY` (zero-padded month and day, 2-digit year)

---

### HTML Structure Analysis

Based on analysis of the try1 repo scraper code and USCCB site patterns:

#### Page Title / Liturgical Day

**Strategy 1 (Most Reliable)**: Extract from `<title>` tag
```html
<title>Saturday of the Thirty-Third Week in Ordinary Time | USCCB</title>
```
- Split on `|` and take first part
- Strip whitespace

**Strategy 2 (Fallback)**: Extract from H1 with class `page-title`
```html
<h1 class="page-title">Saturday of the Thirty-Third Week in Ordinary Time</h1>
```

**Strategy 3 (Last Resort)**: Any H1 tag
```html
<h1>Saturday of the Thirty-Third Week in Ordinary Time</h1>
```

**Decision**: Implement all three strategies in order, use first successful match. Log warning if fallbacks used.

---

#### Reading Entries Structure

**Pattern**: Readings are in `<div class="content-header">` followed by `<div class="content-body">`

**Header Structure**:
```html
<div class="content-header">
    <h3 class="name">First Reading</h3>
    <div class="address">
        <a href="/bible/...">1 Maccabees 6:1-13</a>
    </div>
</div>
```

**Body Structure**:
```html
<div class="content-body">
    <p>King Antiochus was traversing the inland provinces...</p>
    <p>When the king heard this news, he was struck with fear...</p>
    <p>He was seized with great grief and such misery...</p>
</div>
```

**Extraction Algorithm**:
1. Find all `<div class="content-header">` elements
2. For each header:
   - Extract title from `<h3 class="name">`
   - Extract citation from `<div class="address"> <a>` text
   - Find next sibling `<div class="content-body">`
   - Extract all `<p>` tags as text (list of paragraphs)
3. Validate: must have title, citation, and at least one paragraph

**Edge Cases**:
- Some readings may have poetry/verse structure (ignore for now, treat as prose)
- Some passages may have verse numbers in text (keep them)
- Text may have `<br>` tags (replace with spaces)
- May have nested tags like `<strong>` or `<em>` (extract text only)

---

#### Multiple Mass Options

Some major feast days have multiple Masses with different readings:

**Example**: Christmas Day (December 25)
- Hub page: `122525.cfm`
- Vigil Mass: `122525-Vigil.cfm`
- Night Mass: `122525-Night.cfm`
- Dawn Mass: `122525-Dawn.cfm`
- Day Mass: `122525-Day.cfm`

**Detection Strategy**:
1. Check hub page for links matching pattern `{MMDDYY}-[A-Za-z]+\.cfm`
2. Exclude Spanish versions (URLs containing `/es/`)
3. If multiple found, select the **last one** (typically most solemn)
4. Fetch that specific Mass readings page

**Implementation**:
```python
def _check_for_multiple_masses(soup, date_str):
    """Check for multiple Mass options and return primary URL."""
    pattern = re.compile(rf'{date_str}-[A-Za-z]+\.cfm')
    links = soup.find_all('a', href=True)
    mass_options = []
    
    for link in links:
        href = link['href']
        if pattern.search(href) and '/es/' not in href:
            full_url = urljoin(self.BASE_URL, href)
            if full_url not in mass_options:
                mass_options.append(full_url)
    
    return mass_options[-1] if mass_options else None
```

**Decision**: Follow try1 repo approach of selecting last Mass option. Document this behavior as selecting "primary/most solemn Mass."

---

### Typical Reading Counts

**Weekdays**: 3 readings
- First Reading
- Responsorial Psalm
- Gospel

**Sundays and Solemnities**: 4 readings
- First Reading
- Responsorial Psalm
- Second Reading
- Gospel

**Special Cases**: Some feasts may have additional readings or different structures. Handle gracefully.

**Validation**: Require at least 1 reading, accept up to 10 (arbitrary upper bound for sanity).

---

## HTML Generation Strategy

### Template Approach

**Decision**: Use Python f-strings for HTML templates (not external template engine).

**Rationale**:
- No new dependencies (Jinja2 would add complexity)
- Simple structure doesn't warrant template engine
- Easy to understand and modify
- Fast rendering
- Can refactor to Jinja2 later if needed

**Alternative Considered**: Jinja2 templates
- **Pros**: More powerful, better separation of concerns
- **Cons**: New dependency, overkill for simple structure
- **Decision**: Defer until complexity warrants it

---

### HTML5 Structure

**Basic Template**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{liturgical_day} | Catholic Liturgy Tools</title>
    <style>
        /* Embedded CSS for simplicity */
        body {
            font-family: Georgia, serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
            line-height: 1.6;
            color: #333;
        }
        h1 {
            color: #5d1a1a;
            border-bottom: 2px solid #8b3a3a;
            padding-bottom: 10px;
        }
        .reading-entry {
            margin: 30px 0;
        }
        .reading-title {
            color: #8b3a3a;
            margin-bottom: 5px;
        }
        .reading-text p {
            margin: 10px 0;
            text-align: justify;
        }
        .nav-link {
            display: inline-block;
            margin-bottom: 20px;
            color: #5d1a1a;
        }
        .attribution {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ccc;
            font-size: 0.9em;
            color: #666;
        }
    </style>
</head>
<body>
    <a href="../index.html" class="nav-link">← Back to Index</a>
    
    <h1>{liturgical_day}</h1>
    <p class="date">{date_display}</p>
    
    {readings_html}
    
    <div class="attribution">
        <p>Readings from <a href="{source_url}">USCCB.org</a></p>
    </div>
</body>
</html>
```

**Reading Entry Template**:
```html
<div class="reading-entry">
    <h2 class="reading-title">{title}</h2>
    <div class="reading-text">
        {paragraphs}
    </div>
</div>
```

**Paragraph Template**:
```html
<p>{paragraph_text}</p>
```

**Design Decisions**:
- **Embedded CSS**: Simpler than external stylesheet, no additional HTTP request
- **Semantic HTML**: Use appropriate tags (h1, h2, p, div with classes)
- **Responsive**: `max-width` and mobile viewport meta tag
- **Color Scheme**: Traditional liturgical colors (burgundy/maroon tones)
- **Typography**: Serif font (Georgia) for readability and traditional feel
- **Attribution**: Link back to USCCB source for transparency and respect

---

### Text Sanitization

**Need**: Protect against malicious HTML (unlikely from USCCB, but good practice)

**Approach**: Basic HTML escaping for user-generated content (even though source is USCCB)

**Implementation**:
```python
import html

def sanitize_text(text: str) -> str:
    """Escape HTML special characters."""
    return html.escape(text, quote=True)
```

**Decision**: Use Python's built-in `html.escape()` for simplicity. If more complex sanitization needed later, consider `bleach` library.

---

## Error Handling Strategy

### Exception Hierarchy

```python
class LiturgyToolsError(Exception):
    """Base exception for all liturgy tools errors."""
    pass

class ScraperError(LiturgyToolsError):
    """Base exception for scraping errors."""
    pass

class NetworkError(ScraperError):
    """Network-related errors (timeout, connection, HTTP errors)."""
    pass

class ParseError(ScraperError):
    """HTML parsing errors (unexpected structure, missing elements)."""
    pass

class ValidationError(LiturgyToolsError):
    """Data validation errors."""
    pass

class DateError(ValidationError):
    """Invalid or malformed date."""
    pass

class GenerationError(LiturgyToolsError):
    """HTML generation errors."""
    pass

class FileSystemError(GenerationError):
    """File I/O errors."""
    pass
```

**Rationale**:
- Clear hierarchy for specific error handling
- Allows catching broad categories or specific errors
- Follows Python exception best practices
- Enables specific error messages for users

---

### Retry Logic with Exponential Backoff

**Pattern** (from try1 repo, refined):

```python
import time
from functools import wraps

def retry_with_backoff(max_attempts=3, backoff_factor=2.0):
    """Decorator for retrying functions with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except (requests.Timeout, requests.ConnectionError) as e:
                    if attempt == max_attempts:
                        raise NetworkError(f"Failed after {max_attempts} attempts: {e}")
                    
                    wait_time = backoff_factor ** attempt
                    logger.warning(f"Attempt {attempt} failed: {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                except Exception:
                    raise  # Don't retry other exceptions
        return wrapper
    return decorator
```

**Usage**:
```python
@retry_with_backoff(max_attempts=3)
def _fetch_page(self, url):
    response = self.session.get(url, timeout=self.timeout)
    response.raise_for_status()
    return response
```

**Parameters**:
- `max_attempts=3`: Try up to 3 times total
- `backoff_factor=2.0`: Wait 2s, 4s, 8s between attempts
- Only retry on network errors (Timeout, ConnectionError)
- Raise other exceptions immediately (ParseError, etc.)

---

## Dependency Analysis

### BeautifulSoup4 vs Alternatives

**Chosen**: BeautifulSoup4 with lxml parser

**Alternatives Considered**:

1. **lxml alone**
   - **Pros**: Fast, powerful XPath support
   - **Cons**: More complex API, steeper learning curve, less forgiving of malformed HTML
   - **Decision**: Use as parser backend for BeautifulSoup

2. **html.parser (stdlib)**
   - **Pros**: No dependencies, built-in
   - **Cons**: Slower, less robust with malformed HTML
   - **Decision**: Could use as fallback, but lxml is preferred

3. **html5lib**
   - **Pros**: Most forgiving, handles HTML5 like browsers do
   - **Cons**: Much slower, unnecessary for USCCB's well-formed HTML
   - **Decision**: Not needed

4. **Scrapy framework**
   - **Pros**: Full-featured scraping framework
   - **Cons**: Heavy dependency, overkill for single site, adds complexity
   - **Decision**: Too much for this use case

**Final Decision**: BeautifulSoup4 + lxml
- Industry standard for Python web scraping
- Excellent documentation and community support
- Handles malformed HTML gracefully
- Fast parsing with lxml backend
- Simple, intuitive API
- Well-tested and maintained

**Dependency Versions**:
```toml
beautifulsoup4>=4.12.0
lxml>=5.0.0
```

---

### Requests vs Alternatives

**Chosen**: Requests (already in project)

**Alternatives Considered**:

1. **urllib (stdlib)**
   - **Pros**: No dependency
   - **Cons**: More verbose, less convenient
   - **Decision**: Requests already used, no reason to change

2. **httpx**
   - **Pros**: Modern, async support, HTTP/2
   - **Cons**: Not needed for this use case, added dependency
   - **Decision**: Overkill

3. **aiohttp**
   - **Pros**: Async HTTP client
   - **Cons**: Async not needed for sequential scraping
   - **Decision**: Not needed

**Final Decision**: Continue using Requests
- Already in project dependencies
- Simple, well-documented
- Sufficient for synchronous scraping
- Session support for connection pooling

---

## Testing Strategy

### Unit Tests with Mocked HTML

**Approach**: Create HTML fixtures for testing without hitting live site

**Fixture Structure**:
```
tests/fixtures/usccb_html/
├── weekday_3_readings.html
├── sunday_4_readings.html
├── christmas_day_hub.html
├── christmas_day_mass.html
├── malformed_no_title.html
└── malformed_no_readings.html
```

**Mocking Strategy**:
```python
import pytest
from unittest.mock import Mock, patch
from pathlib import Path

@pytest.fixture
def weekday_html():
    """Load weekday HTML fixture."""
    fixture_path = Path(__file__).parent / 'fixtures' / 'usccb_html' / 'weekday_3_readings.html'
    return fixture_path.read_text()

@patch('requests.Session.get')
def test_scrape_weekday(mock_get, weekday_html):
    """Test scraping a weekday with 3 readings."""
    mock_response = Mock()
    mock_response.content = weekday_html
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    scraper = USCCBReadingsScraper()
    reading = scraper.get_readings_for_date(date(2025, 11, 22))
    
    assert reading.liturgical_day == "Saturday of the Thirty-Third Week in Ordinary Time"
    assert len(reading.readings) == 3
```

**Coverage Goal**: 90%+ with mocked tests

---

### Integration Tests Against Live Site

**Approach**: Test against real USCCB site, but carefully

**Considerations**:
- **Rate Limiting**: No more than 1 request per second
- **Test Selection**: Only 3-5 sample dates, not exhaustive
- **Marking**: Mark tests as `@pytest.mark.slow` and `@pytest.mark.integration`
- **Skipping**: Allow skipping with `--skip-integration` flag
- **CI/CD**: Run sparingly (not on every commit)

**Sample Dates**:
```python
INTEGRATION_TEST_DATES = [
    (date(2025, 11, 22), "Saturday of the Thirty-Third Week in Ordinary Time", 3),  # Weekday
    (date(2025, 11, 24), "Our Lord Jesus Christ, King of the Universe", 4),  # Sunday
    (date(2025, 12, 25), "The Nativity of the Lord (Christmas)", 4),  # Feast with multiple Masses
]

@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.parametrize("test_date,expected_day,expected_count", INTEGRATION_TEST_DATES)
def test_live_usccb_scraping(test_date, expected_day, expected_count):
    """Test scraping real USCCB pages."""
    scraper = USCCBReadingsScraper()
    reading = scraper.get_readings_for_date(test_date)
    
    assert expected_day in reading.liturgical_day
    assert len(reading.readings) == expected_count
    
    # Rate limit: wait 1 second between tests
    time.sleep(1)
```

**CI/CD Strategy**:
- Run integration tests only on PR merges (not every commit)
- Schedule weekly integration test runs to detect USCCB changes
- If integration tests fail, notify maintainers (potential structure change)

---

### E2E Tests for CLI

**Approach**: Test complete CLI workflows with real file system

**Pattern**:
```python
def test_generate_readings_command(tmp_path, monkeypatch):
    """Test generate-readings CLI command."""
    # Change to temp directory
    monkeypatch.chdir(tmp_path)
    
    # Create readings directory
    (tmp_path / 'readings').mkdir()
    
    # Run CLI command
    result = subprocess.run(
        ['catholic-liturgy', 'generate-readings', '--date', '2025-11-22'],
        capture_output=True,
        text=True
    )
    
    # Verify success
    assert result.returncode == 0
    assert "Saturday of the Thirty-Third Week" in result.stdout
    
    # Verify file created
    html_file = tmp_path / 'readings' / '2025-11-22.html'
    assert html_file.exists()
    
    # Verify HTML content
    html_content = html_file.read_text()
    assert "<!DOCTYPE html>" in html_content
    assert "Saturday of the Thirty-Third Week" in html_content
```

---

## HTML Validation

### Validation Tools

**W3C HTML Validator**: Use for spot-checking generated HTML

**Automated Validation** (optional):
```python
# Could add to tests if needed
from html5validator import Validator

def test_generated_html_is_valid():
    """Verify generated HTML is valid HTML5."""
    # Generate sample HTML
    html_content = generate_readings_html(sample_reading)
    
    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(html_content)
        temp_path = f.name
    
    try:
        # Validate
        validator = Validator()
        result = validator.validate([temp_path])
        assert result == 0, "HTML validation failed"
    finally:
        os.unlink(temp_path)
```

**Decision**: Manual spot-checking initially, add automated validation if issues arise.

---

## Performance Profiling

### Profiling Strategy

**Tool**: Python's built-in `cProfile` and `time` module

**Key Measurements**:
```python
import time
import logging

def profile_operation(operation_name):
    """Decorator to profile operation timing."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start
            logging.info(f"{operation_name} completed in {duration:.2f}s")
            return result
        return wrapper
    return decorator

@profile_operation("USCCB page fetch")
def _fetch_page(self, url):
    # ... implementation
```

**Benchmarking**:
```bash
# Profile a complete workflow
time catholic-liturgy generate-readings --date 2025-11-22

# Profile with Python
python -m cProfile -s cumulative -m catholic_liturgy_tools.cli generate-readings --date 2025-11-22
```

**Targets** (from plan.md):
- Fetch: < 3s
- Parse: < 1s
- Generate HTML: < 1s
- Write file: < 0.5s
- Total: < 5s

**Decision**: Add timing logs to key functions. If performance issues arise, profile and optimize.

---

## Logging Strategy

### Log Levels

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Usage
logger.debug("Parsing HTML structure...")
logger.info(f"Fetching readings for {date}")
logger.warning("Using fallback method for liturgical day name")
logger.error(f"Failed to fetch page: {error}")
logger.critical(f"Unexpected error: {error}")
```

**Guidelines**:
- **DEBUG**: Detailed parsing steps, HTML structure details
- **INFO**: High-level operations (fetching, generating, success messages)
- **WARNING**: Fallback methods used, retries, non-critical issues
- **ERROR**: Failures that prevent completion but can be retried
- **CRITICAL**: Unrecoverable errors, system failures

**User vs Developer Logs**:
- CLI output: User-friendly messages (success, progress)
- Log file: Developer-oriented details (for debugging)

---

## Security Considerations

### Input Validation

**Date Parameter**:
```python
def validate_date(date_str: str) -> date:
    """Validate and parse date string."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise DateError(f"Invalid date format: {date_str}. Expected YYYY-MM-DD")
```

**HTML Sanitization**:
```python
import html

def sanitize_text(text: str) -> str:
    """Escape HTML special characters."""
    return html.escape(text, quote=True)
```

**URL Building**:
```python
def build_url(date: date) -> str:
    """Build USCCB URL for date."""
    # Use strftime to ensure proper formatting
    date_str = date.strftime("%m%d%y")
    # Use string formatting (not f-string with user input)
    return f"https://bible.usccb.org/bible/readings/{date_str}.cfm"
```

### Secrets Management

**GitHub Token**: Already handled in spec 001 with dotenv

**No Additional Secrets Needed**: USCCB scraping is public, no authentication required

---

## Browser Compatibility Testing

### Target Browsers

- Chrome/Chromium (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

### Testing Approach

**Manual Testing**:
1. Generate sample readings HTML
2. Open in each browser
3. Verify layout, fonts, colors
4. Test responsive behavior (resize window)
5. Test navigation links

**Automated Testing** (optional, future):
- Consider Playwright or Selenium for automated browser testing
- Not critical for initial version

**Decision**: Manual testing sufficient for initial release. Add automated tests if browser issues arise.

---

## Accessibility Considerations

**Current Status**: Basic accessibility (semantic HTML, alt text if images added)

**Future Enhancements** (out of scope):
- ARIA labels for screen readers
- Keyboard navigation testing
- Color contrast validation (WCAG AA)
- Font size adjustments
- High contrast mode support

**Decision**: Start simple, improve accessibility in future iterations based on user feedback.

---

## Internationalization (i18n)

**Current Status**: English only (USCCB default language)

**Future Considerations** (out of scope):
- Spanish readings (USCCB has `/es/` URLs)
- Multiple Bible translations (NAB, RSV, KJV)
- UI text translations

**Decision**: English only for initial release. USCCB supports Spanish, so future enhancement is feasible.

---

## Caching Strategy

**Current Status**: No caching

**Future Considerations**:
- Cache fetched readings to avoid re-scraping
- SQLite database for local cache
- Cache invalidation strategy (time-based or manual)

**Rationale for No Caching Initially**:
- Simplicity: No additional complexity
- Freshness: Always get latest data from USCCB
- Low frequency: Daily workflow, not high-volume
- Storage: Minimal disk usage without cache

**Decision**: No caching for initial release. Add if performance or rate-limiting becomes an issue.

---

## Alternative Approaches Considered

### 1. Using Official USCCB API

**Research**: USCCB does not provide an official public API for readings

**Alternative**: Scraping is the only option

**Decision**: Proceed with web scraping, document respectful usage

---

### 2. Pre-fetching Future Readings

**Idea**: Fetch multiple days/weeks of readings at once

**Pros**: Faster bulk generation, less frequent requests

**Cons**: More complex, requires storage/cache, may not be used

**Decision**: Generate on-demand (daily workflow). Consider for future optimization if needed.

---

### 3. Generating Markdown Instead of HTML

**Idea**: Generate readings as markdown (like messages), let Jekyll render

**Pros**: Consistent with messages, simpler generation

**Cons**: Markdown lacks semantic structure for readings, harder to style distinctly

**Decision**: Generate HTML for readings (separate from messages), allows better control over formatting and styling

---

### 4. Using Database for Readings Storage

**Idea**: Store readings in SQLite database instead of HTML files

**Pros**: Query capabilities, relational data, versioning

**Cons**: Added complexity, not needed for static site, harder to version control

**Decision**: Use file-based storage (HTML files) for simplicity and Git-friendly approach

---

## Open Questions & Future Research

### 1. USCCB Terms of Service

**Question**: Does USCCB allow scraping? Any usage restrictions?

**Action**: Review USCCB terms of service and robots.txt

**Status**: Assumed educational/personal use is acceptable. Include attribution and polite scraping.

---

### 2. Liturgical Calendar Integration

**Question**: Should we integrate liturgical calendar data (colors, seasons)?

**Status**: Out of scope for this spec. Consider for future enhancement (spec 003?)

---

### 3. Audio Readings

**Question**: USCCB may have audio readings. Should we link to them?

**Status**: Out of scope. Consider for future enhancement.

---

### 4. Alternative Bible Translations

**Question**: Should we support multiple translations (NAB, RSV, KJV)?

**Status**: Out of scope. USCCB uses NAB (New American Bible). Other translations would require different sources.

---

### 5. Historical Readings Archive

**Question**: How far back should we support fetching readings?

**Status**: USCCB URL pattern works for any date. Support any date user requests. No artificial limits.

---

## Lessons from Try1 Repo

**What Worked Well** (keep):
- Retry logic with exponential backoff
- Multiple Mass detection for feast days
- HTML fixture approach for testing
- Clear exception hierarchy

**What to Improve**:
- Add comprehensive docstrings with type hints
- Increase test coverage (try1 may have been lower)
- Better error messages for users (not just developers)
- Validate extracted data before returning
- Add integration tests (not just unit tests)

---

## Documentation Requirements

**README.md Updates**:
- Add `generate-readings` command with examples
- Document USCCB as data source with attribution
- Add troubleshooting section for scraping issues
- Update workflow description

**research.md** (this file):
- HTML structure analysis (complete)
- Technical decisions (complete)
- Testing strategy (complete)

**contracts/cli-commands.md**:
- `generate-readings` command specification
- Parameters, options, output format
- Error codes and messages

**contracts/html-format.md**:
- HTML structure specification
- CSS styles documentation
- Navigation and links

---

## Risk Mitigation Checklist

- ✅ **USCCB Structure Changes**: HTML fixtures + integration tests
- ✅ **Network Failures**: Retry logic + exponential backoff
- ✅ **Rate Limiting**: Polite User-Agent + rate limiting in tests
- ✅ **Data Validation**: Comprehensive validation functions
- ✅ **HTML Generation**: Unit tests + HTML validation
- ✅ **Browser Compatibility**: Manual testing across browsers
- ✅ **Performance**: Profiling + timing logs
- ✅ **Security**: Input validation + HTML escaping

---

## Next Steps

1. ✅ **Research Complete**: This document captures all technical decisions
2. **Create Contracts**: Document CLI commands and HTML format in `contracts/`
3. **Begin Implementation**: Start Phase 2 (Scraper) with TDD approach
4. **Iterate**: Follow plan.md phases with testing at each step
5. **Review**: Conduct review after implementation to capture lessons learned

---

**Document Status**: Complete - ready for Phase 1 (Design & Contracts)
