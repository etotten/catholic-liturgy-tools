# Data Model: Daily Reflections with AI-Augmented Content

**Feature**: 005-daily-reflections  
**Date**: November 30, 2025  
**Purpose**: Define data structures for AI-augmented daily reflections

## Overview

This data model extends the existing `DailyReading` model to include AI-generated content (synopses, reflections), sourced prayers, and feast day information.

---

## Core Entities

### 1. ReadingSynopsis

Represents a one-line AI-generated synopsis for a single Scripture reading.

**Attributes**:
- `reading_title`: str - Title of the reading (e.g., "First Reading", "Gospel")
  - Required: Yes
  - Examples: "First Reading", "Responsorial Psalm", "Gospel"
- `synopsis_text`: str - One-line synopsis in plain language
  - Required: Yes
  - Validation: Non-empty, typically 10-25 words
  - Example: "God calls us to trust in His providence even in times of uncertainty."
- `tokens_used`: int - Number of AI tokens consumed generating this synopsis
  - Required: Yes
  - Used for: Cost tracking
  - Range: Typically 20-30 tokens output

**Relationships**:
- Belongs to one `DailyReading`
- Maps 1:1 with a `ReadingEntry` by `reading_title`

**Validation Rules**:
- Synopsis text must not be empty
- Synopsis should be concise (prefer <25 words)
- Must correspond to an existing reading in the daily readings

---

### 2. DailyReflection

Represents the unified reflection synthesizing all readings for a day, including pondering questions and CCC citations.

**Attributes**:
- `reflection_text`: str - Main reflection content (HTML formatted)
  - Required: Yes
  - Length: Typically 300-500 words
  - Format: May include paragraph breaks, emphasis
  - Example: "Today's readings invite us to consider..."
- `pondering_questions`: List[str] - Questions for personal meditation
  - Required: Yes
  - Count: 2-3 questions per FR-004
  - Validation: Each question non-empty, ends with "?"
  - Example: ["How does God's call challenge me today?", "Where do I need to trust more fully?"]
- `ccc_citations`: List[CCCCitation] - References to Catechism paragraphs
  - Required: Yes
  - Count: 1-2 citations per FR-005
  - Validation: Each citation has valid paragraph number
- `input_tokens`: int - AI input tokens for generation
  - Required: Yes
  - Used for: Cost tracking
- `output_tokens`: int - AI output tokens generated
  - Required: Yes
  - Used for: Cost tracking

**Relationships**:
- Belongs to one `DailyReading`
- Has many `CCCCitation` (1-2 typically)

**Validation Rules**:
- Must have at least 2 pondering questions
- Must have 1-2 CCC citations
- All CCC citations must pass validation (paragraph in range 1-2865)
- Reflection text must not be empty

---

### 3. CCCCitation

Represents a citation of the Catechism of the Catholic Church.

**Attributes**:
- `paragraph_number`: int - CCC paragraph number
  - Required: Yes
  - Validation: Must be 1 ≤ n ≤ 2865
  - Example: 2558
- `excerpt_text`: str - Brief quote or summary from the CCC paragraph
  - Required: Yes
  - Length: Typically 1-3 sentences
  - Example: "Prayer is the raising of one's mind and heart to God..."
- `context_note`: str - Optional brief note on relevance to readings
  - Required: No
  - Example: "This teaching connects to today's Gospel call to persistent prayer"

**Relationships**:
- Belongs to one `DailyReflection`

**Validation Rules**:
- Paragraph number must be validated (1-2865)
- Excerpt text must not be empty

---

### 4. SourcedPrayer

Represents a Catholic prayer sourced from an authoritative website, selected for the liturgical day.

**Attributes**:
- `prayer_title`: str - Title of the prayer
  - Required: Yes
  - Example: "Prayer of St. Francis", "Prayer before Mass"
- `prayer_text`: str - Full text of the prayer (HTML formatted)
  - Required: Yes
  - Format: May include line breaks, stanzas
  - Example: "Lord, make me an instrument of your peace..."
- `source_name`: str - Name of the source
  - Required: Yes
  - Values: One of "USCCB", "Vatican", "Catholic Online", "EWTN", "Loyola Press"
  - Example: "USCCB"
- `source_url`: str - URL to the prayer on the source website
  - Required: Yes
  - Validation: Valid HTTP(S) URL
  - Example: "https://www.usccb.org/prayers/prayer-st-francis"
- `selection_reason`: str - Why this prayer was chosen (liturgical context)
  - Required: Yes
  - Example: "Feast of St. Francis", "Theme of mercy in Gospel"
- `liturgical_context`: str - Liturgical season or feast day type
  - Required: No
  - Examples: "Advent", "Easter", "Memorial of Saint", "Ordinary Time"

**Relationships**:
- Belongs to one `DailyReading`

**Validation Rules**:
- Source name must be one of the approved five sources
- Source URL must be valid
- Prayer text must not be empty

---

### 5. FeastDayInfo

Represents information about a feast day, solemnity, or saint's day.

**Attributes**:
- `feast_type`: str - Type of celebration
  - Required: Yes
  - Values: "saint", "solemnity", "feast", "memorial", "optional_memorial"
  - Example: "saint"
- `feast_name`: str - Name of the feast or saint
  - Required: Yes
  - Example: "Memorial of Saint Cecilia, Virgin and Martyr"
- `is_saint`: bool - Whether this feast celebrates a saint
  - Required: Yes
  - Derived from: `feast_type == "saint"`
- `saint_bio`: Optional[SaintBiography] - Biography if saint's day
  - Required: Only if `is_saint == True`
  - Validation: Must be present for saint celebrations per FR-009

**Relationships**:
- Belongs to one `DailyReading`
- Has one optional `SaintBiography` (required if `is_saint`)

**Validation Rules**:
- If `is_saint` is True, `saint_bio` must be present
- Feast name must not be empty

---

### 6. SaintBiography

Represents biographical information about a saint being celebrated.

**Attributes**:
- `birth_date`: Optional[str] - Approximate birth date
  - Required: Yes (per FR-009)
  - Format: Year, or "circa YEAR", or range "YEAR-YEAR"
  - Example: "1200", "circa 300", "Unknown"
- `death_date`: Optional[str] - Date of death
  - Required: Yes (per FR-009)
  - Format: "Month DD, YEAR" or "YEAR" or "circa YEAR"
  - Example: "November 22, 230", "304"
- `geographic_locations`: List[str] - Key locations in saint's life
  - Required: Yes (per FR-009)
  - Count: Typically 1-3 locations
  - Example: ["Rome, Italy", "Sicily"]
- `canonization_reason`: str - Why the person became a saint
  - Required: Yes (per FR-009)
  - Description: Key deeds, virtues, or martyrdom
  - Example: "Martyred for refusing to renounce her Christian faith; patron saint of music"
- `more_info_url`: str - Link to Catholic source with more information
  - Required: Yes (per FR-009)
  - Validation: Valid HTTP(S) URL to Catholic source
  - Example: "https://www.catholic.org/saints/saint.php?saint_id=85"

**Relationships**:
- Belongs to one `FeastDayInfo`

**Validation Rules**:
- All fields required per FR-009
- More info URL must be valid and point to reputable Catholic source
- At least one geographic location required

---

### 7. ReflectionCostSummary

Tracks AI API costs for a single reflection generation.

**Attributes**:
- `date`: date - Date of the reflection
  - Required: Yes
- `total_input_tokens`: int - Total input tokens across all API calls
  - Required: Yes
  - Aggregates: Synopsis generation (per reading) + reflection generation
- `total_output_tokens`: int - Total output tokens generated
  - Required: Yes
  - Aggregates: All synopses + reflection content
- `total_cost_usd`: float - Total cost in US dollars
  - Required: Yes
  - Calculation: Based on Anthropic pricing (input + output)
  - Constraint: Must be ≤ $0.04 per FR-018
- `exceeded_budget`: bool - Whether cost exceeded $0.04 limit
  - Required: Yes
  - Derived from: `total_cost_usd > 0.04`
- `api_calls_count`: int - Number of API calls made
  - Required: Yes
  - Typically: 4-5 (one per reading + one for reflection)

**Relationships**:
- Belongs to one `DailyReading`

**Validation Rules**:
- Total cost should not exceed $0.04 (warning if exceeded)
- All token counts must be non-negative

---

## Extended Core Entity

### 8. DailyReading (Extended)

The existing `DailyReading` entity is extended with new attributes for reflection content.

**New Attributes** (in addition to existing):
- `synopses`: List[ReadingSynopsis] - AI-generated synopsis for each reading
  - Required: Yes for reflection-enabled readings
  - Count: Matches number of readings (typically 3-4)
- `reflection`: Optional[DailyReflection] - Unified daily reflection
  - Required: Yes for reflection-enabled readings
- `prayer`: Optional[SourcedPrayer] - Opening prayer for the day
  - Required: Yes for reflection-enabled readings (per FR-006)
- `feast_info`: Optional[FeastDayInfo] - Feast day information if applicable
  - Required: Only on feast days
- `cost_summary`: Optional[ReflectionCostSummary] - Cost tracking for this reflection
  - Required: Yes when AI content generated
- `generation_timestamp`: datetime - When reflection content was generated
  - Required: Yes for reflection-enabled readings
  - Format: ISO 8601 timestamp
- `ai_service_status`: str - Status of AI generation
  - Required: Yes
  - Values: "success", "partial", "failed"
  - "partial": Readings displayed but AI content unavailable
  - "failed": Generation attempted but failed

**Existing Attributes** (unchanged):
- `date`: date
- `date_display`: str
- `liturgical_day`: str
- `readings`: List[ReadingEntry]
- `source_url`: str

**Validation Rules**:
- If `ai_service_status == "success"`, all AI content fields must be present
- If `ai_service_status == "failed"`, AI content fields may be None
- Synopses count must match readings count when present

---

## Data Flow

```
1. Fetch readings from USCCB (existing)
   → DailyReading with readings list

2. Generate synopses (new)
   → For each reading → API call → ReadingSynopsis
   → Track tokens in ReflectionCostSummary

3. Check feast day (new)
   → Query liturgical calendar → FeastDayInfo
   → If saint → fetch SaintBiography

4. Select prayer (new)
   → Match liturgical context → SourcedPrayer

5. Generate reflection (new)
   → All readings + feast context → API call
   → DailyReflection with CCCCitations
   → Track tokens in ReflectionCostSummary

6. Validate costs
   → Check total_cost_usd ≤ $0.04
   → Set exceeded_budget flag

7. Generate HTML (modified)
   → Combine all components
   → Render with synopses, prayer, reflection, feast info
```

---

## Relationships Diagram

```
DailyReading
├── readings: List[ReadingEntry]           (existing)
├── synopses: List[ReadingSynopsis]        (new, 1 per reading)
├── reflection: DailyReflection            (new, 1)
│   └── ccc_citations: List[CCCCitation]  (new, 1-2)
├── prayer: SourcedPrayer                  (new, 1)
├── feast_info: FeastDayInfo               (new, 0-1)
│   └── saint_bio: SaintBiography         (new, 0-1)
└── cost_summary: ReflectionCostSummary   (new, 1)
```

---

## Implementation Notes

### Data Storage

- **Format**: Python dataclasses (using `@dataclass` decorator)
- **Serialization**: JSON for prayer database, cost logs
- **Persistence**: File-based (HTML output), no database required
- **Pattern**: Follows existing `scraper/models.py` structure

### Backward Compatibility

- Existing `DailyReading` structure remains unchanged
- New attributes are optional (support graceful degradation)
- Old readings without reflection content continue to work
- HTML generator checks for presence of reflection attributes

### Error Handling

- If AI generation fails, `ai_service_status = "failed"`
- Missing reflection content → display readings only
- Invalid CCC citations → retry or log warning
- Cost exceeded → log warning, continue (don't fail silently)

---

## Example Usage

```python
from datetime import date
from catholic_liturgy_tools.scraper.models import DailyReading
from catholic_liturgy_tools.ai.models import (
    ReadingSynopsis, DailyReflection, CCCCitation,
    SourcedPrayer, FeastDayInfo, ReflectionCostSummary
)

# Create synopses for each reading
synopsis1 = ReadingSynopsis(
    reading_title="First Reading",
    synopsis_text="God calls us to trust in His providence.",
    tokens_used=25
)

# Create CCC citations
ccc1 = CCCCitation(
    paragraph_number=2558,
    excerpt_text="Prayer is the raising of one's mind and heart to God.",
    context_note="Connects to Gospel's teaching on prayer"
)

# Create daily reflection
reflection = DailyReflection(
    reflection_text="<p>Today's readings invite us to...</p>",
    pondering_questions=[
        "How does God's call challenge me today?",
        "Where do I need to trust more fully?",
        "What does it mean to pray unceasingly?"
    ],
    ccc_citations=[ccc1],
    input_tokens=2800,
    output_tokens=450
)

# Create sourced prayer
prayer = SourcedPrayer(
    prayer_title="Prayer of St. Francis",
    prayer_text="Lord, make me an instrument of your peace...",
    source_name="USCCB",
    source_url="https://www.usccb.org/prayers/prayer-st-francis",
    selection_reason="Theme of peace in Gospel",
    liturgical_context="Ordinary Time"
)

# Track costs
cost_summary = ReflectionCostSummary(
    date=date(2025, 11, 30),
    total_input_tokens=2800,
    total_output_tokens=500,
    total_cost_usd=0.0159,
    exceeded_budget=False,
    api_calls_count=4
)

# Extend DailyReading
daily_reading.synopses = [synopsis1, ...]
daily_reading.reflection = reflection
daily_reading.prayer = prayer
daily_reading.cost_summary = cost_summary
daily_reading.generation_timestamp = datetime.now()
daily_reading.ai_service_status = "success"
```
