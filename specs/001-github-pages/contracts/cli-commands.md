# CLI Command Contracts

**Feature**: GitHub Pages Daily Message  
**Branch**: 001-github-pages  
**Phase**: 1 (Design & Contracts)  
**Date**: 2025-11-22

## Purpose

This document specifies the contract (interface) for all CLI commands added by this feature. Each command is documented with its signature, behavior, inputs, outputs, and error conditions.

---

## Command 1: `generate-message` (Priority P1)

### Signature
```bash
catholic-liturgy generate-message [OPTIONS]
```

### Description
Generates a daily message markdown file for today's date containing the greeting "Hello Catholic World". The file is created in the `_posts/` directory with Jekyll-compatible format.

### Options
Currently no options. Future enhancements may add:
- `--date DATE`: Generate message for specific date (out of scope for P1)
- `--output-dir DIR`: Custom output directory (out of scope for P1)
- `--greeting TEXT`: Custom greeting text (out of scope for P1)

### Inputs
- **System Date**: Uses system's local date via `date.today()`
- **Template**: Fixed message template with date and greeting

### Outputs

**Success (Exit Code 0)**:
```
Generated daily message for 2025-11-22
File: _posts/2025-11-22-daily-message.md
```

**File Created**: `_posts/2025-11-22-daily-message.md`
```markdown
---
layout: post
title: "Daily Message for 2025-11-22"
date: 2025-11-22
---

# 2025-11-22

Hello Catholic World
```

### Error Conditions

| Error | Exit Code | Message | Cause |
|-------|-----------|---------|-------|
| Permission Denied | 1 | `Error: Cannot write to _posts/ directory. Permission denied.` | No write access to output directory |
| File System Error | 1 | `Error: Failed to create message file: {reason}` | Disk full, invalid filesystem, etc. |

### Behavior

1. Get today's date in YYYY-MM-DD format
2. Create `_posts/` directory if it doesn't exist
3. Generate filename: `{date}-daily-message.md`
4. Create markdown content with YAML frontmatter
5. Write content to file (overwrite if exists)
6. Print success message with filename

### Idempotency
- Running multiple times in same day: Overwrites existing file
- No side effects beyond file creation/update

### Testing Requirements
- **Unit Test**: Test message generation logic with mocked date
- **Integration Test**: Test file creation in temp directory
- **E2E Test**: Execute CLI command, verify file exists and contains correct content

---

## Command 2: `generate-index` (Priority P2)

### Signature
```bash
catholic-liturgy generate-index [OPTIONS]
```

### Description
Generates an index page (`index.md`) that lists all daily message files from the `_posts/` directory with links, sorted in reverse chronological order (newest first).

### Options
Currently no options. Future enhancements may add:
- `--output FILE`: Custom output filename (out of scope for P2)
- `--limit N`: Limit number of messages shown (out of scope for P2)

### Inputs
- **File System**: Scans `_posts/` directory for `*-daily-message.md` files
- **File Parsing**: Extracts dates from filenames

### Outputs

**Success (Exit Code 0)**:
```
Generated index page with 5 messages
File: index.md
```

**File Created**: `index.md`
```markdown
---
layout: page
title: "Catholic Liturgy Tools - Daily Messages"
---

# Catholic Liturgy Tools - Daily Messages

## Recent Messages

- [Daily Message for 2025-11-23](_posts/2025-11-23-daily-message.md)
- [Daily Message for 2025-11-22](_posts/2025-11-22-daily-message.md)
- [Daily Message for 2025-11-21](_posts/2025-11-21-daily-message.md)
```

### Error Conditions

| Error | Exit Code | Message | Cause |
|-------|-----------|---------|-------|
| Missing _posts Directory | 0 (Warning) | `Warning: No _posts/ directory found. Creating empty index.` | Directory doesn't exist (not fatal) |
| Permission Denied | 1 | `Error: Cannot write index.md. Permission denied.` | No write access to output location |
| File System Error | 1 | `Error: Failed to create index file: {reason}` | Disk full, invalid filesystem, etc. |

### Behavior

1. Check if `_posts/` directory exists
2. If not exists, create empty index (with warning)
3. If exists, scan for `*-daily-message.md` files
4. Parse each filename to extract date (format: `YYYY-MM-DD-daily-message.md`)
5. Skip files that don't match pattern (with warning)
6. Sort dates in reverse chronological order
7. Deduplicate dates (if multiple files per date, keep first)
8. Generate markdown content with links
9. Write to `index.md`
10. Print success message with count

### Idempotency
- Running multiple times: Regenerates index from current file system state
- No side effects beyond index file creation/update

### Testing Requirements
- **Unit Test**: Test index generation logic with mock file list
- **Integration Test**: Test with temp directory containing multiple message files
- **E2E Test**: Execute CLI command after generating messages, verify index content

---

## Command 3: `trigger-publish` (Priority P4)

### Signature
```bash
catholic-liturgy trigger-publish [OPTIONS]
```

### Description
Triggers the GitHub Actions workflow remotely to generate and publish daily messages to GitHub Pages. Requires `GITHUB_TOKEN` environment variable.

### Options
Currently no options. Future enhancements may add:
- `--workflow FILE`: Specify workflow filename (default: publish-daily-message.yml)
- `--branch REF`: Specify branch to run on (default: main)

### Environment Variables
- **GITHUB_TOKEN** (Required): GitHub Personal Access Token with `workflow` scope
  - Must be set by user: `export GITHUB_TOKEN=ghp_xxxxx`

### Inputs
- **Environment Variable**: `GITHUB_TOKEN`
- **Hardcoded Values**: Repository owner, repo name, workflow file

### Outputs

**Success (Exit Code 0)**:
```
Successfully triggered GitHub Actions workflow
Workflow: publish-daily-message.yml
Check status at: https://github.com/etotten/catholic-liturgy-tools/actions
```

**Error - Missing Token (Exit Code 1)**:
```
Error: GITHUB_TOKEN environment variable not set
Please set your GitHub Personal Access Token with 'workflow' scope:
  export GITHUB_TOKEN=ghp_your_token_here
See: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
```

**Error - Authentication Failed (Exit Code 1)**:
```
Error: GitHub authentication failed (401 Unauthorized)
Please check your GITHUB_TOKEN is valid and has 'workflow' scope
```

**Error - Workflow Not Found (Exit Code 1)**:
```
Error: Workflow file not found (404 Not Found)
Workflow: publish-daily-message.yml
Please ensure the workflow file exists in .github/workflows/
```

### Error Conditions

| Error | Exit Code | Message | Cause |
|-------|-----------|---------|-------|
| Missing Token | 1 | `Error: GITHUB_TOKEN environment variable not set` | Environment variable not set |
| Authentication Failed | 1 | `Error: GitHub authentication failed (401 Unauthorized)` | Invalid token |
| Forbidden | 1 | `Error: Permission denied (403 Forbidden)` | Token lacks 'workflow' scope |
| Workflow Not Found | 1 | `Error: Workflow file not found (404 Not Found)` | Workflow doesn't exist |
| Network Error | 1 | `Error: Failed to connect to GitHub API: {reason}` | Network issues, GitHub downtime |
| API Error | 1 | `Error: GitHub API error: {reason}` | Other API errors |

### Behavior

1. Check for `GITHUB_TOKEN` environment variable
2. If missing, print error with setup instructions and exit
3. Construct GitHub API URL for workflow dispatch
4. Prepare API request with token and ref (main branch)
5. Send POST request to GitHub API
6. Handle response:
   - 204 No Content → Success
   - 401 → Authentication error
   - 403 → Permission error
   - 404 → Workflow not found
   - Other → Generic API error
7. Print appropriate success/error message

### Idempotency
- Running multiple times: Each call triggers a new workflow run
- No local side effects (only remote API call)

### Testing Requirements
- **Unit Test**: Test API call logic with mocked requests
- **Integration Test**: Test with mock GitHub API responses (success/error scenarios)
- **E2E Test**: Execute CLI command with real/test token (if safe), or verify error handling

---

## Common CLI Behaviors

### Help Text
All commands support `--help`:
```bash
catholic-liturgy generate-message --help
catholic-liturgy generate-index --help
catholic-liturgy trigger-publish --help
```

Each displays:
- Command description
- Usage syntax
- Available options
- Examples

### Version
Already supported by main CLI:
```bash
catholic-liturgy --version
```

### Exit Codes
- **0**: Success
- **1**: Error (general)
- **2**: Usage error (invalid arguments) - if applicable

### Output Format
- Success messages: Plain text, human-readable
- Error messages: Prefixed with "Error:", include actionable advice
- Warnings: Prefixed with "Warning:", non-fatal issues

### Error Message Guidelines
1. Start with "Error:" prefix
2. Explain what went wrong
3. Provide guidance on how to fix (if applicable)
4. Include relevant links to documentation

---

## CLI Integration

### Main CLI Updates

The main CLI (`src/catholic_liturgy_tools/cli.py`) will be updated to include these subcommands:

```python
def main():
    parser = argparse.ArgumentParser(
        prog="catholic-liturgy",
        description="Tools for working with Catholic liturgical content",
    )
    
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # P1: Generate message
    parser_generate = subparsers.add_parser(
        "generate-message",
        help="Generate daily message for today"
    )
    
    # P2: Generate index
    parser_index = subparsers.add_parser(
        "generate-index",
        help="Generate index page with links to all messages"
    )
    
    # P4: Trigger publish
    parser_trigger = subparsers.add_parser(
        "trigger-publish",
        help="Trigger GitHub Actions workflow to publish messages"
    )
    
    args = parser.parse_args()
    
    if args.command == "generate-message":
        return generate_message_command()
    elif args.command == "generate-index":
        return generate_index_command()
    elif args.command == "trigger-publish":
        return trigger_publish_command()
    else:
        parser.print_help()
        return 0
```

---

## API Contract Summary

| Command | Priority | Inputs | Outputs | Exit Codes | Side Effects |
|---------|----------|--------|---------|------------|--------------|
| `generate-message` | P1 | System date | Message file in `_posts/` | 0 (success), 1 (error) | Creates/updates file |
| `generate-index` | P2 | Files in `_posts/` | Index file at root | 0 (success), 1 (error) | Creates/updates index.md |
| `trigger-publish` | P4 | `GITHUB_TOKEN` env var | Success/error message | 0 (success), 1 (error) | Triggers GitHub workflow |

---

## Testing Contract

Each command must have:
1. **Unit tests**: Test logic with mocks (functions isolated)
2. **Integration tests**: Test with temp file system (workflows)
3. **E2E tests**: Execute actual CLI commands (end-to-end behavior)
4. **Coverage**: Minimum 90% for all command code paths

Test files:
- `tests/unit/test_message.py` - Message generation logic
- `tests/unit/test_index.py` - Index generation logic
- `tests/unit/test_github_actions.py` - GitHub API logic (P4)
- `tests/integration/test_message_workflow.py` - Message file creation
- `tests/integration/test_index_workflow.py` - Index generation workflow
- `tests/e2e/test_cli_generate.py` - CLI generate-message (P1)
- `tests/e2e/test_cli_index.py` - CLI generate-index (P2)
- `tests/e2e/test_cli_trigger.py` - CLI trigger-publish (P4)

---

## Future Enhancements (Out of Scope)

- `--date` option for generating historical messages
- `--greeting` option for custom greeting text
- `--output-dir` option for custom output location
- `--format` option for different output formats (HTML, JSON, etc.)
- `--limit` option for index page (show only N most recent)
- `edit-message` command for modifying existing messages
- `delete-message` command for removing messages
- `list-messages` command for viewing all messages without generating index

---

## Summary

Three CLI commands with clear contracts:
1. **generate-message** (P1): Local message generation
2. **generate-index** (P2): Index page generation
3. **trigger-publish** (P4): Remote workflow triggering

Each command has:
- Clear inputs/outputs
- Defined error handling
- Idempotent behavior
- Comprehensive testing requirements
- Constitutional compliance (90% coverage, E2E tests)

Ready for implementation in Phase 2 (Tasks).
