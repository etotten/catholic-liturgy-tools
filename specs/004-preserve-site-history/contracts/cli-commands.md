# CLI Commands Contract

**Feature**: 004-preserve-site-history  
**Date**: 2025-11-30

## Overview

This contract defines the expected behavior of CLI commands related to content preservation. The existing CLI commands remain unchanged in their interface, but their implementation behavior must ensure content accumulation.

## Existing Commands (Behavior Changes Only)

### `generate-message`

**No interface changes** - Command signature remains identical

**Behavior Requirements**:
- MUST NOT delete existing message files from other dates
- MUST preserve `_site/messages/` directory if it exists
- MUST create `_site/messages/` directory if it doesn't exist
- MUST overwrite file if generating for a date that already has a message
- MUST append to existing directory contents, not replace directory

**Before Fix** (Current Problematic Behavior):
```bash
# Day 1
$ catholic-liturgy generate-message --date 2025-11-23
# Creates: _site/messages/2025-11-23-daily-message.md

# Day 2
$ catholic-liturgy generate-message --date 2025-11-24
# Creates: _site/messages/2025-11-24-daily-message.md
# Problem: If _site/ was wiped, only 2025-11-24 exists
```

**After Fix** (Required Behavior):
```bash
# Day 1
$ catholic-liturgy generate-message --date 2025-11-23
# Creates: _site/messages/2025-11-23-daily-message.md
# (Git commit happens separately in workflow, not by CLI)

# Day 2
$ catholic-liturgy generate-message --date 2025-11-24
# Creates: _site/messages/2025-11-24-daily-message.md
# Result: Both 2025-11-23 AND 2025-11-24 exist (if _site/ preserved)
# (Git commit happens separately in workflow, not by CLI)
```

**Success Criteria**:
- Running command twice for different dates results in both files existing
- File count in `_site/messages/` increases with each new date
- Existing files remain untouched when generating for different dates

---

### `generate-readings`

**No interface changes** - Command signature remains identical

**Behavior Requirements**:
- MUST NOT delete existing readings files from other dates
- MUST preserve `_site/readings/` directory if it exists
- MUST create `_site/readings/` directory if it doesn't exist
- MUST overwrite file if generating for a date that already has readings
- MUST append to existing directory contents, not replace directory

**Before Fix** (Current Problematic Behavior):
```bash
# Day 1
$ catholic-liturgy generate-readings --date 2025-11-23
# Creates: _site/readings/2025-11-23.html

# Day 2  
$ catholic-liturgy generate-readings --date 2025-11-24
# Creates: _site/readings/2025-11-24.html
# Problem: If _site/ was wiped, only 2025-11-24 exists
```

**After Fix** (Required Behavior):
```bash
# Day 1
$ catholic-liturgy generate-readings --date 2025-11-23
# Creates: _site/readings/2025-11-23.html
# (Git commit happens separately in workflow, not by CLI)

# Day 2
$ catholic-liturgy generate-readings --date 2025-11-24
# Creates: _site/readings/2025-11-24.html
# Result: Both 2025-11-23 AND 2025-11-24 exist (if _site/ preserved)
# (Git commit happens separately in workflow, not by CLI)
```

**Success Criteria**:
- Running command twice for different dates results in both files existing
- File count in `_site/readings/` increases with each new date
- Existing files remain untouched when generating for different dates

---

### `generate-index`

**No interface changes** - Command signature remains identical

**Behavior Requirements**:
- MUST scan ALL files in `_site/messages/` directory (not just latest)
- MUST scan ALL files in `_site/readings/` directory (not just latest)
- MUST generate links to ALL discovered message files
- MUST generate links to ALL discovered readings files
- MUST order links reverse chronologically (newest first) in each section
- MUST verify discovered files exist before including in index
- MUST handle empty directories gracefully (generate index with empty sections)

**Before Fix** (Current Problematic Behavior):
```bash
# After generating content for 3 days
$ catholic-liturgy generate-index
# Problem: Only shows latest message and reading in index
```

**After Fix** (Required Behavior):
```bash
# After generating content for 3 days  
$ ls _site/messages/
2025-11-23-daily-message.md
2025-11-24-daily-message.md
2025-11-25-daily-message.md

$ catholic-liturgy generate-index
# Generates index.html with 3 message links (all dates)
# Links appear in order: 2025-11-25, 2025-11-24, 2025-11-23
```

**Success Criteria**:
- Index page contains same number of message links as files in `_site/messages/`
- Index page contains same number of readings links as files in `_site/readings/`
- Links are ordered newest to oldest in each section
- All links point to existing files
- Running command multiple times produces same result (idempotent)

**File Discovery Contract**:
```python
# Pseudo-contract for file discovery behavior
def scan_message_files(directory: str) -> List[Path]:
    """
    MUST:
    - Find ALL files matching pattern *-daily-message.md
    - Return complete list, not just one file
    - Sort reverse chronologically
    - Handle empty directory (return empty list)
    """

def scan_readings_files(directory: str) -> List[ReadingsEntry]:
    """
    MUST:
    - Find ALL files matching pattern YYYY-MM-DD.html
    - Extract date and liturgical day from each file
    - Return complete list, not just one file
    - Sort reverse chronologically
    - Handle empty directory (return empty list)
    """
```

---

## Testing Contracts

### Multi-Run Accumulation Test

**Test Purpose**: Verify content accumulates across multiple generation runs

**Test Steps**:
```bash
# Setup: Clean _site directory
rm -rf _site/

# Run 1: Generate for 2025-11-23
catholic-liturgy generate-message --date 2025-11-23
catholic-liturgy generate-readings --date 2025-11-23
catholic-liturgy generate-index

# Verify: 1 message, 1 reading, index with 1 link each
assert_file_exists _site/messages/2025-11-23-daily-message.md
assert_file_exists _site/readings/2025-11-23.html
assert_index_contains_date 2025-11-23

# Run 2: Generate for 2025-11-24
catholic-liturgy generate-message --date 2025-11-24
catholic-liturgy generate-readings --date 2025-11-24
catholic-liturgy generate-index

# Verify: 2 messages, 2 readings, index with 2 links each
assert_file_exists _site/messages/2025-11-23-daily-message.md  # Still exists
assert_file_exists _site/messages/2025-11-24-daily-message.md  # New file
assert_file_exists _site/readings/2025-11-23.html              # Still exists
assert_file_exists _site/readings/2025-11-24.html              # New file
assert_index_contains_dates 2025-11-23 2025-11-24
assert_index_order 2025-11-24 2025-11-23  # Newest first

# Run 3: Generate for 2025-11-25
catholic-liturgy generate-message --date 2025-11-25
catholic-liturgy generate-readings --date 2025-11-25
catholic-liturgy generate-index

# Verify: 3 messages, 3 readings, index with 3 links each
assert_file_count _site/messages/ 3
assert_file_count _site/readings/ 3
assert_index_contains_dates 2025-11-23 2025-11-24 2025-11-25
assert_index_order 2025-11-25 2025-11-24 2025-11-23  # Newest first
```

**Expected Result**: All generated files persist, index grows with each run

---

### Same-Date Regeneration Test

**Test Purpose**: Verify overwrite behavior for same-date regeneration

**Test Steps**:
```bash
# Generate initial content
catholic-liturgy generate-message --date 2025-11-23
initial_message=$(cat _site/messages/2025-11-23-daily-message.md)

catholic-liturgy generate-readings --date 2025-11-23
initial_readings=$(cat _site/readings/2025-11-23.html)

# Regenerate same date
catholic-liturgy generate-message --date 2025-11-23
catholic-liturgy generate-readings --date 2025-11-23
catholic-liturgy generate-index

# Verify: Files are overwritten (may differ if content changed)
assert_file_exists _site/messages/2025-11-23-daily-message.md
assert_file_exists _site/readings/2025-11-23.html
assert_file_count _site/messages/ 1  # Still only 1 file, not 2
assert_file_count _site/readings/ 1  # Still only 1 file, not 2

# Index should have exactly 1 entry per section, not duplicates
assert_index_contains_dates 2025-11-23
assert_no_duplicate_links_in_index
```

**Expected Result**: Files are overwritten, no duplicates created, index remains clean

---

### Empty Directory Test

**Test Purpose**: Verify graceful handling of empty directories

**Test Steps**:
```bash
# Setup: Ensure _site exists but is empty
mkdir -p _site/messages _site/readings
rm -f _site/messages/* _site/readings/*

# Generate index with no content
catholic-liturgy generate-index

# Verify: Index generated with empty sections, no errors
assert_file_exists _site/index.html
assert_index_has_section "Daily Messages"
assert_index_has_section "Daily Readings"
assert_index_message_count 0
assert_index_reading_count 0
assert_no_broken_links_in_index
```

**Expected Result**: Index page created successfully with empty sections, no errors

---

## Separation of Concerns: CLI vs Workflow

**IMPORTANT**: The CLI commands do **NOT** perform Git operations. They are pure content generators.

**CLI Responsibility**:
- Generate content files in `_site/` directory
- Preserve existing files (don't delete)
- Overwrite files if regenerating same date
- That's it - no Git commits, no pushes

**Workflow Responsibility**:
- Run CLI commands to generate content
- Commit `_site/` changes to repository
- Deploy to GitHub Pages

**Why This Separation?**
- Allows manual experimentation without commits
- CLI remains simple and focused
- User controls when/if to commit via Git
- Workflow automates the full pipeline

**Manual Usage Example**:
```bash
# Generate content locally for testing
$ catholic-liturgy generate-message --date 2025-11-23
$ catholic-liturgy generate-readings --date 2025-11-23
$ catholic-liturgy generate-index

# Review the generated files
$ open _site/index.html

# Commit manually only if satisfied
$ git add _site/
$ git commit -m "Generated content for 2025-11-23"
$ git push
```

## No New Commands Required

This feature requires **no new CLI commands**. All functionality is achieved by:
1. CLI commands generate files (no behavior change to existing commands)
2. GitHub Actions workflow commits generated content (new workflow step)

The CLI interface remains stable and backward-compatible.
