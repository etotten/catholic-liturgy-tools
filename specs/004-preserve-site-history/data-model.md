# Data Model: Preserve Site Historical Content

**Feature**: 004-preserve-site-history  
**Date**: 2025-11-30  
**Phase**: 1 - Design & Contracts

## Entities

### ContentFile

**Description**: Represents a single generated content file (message or reading) in the _site/ directory

**Attributes**:
- `path`: Absolute file path (e.g., `_site/messages/2025-11-23-daily-message.md`)
- `date`: Date string in YYYY-MM-DD format extracted from filename
- `content_type`: Type of content ("message" or "reading")
- `exists`: Boolean indicating if file currently exists on filesystem

**Relationships**:
- Part of HistoricalContentArchive
- Referenced by IndexEntry

**Validation Rules**:
- Filename must follow patterns: `YYYY-MM-DD-daily-message.md` OR `YYYY-MM-DD.html`
- Date must be valid calendar date
- File must be within `_site/messages/` or `_site/readings/` directories

**State Transitions**:
- `new` → `generated` → `committed` → `deployed`
- Can transition back to `generated` state if regenerated (overwrite)

### IndexEntry

**Description**: Represents a single link entry in the index page pointing to content

**Attributes**:
- `date`: Date of the content (YYYY-MM-DD format)
- `display_text`: Text shown to user (e.g., "2025-11-23" for messages, "2025-11-23 - First Sunday of Advent" for readings)
- `relative_link`: Relative URL path (e.g., `messages/2025-11-23-daily-message.md`)
- `content_type`: Type ("message" or "reading")

**Relationships**:
- References ContentFile
- Part of IndexPage
- Sorted within ContentSection

**Validation Rules**:
- Link must point to existing ContentFile
- Date must match referenced ContentFile date
- Display text must be non-empty

### IndexPage

**Description**: The complete index.html page listing all historical content

**Attributes**:
- `path`: File path (`_site/index.html`)
- `title`: Page title ("Catholic Liturgy Tools")
- `sections`: List of ContentSection objects (messages section, readings section)
- `generation_timestamp`: When index was last generated

**Relationships**:
- Contains multiple ContentSection objects
- References all ContentFile objects via IndexEntry

**Validation Rules**:
- Must contain at least two sections (messages, readings)
- All links must resolve to existing files
- Sections must maintain reverse chronological order

### ContentSection

**Description**: A section within the index page grouping one type of content

**Attributes**:
- `title`: Section heading ("Daily Messages" or "Daily Readings")
- `entries`: Ordered list of IndexEntry objects
- `content_type`: Type of content in section ("message" or "reading")

**Relationships**:
- Part of IndexPage
- Contains multiple IndexEntry objects

**Validation Rules**:
- Entries must be sorted reverse chronologically (newest first)
- All entries must have matching content_type
- Entry dates must be unique within section

### HistoricalContentArchive

**Description**: The complete collection of all generated content files accumulated over time

**Attributes**:
- `root_path`: Base directory path (`_site/`)
- `message_files`: List of ContentFile objects for messages
- `reading_files`: List of ContentFile objects for readings
- `total_count`: Total number of content files
- `date_range`: Tuple of (earliest_date, latest_date)

**Relationships**:
- Contains all ContentFile objects
- Represented in Git repository history

**Validation Rules**:
- Root path must exist
- Message files must be in `_site/messages/` subdirectory
- Reading files must be in `_site/readings/` subdirectory
- No duplicate dates within same content type

**State Transitions**:
- Grows monotonically (files added, never removed by automation)
- Individual files may be overwritten (same date regeneration)

### ContentGenerationRun

**Description**: A single execution of the content generation workflow

**Attributes**:
- `date`: Date for which content is being generated
- `generated_files`: List of ContentFile objects created/updated in this run
- `git_commit_sha`: SHA of commit storing this run's changes
- `status`: Status of run ("in_progress", "completed", "failed")

**Relationships**:
- Creates/updates ContentFile objects
- Triggers IndexPage regeneration
- Results in Git commit

**Validation Rules**:
- Date must be valid
- Must generate at least one file (message or reading)
- Must regenerate index page if content was generated

**State Transitions**:
1. `initiated` - Workflow triggered
2. `generating_content` - Creating message/reading files
3. `generating_index` - Updating index page
4. `committing` - Adding changes to Git
5. `deploying` - Pushing to gh-pages
6. `completed` - All steps successful

### PublishingWorkflow

**Description**: The GitHub Actions workflow that generates, commits, and deploys content

**Attributes**:
- `workflow_run_id`: GitHub Actions run identifier
- `trigger_event`: What triggered the workflow ("schedule", "workflow_dispatch", "push")
- `generation_runs`: List of ContentGenerationRun objects executed
- `commit_sha_before`: Git SHA before workflow started
- `commit_sha_after`: Git SHA after workflow completed

**Relationships**:
- Executes one or more ContentGenerationRun objects
- Modifies HistoricalContentArchive
- Updates IndexPage
- Creates Git commits

**Validation Rules**:
- Must commit generated content before deploying
- Must deploy all files from _site/ directory (not just new ones)
- Must not delete existing content files

## Entity Relationships Diagram

```
HistoricalContentArchive
  ├─ message_files: List[ContentFile]
  └─ reading_files: List[ContentFile]
       │
       │ referenced by
       ↓
IndexPage
  ├─ ContentSection (messages)
  │    └─ List[IndexEntry] ──references──> ContentFile
  └─ ContentSection (readings)
       └─ List[IndexEntry] ──references──> ContentFile

PublishingWorkflow
  └─ ContentGenerationRun
       ├─ generates──> ContentFile
       ├─ triggers──> IndexPage regeneration
       └─ creates──> Git commit
```

## Data Flow

1. **Content Generation**:
   ```
   PublishingWorkflow triggers
   → ContentGenerationRun initiated for date
   → Generate message ContentFile (if applicable)
   → Generate reading ContentFile (if applicable)
   → Scan HistoricalContentArchive to discover all files
   → Regenerate IndexPage with all IndexEntry objects
   → Commit ContentFiles + IndexPage to Git
   → Deploy HistoricalContentArchive to gh-pages
   ```

2. **File Discovery (Index Generation)**:
   ```
   Scan _site/messages/ directory
   → Discover all ContentFile objects (messages)
   → Extract date from each filename
   → Create IndexEntry for each message
   
   Scan _site/readings/ directory  
   → Discover all ContentFile objects (readings)
   → Extract date + liturgical day from each file
   → Create IndexEntry for each reading
   
   Group entries into ContentSection objects
   → Sort each section reverse chronologically
   → Build complete IndexPage HTML
   ```

3. **Same-Date Regeneration (Overwrite)**:
   ```
   ContentGenerationRun for existing date
   → Check if ContentFile exists for date
   → Overwrite existing file (no version, no skip)
   → Previous version preserved in Git history
   → Regenerate IndexPage (entry already exists, no duplicate)
   → Commit overwrites previous file
   → Deploy updated archive
   ```

## Invariants

1. **Accumulation**: `len(HistoricalContentArchive.message_files)` never decreases between workflow runs (except for same-date overwrites)
2. **Consistency**: Every `IndexEntry` in `IndexPage` must reference an existing `ContentFile`
3. **Ordering**: Within each `ContentSection`, entries are sorted reverse chronologically
4. **Uniqueness**: No duplicate dates within a `ContentSection`
5. **Persistence**: All `ContentFile` objects must be tracked in Git repository
6. **Completeness**: `IndexPage` must list all `ContentFile` objects in `HistoricalContentArchive`

## Storage

**Filesystem Structure**:
```
_site/
├── index.html                        # IndexPage
├── messages/
│   ├── 2025-11-01-daily-message.md  # ContentFile (message)
│   ├── 2025-11-02-daily-message.md
│   └── ...
└── readings/
    ├── 2025-11-01.html               # ContentFile (reading)
    ├── 2025-11-02.html
    └── ...
```

**Git Repository**:
- All ContentFile objects committed to main branch
- Each ContentGenerationRun creates a commit
- Git history preserves overwritten versions
- gh-pages branch receives deployed copy

## No Implementation Details

This data model describes **what** entities exist and their relationships, not **how** they are implemented in code. Implementation details (Python classes, database tables, API endpoints) are deferred to the tasks phase.
