# Data Model

**Feature**: Daily Readings from Catholic Lectionary  
**Branch**: 002-daily-readings  
**Phase**: 1 (Design & Contracts)  
**Date**: 2025-11-22

## Purpose

This document defines the core entities, their attributes, relationships, and validation rules for the Daily Readings feature. It extends the existing data model from spec 001-github-pages to include readings data and updated index page structure.

---

## Entities

### 1. Daily Reading

A Daily Reading represents the complete set of Scripture readings from the Catholic Lectionary for a specific liturgical date, fetched from USCCB.org.

**Attributes**:
- `date`: ISO 8601 date string (YYYY-MM-DD format)
  - Required: Yes
  - Validation: Must be valid date, format YYYY-MM-DD
  - Example: `"2025-11-22"`
  
- `date_display`: Human-readable date string
  - Required: Yes
  - Format: "Month DD, YYYY"
  - Example: `"November 22, 2025"`
  - Derived from: `date` attribute
  
- `liturgical_day`: Name of the liturgical day
  - Required: Yes
  - Validation: Non-empty string
  - Example: `"Saturday of the Thirty-Third Week in Ordinary Time"`
  - Source: Extracted from USCCB page title or H1 heading
  
- `readings`: List of ReadingEntry objects
  - Required: Yes (must have at least 1 reading)
  - Type: List[ReadingEntry]
  - Order: Maintained as returned by USCCB (First, Psalm, Second if present, Gospel)
  - Validation: At least 1 entry, typically 3-4 entries
  
- `source_url`: URL where readings were fetched
  - Required: Yes
  - Format: `https://bible.usccb.org/bible/readings/{MMDDYY}.cfm`
  - Example: `"https://bible.usccb.org/bible/readings/112225.cfm"`
  - Purpose: Attribution and debugging
  
- `filename`: Derived attribute for HTML file
  - Format: `{date}.html`
  - Example: `"2025-11-22.html"`
  
- `file_path`: Derived attribute for full file path
  - Format: `readings/{filename}`
  - Example: `"readings/2025-11-22.html"`

**Validation Rules**:
1. Date must be parseable as YYYY-MM-DD
2. Liturgical day must be non-empty string
3. Readings list must contain at least 1 ReadingEntry
4. Source URL must be valid USCCB readings URL
5. All ReadingEntry objects must pass their validation

**State Transitions**:
- Fetched: Raw data retrieved from USCCB
- Parsed: Data extracted and validated into DailyReading object
- Generated: HTML file created from DailyReading data
- Published: HTML file committed and deployed to GitHub Pages

**Relationships**:
- One DailyReading per date (unique by date)
- One DailyReading contains 3-4 ReadingEntry objects
- Many DailyReadings are linked by one Index Page

**Python Representation**:
```python
from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class DailyReading:
    date: str  # YYYY-MM-DD
    date_display: str  # "Month DD, YYYY"
    liturgical_day: str
    readings: List['ReadingEntry']
    source_url: str
    
    def validate(self) -> None:
        """Validate all attributes."""
        # Date validation
        datetime.strptime(self.date, "%Y-%m-%d")
        
        # Content validation
        if not self.liturgical_day.strip():
            raise ValueError("Liturgical day cannot be empty")
        
        if not self.readings:
            raise ValueError("Must have at least one reading")
        
        # Validate all readings
        for reading in self.readings:
            reading.validate()
    
    @property
    def filename(self) -> str:
        return f"{self.date}.html"
    
    @property
    def file_path(self) -> str:
        return f"readings/{self.filename}"
```

---

### 2. Reading Entry

A ReadingEntry represents a single Scripture reading component (e.g., First Reading, Responsorial Psalm, Gospel) within a Daily Reading.

**Attributes**:
- `title`: Reading type/name
  - Required: Yes
  - Validation: Non-empty string
  - Examples: `"First Reading"`, `"Responsorial Psalm"`, `"Gospel"`
  - Note: May be combined with citation (e.g., "First Reading: Genesis 1:1-5")
  
- `citation`: Scripture reference
  - Required: Yes
  - Validation: Non-empty string
  - Examples: `"Luke 21:1-4"`, `"Psalm 119:1-8"`, `"1 Corinthians 15:1-11"`
  - Format: Varies based on Scripture book and passage
  
- `text`: Reading content
  - Required: Yes
  - Type: List[str] (list of paragraphs)
  - Validation: Must have at least 1 paragraph, each non-empty
  - Example: `["Jesus looked up and saw...", "He also saw a poor widow..."]`
  - Format: Plain text paragraphs without HTML tags
  
- `title_with_citation`: Derived display attribute
  - Format: `"{title}: {citation}"` if citation not in title, else just `title`
  - Example: `"First Reading: Genesis 1:1-5"`
  - Purpose: Consistent display formatting

**Validation Rules**:
1. Title must be non-empty string
2. Citation must be non-empty string
3. Text must be non-empty list
4. Each paragraph in text must be non-empty string
5. Text should be sanitized (no malicious HTML if any slips through)

**HTML Rendering**:
```html
<div class="reading-entry">
    <h2 class="reading-title">{title_with_citation}</h2>
    <div class="reading-text">
        <p>{paragraph1}</p>
        <p>{paragraph2}</p>
        ...
    </div>
</div>
```

**Python Representation**:
```python
from dataclasses import dataclass
from typing import List

@dataclass
class ReadingEntry:
    title: str
    citation: str
    text: List[str]  # List of paragraphs
    
    def validate(self) -> None:
        """Validate all attributes."""
        if not self.title.strip():
            raise ValueError("Reading title cannot be empty")
        
        if not self.citation.strip():
            raise ValueError("Reading citation cannot be empty")
        
        if not self.text:
            raise ValueError("Reading text cannot be empty")
        
        for i, paragraph in enumerate(self.text):
            if not paragraph.strip():
                raise ValueError(f"Paragraph {i} cannot be empty")
    
    @property
    def title_with_citation(self) -> str:
        """Get formatted title with citation."""
        if self.citation in self.title:
            return self.title
        return f"{self.title}: {self.citation}"
```

---

### 3. Index Page (Updated)

The Index Page entity is extended from spec 001 to include Daily Readings alongside Daily Messages.

**Attributes** (new/modified):
- `title`: Page title
  - Required: Yes
  - Value: `"Catholic Liturgy Tools"`
  
- `messages`: List of message entries
  - Required: Yes (can be empty list)
  - Type: List[MessageEntry]
  - Sorted: Reverse chronological order (newest first)
  
- `readings`: **NEW** List of readings entries
  - Required: Yes (can be empty list)
  - Type: List[ReadingsEntry]
  - Sorted: Reverse chronological order (newest first)
  
- `filename`: Fixed value
  - Value: `"index.md"` (changed from previous if needed)
  
- `file_path`: Root of repository
  - Value: `"index.md"`

**MessageEntry** (existing, from spec 001):
- `date`: Date of the message (YYYY-MM-DD)
- `title`: Display title (e.g., "Daily Message for 2025-11-22")
- `link`: Relative link to message file
  - Format: `_posts/{date}-daily-message.md`

**ReadingsEntry** (new):
- `date`: Date of the readings (YYYY-MM-DD)
- `liturgical_day`: Liturgical day name for display
- `title`: Display title combining date and liturgical day
  - Format: `"{date} - {liturgical_day}"`
  - Example: `"2025-11-22 - Saturday of the Thirty-Third Week in Ordinary Time"`
- `link`: Relative link to readings HTML file
  - Format: `readings/{date}.html`
  - Example: `"readings/2025-11-22.html"`

**File Representation** (Markdown):
```markdown
---
layout: page
title: "Catholic Liturgy Tools"
---

# Catholic Liturgy Tools

Welcome to Catholic Liturgy Tools, a resource for daily liturgical content.

## Daily Messages

- [Daily Message for 2025-11-22](_posts/2025-11-22-daily-message.md)
- [Daily Message for 2025-11-21](_posts/2025-11-21-daily-message.md)

## Daily Readings

- [2025-11-22 - Saturday of the Thirty-Third Week in Ordinary Time](readings/2025-11-22.html)
- [2025-11-21 - Friday of the Thirty-Third Week in Ordinary Time](readings/2025-11-21.html)
```

**Generation Logic**:
1. Scan `_posts/` directory for message markdown files
2. Scan `readings/` directory for readings HTML files
3. Extract date from filenames
4. For readings, parse HTML to extract liturgical day name (or read from metadata)
5. Sort both lists by date (newest first)
6. Generate markdown with two sections
7. Handle cases where one section may be empty

**Python Representation**:
```python
from dataclasses import dataclass
from typing import List
from pathlib import Path

@dataclass
class MessageEntry:
    date: str
    title: str
    link: str

@dataclass
class ReadingsEntry:
    date: str
    liturgical_day: str
    link: str
    
    @property
    def title(self) -> str:
        return f"{self.date} - {self.liturgical_day}"

@dataclass
class IndexPage:
    title: str
    messages: List[MessageEntry]
    readings: List[ReadingsEntry]
    
    def validate(self) -> None:
        """Validate index page data."""
        if not self.title.strip():
            raise ValueError("Index title cannot be empty")
        
        # Validate messages are sorted
        dates = [m.date for m in self.messages]
        if dates != sorted(dates, reverse=True):
            raise ValueError("Messages must be sorted newest first")
        
        # Validate readings are sorted
        dates = [r.date for r in self.readings]
        if dates != sorted(dates, reverse=True):
            raise ValueError("Readings must be sorted newest first")
    
    @property
    def filename(self) -> str:
        return "index.md"
    
    @property
    def file_path(self) -> Path:
        return Path("index.md")
```

---

### 4. Scraper Configuration

Configuration entity for USCCB scraper behavior.

**Attributes**:
- `base_url`: Base URL for USCCB site
  - Value: `"https://bible.usccb.org"`
  - Immutable: Yes
  
- `timeout`: HTTP request timeout in seconds
  - Default: `30`
  - Range: 10-60 seconds
  - Purpose: Prevent hanging requests
  
- `max_retries`: Maximum retry attempts on failure
  - Default: `3`
  - Range: 1-5
  - Purpose: Reliability against transient failures
  
- `backoff_factor`: Exponential backoff multiplier
  - Default: `2.0`
  - Range: 1.5-3.0
  - Purpose: Polite retry behavior
  
- `user_agent`: HTTP User-Agent header
  - Required: Yes
  - Format: `"Catholic Liturgy Tools/{version} (Educational Purpose)"`
  - Example: `"Catholic Liturgy Tools/0.2.0 (Educational Purpose)"`
  - Purpose: Identify the tool to USCCB servers

**Python Representation**:
```python
from dataclasses import dataclass

@dataclass
class ScraperConfig:
    base_url: str = "https://bible.usccb.org"
    timeout: int = 30
    max_retries: int = 3
    backoff_factor: float = 2.0
    user_agent: str = "Catholic Liturgy Tools/0.2.0 (Educational Purpose)"
    
    def validate(self) -> None:
        """Validate configuration."""
        if self.timeout < 10 or self.timeout > 60:
            raise ValueError("Timeout must be between 10 and 60 seconds")
        
        if self.max_retries < 1 or self.max_retries > 5:
            raise ValueError("Max retries must be between 1 and 5")
        
        if self.backoff_factor < 1.5 or self.backoff_factor > 3.0:
            raise ValueError("Backoff factor must be between 1.5 and 3.0")
```

---

## Entity Relationships

```
┌─────────────────┐
│   Index Page    │
│   (index.md)    │
└────────┬────────┘
         │ links to
    ┌────┴──────┐
    │           │
    ▼           ▼
┌────────┐  ┌──────────────┐
│ Daily  │  │Daily Reading │
│Message │  │   (HTML)     │
└────────┘  └──────┬───────┘
               1    │ contains
                    │ 3-4
                    ▼
            ┌───────────────┐
            │ ReadingEntry  │
            │               │
            └───────────────┘
```

**Relationships**:
1. One Index Page links to many Daily Messages (1:N)
2. One Index Page links to many Daily Readings (1:N)
3. One Daily Reading contains 3-4 Reading Entries (1:N)
4. Daily Messages and Daily Readings are independent (no direct relationship)
5. Both Messages and Readings share the same date space but are stored separately

---

## File Storage Structure

```
repository_root/
├── index.md                    # Index Page entity
├── _posts/                     # Daily Messages (from spec 001)
│   ├── 2025-11-22-daily-message.md
│   ├── 2025-11-21-daily-message.md
│   └── ...
└── readings/                   # Daily Readings (new)
    ├── 2025-11-22.html
    ├── 2025-11-21.html
    └── ...
```

**Design Decisions**:
- Separate directories prevent filename conflicts
- HTML files in `readings/` directory (not `_posts/`) because they are standalone HTML, not Jekyll posts
- Index.md at root for clean URLs (no `/index.html` needed)
- Date-based filenames enable easy sorting and scanning

---

## Data Flow

```
1. USCCB Website (Source)
   ↓ HTTP GET request
2. Raw HTML
   ↓ BeautifulSoup parsing
3. DailyReading object (with ReadingEntry list)
   ↓ Validation
4. Validated DailyReading
   ↓ HTML generation
5. HTML file (readings/{date}.html)
   ↓ File system write
6. Persistent storage
   ↓ Index scanning
7. ReadingsEntry in IndexPage
   ↓ Markdown generation
8. Updated index.md
   ↓ Git commit + push
9. GitHub Pages deployment
   ↓ Jekyll rendering
10. Live website
```

---

## Error States

**Scraping Errors**:
- `NetworkError`: Connection failure, timeout, HTTP error
- `ParseError`: HTML structure unexpected, missing required elements
- `ValidationError`: Extracted data fails validation rules
- `DateError`: Invalid or malformed date input

**Generation Errors**:
- `FileSystemError`: Cannot create directory or write file
- `TemplateError`: HTML template rendering fails
- `EncodingError`: Text encoding issues

**Index Errors**:
- `ScanError`: Cannot read directory or files
- `SortError`: Date parsing fails during sorting
- `EmptyIndexError`: No content found in either messages or readings directories

---

## Validation Examples

**Valid DailyReading**:
```python
reading = DailyReading(
    date="2025-11-22",
    date_display="November 22, 2025",
    liturgical_day="Saturday of the Thirty-Third Week in Ordinary Time",
    readings=[
        ReadingEntry(
            title="First Reading",
            citation="1 Maccabees 6:1-13",
            text=["King Antiochus was traversing...", "He was seized with great grief..."]
        ),
        ReadingEntry(
            title="Responsorial Psalm",
            citation="Psalm 9:2-3, 4, 6, 16, 19",
            text=["I will give thanks to you...", "Because you have upheld my right..."]
        ),
        ReadingEntry(
            title="Gospel",
            citation="Luke 20:27-40",
            text=["Some Sadducees, those who deny...", "Jesus said to them..."]
        )
    ],
    source_url="https://bible.usccb.org/bible/readings/112225.cfm"
)
reading.validate()  # Should pass
```

**Invalid DailyReading** (missing readings):
```python
reading = DailyReading(
    date="2025-11-22",
    date_display="November 22, 2025",
    liturgical_day="Saturday of the Thirty-Third Week in Ordinary Time",
    readings=[],  # Empty!
    source_url="https://bible.usccb.org/bible/readings/112225.cfm"
)
reading.validate()  # Raises ValueError: Must have at least one reading
```

---

## Migration from Existing System

Since this is a new feature, no data migration is needed. However:

1. **Index Page Update**: The existing `index.md` will be regenerated with new structure
2. **Workflow Compatibility**: Existing daily message workflow continues to work unchanged
3. **Backward Compatibility**: Old index.md format will be replaced, but old message files remain valid
4. **Gradual Rollout**: Readings can be added without affecting existing messages

---

## Performance Considerations

**Storage**:
- Each HTML file: ~10-30 KB (estimated based on text content)
- 365 readings/year: ~3.6-11 MB/year
- 10 years: ~36-110 MB (well within GitHub Pages limits)

**Fetch Time**:
- Single USCCB page fetch: ~1-3 seconds (network dependent)
- Parsing: <1 second
- HTML generation: <1 second
- Total per day: ~2-5 seconds

**Index Generation**:
- Scanning directories: <1 second for 1000 files
- Sorting: <1 second
- Markdown generation: <1 second
- Total: <3 seconds even with years of content

---

## Future Data Model Extensions

**Possible future entities** (out of scope for this spec):
- `SaintOfTheDay`: Daily saint biography and feast information
- `LiturgicalColor`: Color of the day with explanation
- `SearchIndex`: Full-text search index of readings
- `UserPreferences`: User customization settings
- `ReadingAudio`: Audio file links for readings
- `Translation`: Alternative Bible translations (NAB, RSV, KJV)

These would require new specifications and data model documentation.
