# CLI Commands Contract

**Feature**: Daily Readings from Catholic Lectionary  
**Branch**: 002-daily-readings  
**Phase**: 1 (Design & Contracts)  
**Date**: 2025-11-22

## Purpose

This document specifies the command-line interface contracts for the Daily Readings feature. It defines all commands, parameters, options, output formats, and error codes.

---

## Command: `generate-readings`

### Description

Fetches daily Catholic liturgical readings from USCCB.org and generates an HTML page for the specified date (or today by default).

### Syntax

```bash
catholic-liturgy generate-readings [OPTIONS]
```

### Options

| Option | Short | Type | Required | Default | Description |
|--------|-------|------|----------|---------|-------------|
| `--date` | `-d` | string | No | today | Date to generate readings for (YYYY-MM-DD format) |
| `--output-dir` | `-o` | string | No | `readings` | Output directory for HTML files |
| `--help` | `-h` | flag | No | N/A | Show help message and exit |

### Examples

**Generate readings for today**:
```bash
catholic-liturgy generate-readings
```

**Generate readings for specific date**:
```bash
catholic-liturgy generate-readings --date 2025-12-25
```

**Generate with custom output directory**:
```bash
catholic-liturgy generate-readings --date 2025-11-22 --output-dir /path/to/output
```

### Success Output

**Format**: Text output to stdout

**Example**:
```
Fetching readings for November 22, 2025...
Successfully fetched readings for "Saturday of the Thirty-Third Week in Ordinary Time"
Generated HTML page: readings/2025-11-22.html
```

**Exit Code**: 0

### Error Output

**Format**: Text output to stderr with descriptive error message

**Network Error Example**:
```
Error: Failed to fetch readings from USCCB.org
Network error: Connection timeout after 30 seconds
Please check your internet connection and try again.
```

**Exit Code**: 1

**Invalid Date Example**:
```
Error: Invalid date format: 2025-13-01
Expected format: YYYY-MM-DD
Example: 2025-12-25
```

**Exit Code**: 2

**Parsing Error Example**:
```
Error: Failed to parse readings from USCCB page
The USCCB website structure may have changed.
Please report this issue at: https://github.com/etotten/catholic-liturgy-tools/issues
```

**Exit Code**: 3

**File System Error Example**:
```
Error: Failed to create output file: readings/2025-11-22.html
Permission denied: readings/
Please check directory permissions.
```

**Exit Code**: 4

### Error Codes Summary

| Code | Category | Description |
|------|----------|-------------|
| 0 | Success | Command completed successfully |
| 1 | Network Error | Failed to fetch data from USCCB.org |
| 2 | Validation Error | Invalid input (date format, etc.) |
| 3 | Parse Error | Failed to parse USCCB HTML |
| 4 | File System Error | Failed to write output file |
| 5 | Unknown Error | Unexpected error occurred |

### Behavior

1. **Date Handling**:
   - If no `--date` provided, use system local date (today)
   - Validate date format (YYYY-MM-DD)
   - Accept any date (past, present, reasonable future)
   - USCCB typically has readings available several weeks in advance

2. **Fetching**:
   - Build USCCB URL: `https://bible.usccb.org/bible/readings/{MMDDYY}.cfm`
   - Set User-Agent: `Catholic Liturgy Tools/{version} (Educational Purpose)`
   - Timeout: 30 seconds
   - Retry: Up to 3 attempts with exponential backoff (2s, 4s, 8s)

3. **Parsing**:
   - Extract liturgical day name from page title or H1
   - Extract all reading entries (title, citation, text)
   - Validate: must have at least 1 reading
   - Handle special cases (multiple Masses for feast days)

4. **HTML Generation**:
   - Generate standalone HTML5 page
   - Include liturgical day name, date, all readings
   - Embed CSS styles
   - Add navigation link to index
   - Add attribution link to USCCB source

5. **File Writing**:
   - Create output directory if it doesn't exist
   - Write file as `{output_dir}/{YYYY-MM-DD}.html`
   - Overwrite if file already exists (idempotent)
   - Use UTF-8 encoding

6. **Progress Reporting**:
   - Display "Fetching readings for {date}..." before network request
   - Display "Successfully fetched readings for {liturgical_day}" after successful fetch
   - Display "Generated HTML page: {filepath}" after successful write

### Validation Rules

**Date Validation**:
```python
# Valid
"2025-11-22"
"2025-01-01"
"2025-12-25"

# Invalid
"11/22/2025"  # Wrong format
"2025-13-01"  # Invalid month
"2025-11-32"  # Invalid day
"25-11-22"    # Year too short
```

**Output Directory**:
- Must be a valid relative or absolute path
- Directory will be created if it doesn't exist
- Parent directory must exist
- Must have write permissions

### Dependencies

**External Services**:
- USCCB.org (bible.usccb.org)
- Requires internet connection

**Python Modules**:
- `catholic_liturgy_tools.scraper.usccb.USCCBReadingsScraper`
- `catholic_liturgy_tools.generator.readings.generate_readings_page`
- `catholic_liturgy_tools.utils.date_utils.get_today`

### Testing Requirements

**Unit Tests**:
- Test command parsing with valid arguments
- Test command parsing with invalid arguments
- Test error handling for each error type
- Test output message formatting

**E2E Tests**:
- Test complete workflow with valid date
- Test complete workflow with today (no date)
- Test with custom output directory
- Test error handling (mocked network failure)
- Test file creation and content validation
- Test idempotency (running twice)

---

## Command: `generate-index` (Modified)

### Description

Scans the `_posts/` and `readings/` directories and generates an index page (`index.md`) with links to all daily messages and readings. **Modified from spec 001 to include readings.**

### Syntax

```bash
catholic-liturgy generate-index [OPTIONS]
```

### Options

| Option | Short | Type | Required | Default | Description |
|--------|-------|------|----------|---------|-------------|
| `--posts-dir` | `-p` | string | No | `_posts` | Directory containing daily message files |
| `--readings-dir` | `-r` | string | No | `readings` | Directory containing readings HTML files |
| `--output-file` | `-o` | string | No | `index.md` | Output file path for index |
| `--help` | `-h` | flag | No | N/A | Show help message and exit |

### Examples

**Generate index with defaults**:
```bash
catholic-liturgy generate-index
```

**Generate with custom directories**:
```bash
catholic-liturgy generate-index --posts-dir _posts --readings-dir readings --output-file index.md
```

### Success Output

**Example**:
```
Scanning daily messages in _posts/...
Found 5 message(s)

Scanning daily readings in readings/...
Found 3 reading(s)

Generated index page with 5 messages and 3 readings
File: index.md
```

**Exit Code**: 0

### Modified Behavior

**New**: Scan `readings/` directory in addition to `_posts/`

**Steps**:
1. Scan `_posts/` directory for `*-daily-message.md` files
2. Scan `readings/` directory for `*.html` files
3. Parse HTML files to extract liturgical day name
4. Sort both lists by date (newest first)
5. Generate `index.md` with two sections:
   - "Daily Messages"
   - "Daily Readings"
6. Include links to all found files
7. Handle empty directories gracefully

**Output Format** (index.md):
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

### Validation Rules

**Directory Validation**:
- Directories must exist (or be empty for new projects)
- Must have read permissions
- If directory doesn't exist, treat as empty (no error)

**File Parsing**:
- Message files: Extract date from filename (`YYYY-MM-DD-daily-message.md`)
- Readings files: Extract date from filename (`YYYY-MM-DD.html`)
- For readings: Parse HTML to extract liturgical day name from `<h1>` or `<title>`

---

## Command: `trigger-publish` (Unchanged, reference only)

### Description

Triggers the GitHub Actions workflow to generate and publish content to GitHub Pages. **Modified from spec 001 to trigger renamed workflow.**

### Syntax

```bash
catholic-liturgy trigger-publish [OPTIONS]
```

### Behavior Change

**New**: Trigger `publish-content.yml` workflow (renamed from `publish-daily-message.yml`)

**Note**: This command's implementation will be updated to reference the new workflow name, but the interface remains the same.

---

## Error Handling Guidelines

### User-Friendly Error Messages

All error messages should follow this pattern:

```
Error: {Brief description of what went wrong}
{Detailed explanation of the cause}
{Suggested action to resolve the issue}
```

**Example**:
```
Error: Failed to fetch readings from USCCB.org
Network error: Connection timeout after 30 seconds
Please check your internet connection and try again.
```

### Error Categories

1. **Network Errors**: Issues connecting to USCCB.org
   - Timeout, connection refused, DNS failure
   - Suggest: Check internet connection, try again later

2. **Validation Errors**: Invalid user input
   - Invalid date format, invalid directory path
   - Suggest: Correct format with example

3. **Parse Errors**: Failed to parse USCCB HTML
   - Unexpected HTML structure, missing elements
   - Suggest: Report issue (may indicate USCCB site change)

4. **File System Errors**: Issues reading/writing files
   - Permission denied, disk full, directory not found
   - Suggest: Check permissions, verify paths

5. **Unknown Errors**: Unexpected exceptions
   - Any other error not caught by above categories
   - Suggest: Report issue with error details

### Logging vs User Output

**User Output (stdout/stderr)**:
- Brief, actionable messages
- No technical jargon
- Clear next steps

**Logs (for developers)**:
- Detailed technical information
- Stack traces
- HTTP response codes, URLs
- HTML structure details

---

## Help Text

### `generate-readings --help`

```
Usage: catholic-liturgy generate-readings [OPTIONS]

Fetch daily Catholic liturgical readings from USCCB.org and generate an HTML page.

Options:
  -d, --date TEXT        Date to generate readings for (YYYY-MM-DD format)
                         Default: today
  -o, --output-dir TEXT  Output directory for HTML files
                         Default: readings
  -h, --help             Show this message and exit

Examples:
  # Generate readings for today
  catholic-liturgy generate-readings

  # Generate readings for Christmas Day
  catholic-liturgy generate-readings --date 2025-12-25

  # Generate with custom output directory
  catholic-liturgy generate-readings --output-dir /path/to/output

Source: Readings are fetched from the United States Conference of Catholic
        Bishops (USCCB) at bible.usccb.org

For more information, visit:
  https://github.com/etotten/catholic-liturgy-tools
```

### `generate-index --help` (Updated)

```
Usage: catholic-liturgy generate-index [OPTIONS]

Generate an index page with links to all daily messages and readings.

Options:
  -p, --posts-dir TEXT     Directory containing daily message files
                           Default: _posts
  -r, --readings-dir TEXT  Directory containing readings HTML files
                           Default: readings
  -o, --output-file TEXT   Output file path for index
                           Default: index.md
  -h, --help               Show this message and exit

Examples:
  # Generate index with defaults
  catholic-liturgy generate-index

  # Generate with custom directories
  catholic-liturgy generate-index --posts-dir _posts --readings-dir readings

The generated index.md includes two sections:
  - Daily Messages: Links to message markdown files in _posts/
  - Daily Readings: Links to readings HTML files in readings/

For more information, visit:
  https://github.com/etotten/catholic-liturgy-tools
```

---

## Contract Validation

### Automated Contract Testing

Tests should verify that commands adhere to this contract:

```python
def test_generate_readings_command_contract():
    """Verify generate-readings command follows contract."""
    # Test 1: Valid execution returns exit code 0
    result = run_command(['generate-readings', '--date', '2025-11-22'])
    assert result.returncode == 0
    
    # Test 2: Output includes liturgical day name
    assert "Saturday of the Thirty-Third Week" in result.stdout
    
    # Test 3: Output includes file path
    assert "readings/2025-11-22.html" in result.stdout
    
    # Test 4: Invalid date returns exit code 2
    result = run_command(['generate-readings', '--date', 'invalid'])
    assert result.returncode == 2
    assert "Error: Invalid date format" in result.stderr
    
    # Test 5: Help option works
    result = run_command(['generate-readings', '--help'])
    assert result.returncode == 0
    assert "Usage:" in result.stdout
```

---

## Version Compatibility

**Initial Version**: 0.2.0 (this feature)

**Backward Compatibility**:
- Existing commands (`generate-message`, `trigger-publish`) unchanged
- New command (`generate-readings`) additive
- Modified command (`generate-index`) backward compatible (adds new functionality without breaking existing behavior)

**Future Compatibility**:
- Command interfaces should remain stable
- New options may be added (additive changes only)
- Deprecation warnings required before removing options
- Major version bump (1.0.0) if breaking changes needed

---

**Document Status**: Complete - ready for implementation
