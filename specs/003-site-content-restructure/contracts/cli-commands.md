# CLI Commands Contract

**Feature**: 003-site-content-restructure  
**Date**: 2025-11-25

## Overview

This document defines the CLI interface contracts. **Important**: No new commands are being added. Existing commands are being updated to output to new `_site/` directory structure while maintaining backward compatibility through the `output_dir` parameter.

---

## Command: `generate-message`

### Current Behavior (v0.2.0)
```bash
catholic-liturgy generate-message [--output-dir DIR]
```

**Default Output**: `_posts/YYYY-MM-DD-daily-message.md`

### New Behavior (v0.3.0)
```bash
catholic-liturgy generate-message [--output-dir DIR]
```

**Default Output**: `_site/messages/YYYY-MM-DD-daily-message.md`

### Changes
- ✅ Command name: **UNCHANGED**
- ✅ Parameters: **UNCHANGED**
- ⚠️ Default output directory: **CHANGED** from `_posts` to `_site/messages`
- ✅ Backward compatibility: **MAINTAINED** via `--output-dir` parameter

### Examples

**Generate to default location (new structure)**:
```bash
$ catholic-liturgy generate-message
Generated daily message for 2025-11-25
File: _site/messages/2025-11-25-daily-message.md
```

**Generate to custom location (backward compatibility)**:
```bash
$ catholic-liturgy generate-message --output-dir custom/path
Generated daily message for 2025-11-25
File: custom/path/2025-11-25-daily-message.md
```

### Exit Codes
- `0`: Success - message generated
- `1`: Error - file write failed or other error

### Error Messages
- `"Error: Failed to create message file: {error}"` - File system error
- `"Error: {error}"` - General error

---

## Command: `generate-readings`

### Current Behavior (v0.2.0)
```bash
catholic-liturgy generate-readings [--date YYYY-MM-DD] [--output-dir DIR]
```

**Default Output**: `readings/YYYY-MM-DD.html`

### New Behavior (v0.3.0)
```bash
catholic-liturgy generate-readings [--date YYYY-MM-DD] [--output-dir DIR]
```

**Default Output**: `_site/readings/YYYY-MM-DD.html`

### Changes
- ✅ Command name: **UNCHANGED**
- ✅ Parameters: **UNCHANGED**
- ⚠️ Default output directory: **CHANGED** from `readings` to `_site/readings`
- ✅ Backward compatibility: **MAINTAINED** via `--output-dir` parameter

### Examples

**Generate today's readings to default location**:
```bash
$ catholic-liturgy generate-readings
Fetching readings from USCCB for November 25, 2025...
Generated readings page for Monday of the Thirty-Fourth Week in Ordinary Time
File: _site/readings/2025-11-25.html
```

**Generate specific date to custom location**:
```bash
$ catholic-liturgy generate-readings --date 2025-12-25 --output-dir custom/readings
Fetching readings from USCCB for December 25, 2025...
Generated readings page for The Nativity of the Lord (Christmas)
File: custom/readings/2025-12-25.html
```

### Exit Codes
- `0`: Success - readings generated
- `1`: Error - network, parse, validation, or file system error

### Error Messages
- `"Error: Network error: {details}"` - USCCB site unreachable
- `"Error: Failed to parse readings: {details}"` - HTML parsing failed
- `"Error: Invalid date format. Use YYYY-MM-DD."` - Date validation failed
- `"Error: Date {date} is not valid"` - Date out of range or invalid

---

## Command: `generate-index`

### Current Behavior (v0.2.0)
```bash
catholic-liturgy generate-index [--output-file FILE] [--posts-dir DIR] [--readings-dir DIR]
```

**Default Output**: `index.md` (Markdown format)  
**Default Scan Paths**: `_posts/` for messages, `readings/` for readings

### New Behavior (v0.3.0)
```bash
catholic-liturgy generate-index [--output-file FILE] [--posts-dir DIR] [--readings-dir DIR]
```

**Default Output**: `_site/index.html` (HTML format)  
**Default Scan Paths**: `_site/messages/` for messages, `_site/readings/` for readings

### Changes
- ✅ Command name: **UNCHANGED**
- ✅ Parameters: **UNCHANGED**
- ⚠️ Default output file: **CHANGED** from `index.md` to `_site/index.html`
- ⚠️ Default output format: **CHANGED** from Markdown to HTML
- ⚠️ Default scan paths: **CHANGED** to `_site/messages/` and `_site/readings/`
- ✅ Backward compatibility: **MAINTAINED** via parameters

### Examples

**Generate index to default location (new structure, HTML)**:
```bash
$ catholic-liturgy generate-index
Generated index page with 10 messages and 5 readings
File: _site/index.html
```

**Generate Markdown index to custom location (backward compatibility)**:
```bash
$ catholic-liturgy generate-index --output-file custom/index.md --posts-dir _posts --readings-dir readings
Generated index page with 10 messages and 5 readings
File: custom/index.md
```

### Exit Codes
- `0`: Success - index generated
- `1`: Error - file write failed or other error

### Error Messages
- `"Error: Failed to write index file: {error}"` - File system error
- `"Error: {error}"` - General error

### Output Format Detection

**Logic**: Format is determined by file extension
- If `--output-file` ends with `.html` → generate HTML
- If `--output-file` ends with `.md` → generate Markdown
- Default (no parameter) → generate HTML (new behavior)

---

## Command: `trigger-action`

### Behavior
```bash
catholic-liturgy trigger-action [--workflow WORKFLOW]
```

**No Changes**: This command is **UNCHANGED** - it triggers GitHub Actions which will use the updated generators

---

## Parameter Specifications

### `--output-dir DIR`
- **Type**: String (directory path)
- **Required**: No
- **Default**: Varies by command (see above)
- **Purpose**: Override default output directory
- **Used by**: `generate-message`, `generate-readings`

### `--output-file FILE`
- **Type**: String (file path)
- **Required**: No
- **Default**: `_site/index.html`
- **Purpose**: Override default output file
- **Used by**: `generate-index`

### `--posts-dir DIR`
- **Type**: String (directory path)
- **Required**: No
- **Default**: `_site/messages`
- **Purpose**: Override directory to scan for message files
- **Used by**: `generate-index`

### `--readings-dir DIR`
- **Type**: String (directory path)
- **Required**: No
- **Default**: `_site/readings`
- **Purpose**: Override directory to scan for readings files
- **Used by**: `generate-index`

### `--date YYYY-MM-DD`
- **Type**: String (ISO date format)
- **Required**: No
- **Default**: Today's date
- **Purpose**: Generate readings for specific date
- **Used by**: `generate-readings`

### `--workflow WORKFLOW`
- **Type**: String (workflow filename)
- **Required**: No
- **Default**: `publish-content.yml`
- **Purpose**: Specify which GitHub Actions workflow to trigger
- **Used by**: `trigger-action`

---

## Backward Compatibility Strategy

### Philosophy
All CLI commands maintain **full backward compatibility** through optional parameters. Users who need the old behavior can explicitly specify old paths.

### Migration Path for Users

**Option 1: Adopt new defaults immediately**
```bash
# Works with new structure automatically
catholic-liturgy generate-message
catholic-liturgy generate-readings
catholic-liturgy generate-index
```

**Option 2: Continue using old paths**
```bash
# Explicitly specify old paths
catholic-liturgy generate-message --output-dir _posts
catholic-liturgy generate-readings --output-dir readings
catholic-liturgy generate-index --output-file index.md --posts-dir _posts --readings-dir readings
```

**Option 3: Mixed approach**
```bash
# Use new defaults for some, old paths for others
catholic-liturgy generate-message  # New: _site/messages/
catholic-liturgy generate-readings --output-dir readings  # Old: readings/
```

---

## Version Compatibility Matrix

| Version | generate-message | generate-readings | generate-index | Breaking Changes |
|---------|------------------|-------------------|----------------|------------------|
| 0.2.0   | → `_posts/`      | → `readings/`     | → `index.md` (MD) | N/A |
| 0.3.0   | → `_site/messages/` | → `_site/readings/` | → `_site/index.html` (HTML) | None (defaults changed) |

**Semantic Versioning Justification**:
- **MINOR bump** (0.2.0 → 0.3.0): New functionality added (HTML generation, new directory structure)
- **Not MAJOR bump**: No breaking changes - all existing functionality preserved via parameters
- **Not PATCH bump**: More than just bug fixes - adds new behavior and defaults

---

## Testing Contracts

### Unit Tests
Each command function must have tests covering:
- ✅ Default behavior (new paths)
- ✅ Custom paths via parameters (backward compatibility)
- ✅ Error conditions (file write failures, network errors, etc.)
- ✅ Output format detection (for `generate-index`)

### E2E Tests
End-to-end tests must verify:
- ✅ Command succeeds with default parameters
- ✅ Files are created in correct locations
- ✅ Output format is correct (HTML vs. Markdown)
- ✅ Links in generated index work correctly
- ✅ Backward compatibility scenarios work

### Coverage Requirement
- **Minimum**: 90% line coverage (per constitution)
- **Focus**: New path logic, HTML generation, format detection

---

## Implementation Notes

### Code Changes Required

**File**: `src/catholic_liturgy_tools/cli.py`
- Update default values for `output_dir` parameters
- Update default value for `output_file` parameter
- Update default values for `posts_dir` and `readings_dir` parameters
- Update help text to reflect new defaults

**File**: `src/catholic_liturgy_tools/generator/message.py`
- Change default: `output_dir="_site/messages"`

**File**: `src/catholic_liturgy_tools/generator/readings.py`
- Change default: `output_dir="_site/readings"`

**File**: `src/catholic_liturgy_tools/generator/index.py`
- Change default: `output_file="_site/index.html"`
- Change defaults: `posts_dir="_site/messages"`, `readings_dir="_site/readings"`
- Add HTML generation logic (detect format from file extension)

---

## Summary

✅ **No new commands added**  
✅ **No command signatures changed**  
✅ **Full backward compatibility maintained**  
⚠️ **Default behavior changed** (justifies MINOR version bump)  
✅ **All existing parameters preserved**
