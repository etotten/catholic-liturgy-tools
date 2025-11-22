# Data Model

**Feature**: GitHub Pages Daily Message  
**Branch**: 001-github-pages  
**Phase**: 1 (Design & Contracts)  
**Date**: 2025-11-22

## Purpose

This document defines the core entities, their attributes, relationships, and validation rules for the GitHub Pages Daily Message feature.

---

## Entities

### 1. Daily Message

A Daily Message represents a single day's published message containing a date and greeting text.

**Attributes**:
- `date`: ISO 8601 date string (YYYY-MM-DD format)
  - Required: Yes
  - Validation: Must be valid date, format YYYY-MM-DD
  - Example: `"2025-11-22"`
- `greeting`: Text content of the message
  - Required: Yes
  - Validation: Non-empty string
  - Default: `"Hello Catholic World"`
- `filename`: Derived attribute, not stored separately
  - Format: `{date}-daily-message.md`
  - Example: `"2025-11-22-daily-message.md"`
- `file_path`: Derived attribute, full path to file
  - Format: `_posts/{filename}`
  - Example: `"_posts/2025-11-22-daily-message.md"`

**File Representation** (Markdown with YAML frontmatter):
```markdown
---
layout: post
title: "Daily Message for {date}"
date: {date}
---

# {date}

{greeting}
```

**Validation Rules**:
1. Date must be parseable as YYYY-MM-DD
2. Date cannot be in the future (if enforced; currently not enforced)
3. Greeting must be non-empty
4. File must have valid YAML frontmatter
5. Content must be valid UTF-8

**State Transitions**:
- Created: New Daily Message generated for a date
- Updated: Daily Message for existing date overwritten
- Published: File committed and pushed to repository (triggers GitHub Pages deployment)

**Relationships**:
- One Daily Message per date (unique by date)
- Many Daily Messages are linked by one Index Page

---

### 2. Index Page

An Index Page represents the homepage that lists and links to all Daily Messages.

**Attributes**:
- `title`: Page title
  - Required: Yes
  - Value: `"Catholic Liturgy Tools - Daily Messages"`
- `messages`: List of message entries to display
  - Required: Yes (can be empty list)
  - Type: List of MessageEntry objects
  - Sorted: Reverse chronological order (newest first)
- `filename`: Fixed value
  - Value: `"index.md"`
- `file_path`: Derived attribute
  - Value: `"index.md"` (root of repository)

**MessageEntry** (Component of Index Page):
- `date`: Date of the message (YYYY-MM-DD)
- `title`: Display title (e.g., "Daily Message for 2025-11-22")
- `link`: Relative link to message file
  - Format: `_posts/{date}-daily-message.md` (Jekyll converts to HTML)

**File Representation** (Markdown):
```markdown
---
layout: page
title: "Catholic Liturgy Tools - Daily Messages"
---

# Daily Messages

## Recent Messages

{% for post in site.posts %}
- [{{ post.title }}]({{ post.url }}) - {{ post.date | date: "%Y-%m-%d" }}
{% endfor %}
```

**Alternative Simple Representation** (No Jekyll liquid):
```markdown
# Catholic Liturgy Tools - Daily Messages

## Recent Messages

- [Daily Message for 2025-11-23](_posts/2025-11-23-daily-message.md)
- [Daily Message for 2025-11-22](_posts/2025-11-22-daily-message.md)
- [Daily Message for 2025-11-21](_posts/2025-11-21-daily-message.md)
```

**Decision**: Use simple markdown representation (no Liquid templates) for Phase 1-2. Jekyll will still process it, and links will work. Liquid templates can be added in future enhancement.

**Validation Rules**:
1. Must contain valid frontmatter (if using Jekyll layout)
2. Links must point to valid _posts files
3. Dates must be in reverse chronological order
4. No duplicate dates in the list
5. File must be valid UTF-8

**State Transitions**:
- Generated: Index created/updated with current list of messages
- Published: File committed and pushed (becomes homepage)

**Relationships**:
- One Index Page per repository
- Links to many Daily Messages

---

### 3. GitHub Workflow Trigger (P4 Only)

A Workflow Trigger represents a request to execute the GitHub Actions workflow remotely.

**Attributes**:
- `workflow_file`: Name of workflow file to trigger
  - Required: Yes
  - Default: `"publish-daily-message.yml"`
  - Validation: Must exist in `.github/workflows/`
- `ref`: Git branch/ref to run workflow on
  - Required: Yes
  - Default: `"main"`
  - Validation: Must be valid branch name
- `token`: GitHub Personal Access Token
  - Required: Yes
  - Source: Environment variable `GITHUB_TOKEN`
  - Validation: Must be non-empty, must have `workflow` scope
- `owner`: Repository owner
  - Required: Yes
  - Example: `"etotten"`
- `repo`: Repository name
  - Required: Yes
  - Example: `"catholic-liturgy-tools"`

**API Request Representation**:
```json
POST /repos/{owner}/{repo}/actions/workflows/{workflow_file}/dispatches
Headers:
  Authorization: token {token}
  Accept: application/vnd.github.v3+json
Body:
  {
    "ref": "{ref}"
  }
```

**Validation Rules**:
1. Token must be present in environment
2. Workflow file must exist (can verify via API or assume valid)
3. Owner and repo must be valid GitHub identifiers
4. API must return 204 (success) or error codes (401, 403, 404)

**State Transitions**:
- Requested: API call sent to GitHub
- Accepted: GitHub returns 204 (workflow queued)
- Failed: GitHub returns error (authentication, not found, etc.)

**Relationships**:
- N/A (external API call, no stored relationships)

---

## Entity Relationship Diagram

```
┌─────────────────┐
│  Daily Message  │
│  (File in       │
│   _posts/)      │
│                 │
│ - date          │
│ - greeting      │
│ - filename      │
│ - file_path     │
└────────┬────────┘
         │
         │ many
         │
         ▼
┌─────────────────┐
│   Index Page    │
│   (index.md)    │
│                 │
│ - title         │
│ - messages[]    │
│ - filename      │
└─────────────────┘

┌──────────────────────┐
│ GitHub Workflow      │
│ Trigger (P4)         │
│ (API Call Only)      │
│                      │
│ - workflow_file      │
│ - ref                │
│ - token              │
│ - owner              │
│ - repo               │
└──────────────────────┘
(No relationships - external API)
```

---

## Data Flow

### Flow 1: Generate Daily Message (P1)
1. User runs CLI: `catholic-liturgy generate-message`
2. System gets today's date (local timezone)
3. System creates Daily Message entity with date + greeting
4. System validates entity (date format, non-empty greeting)
5. System renders entity to markdown with frontmatter
6. System writes file to `_posts/{date}-daily-message.md`
7. System returns success

### Flow 2: Generate Index Page (P2)
1. User runs CLI: `catholic-liturgy generate-index`
2. System scans `_posts/` directory for `*-daily-message.md` files
3. System parses each file to extract date (from filename or frontmatter)
4. System creates MessageEntry for each file
5. System sorts entries by date (reverse chronological)
6. System deduplicates entries by date
7. System creates Index Page entity with sorted messages
8. System renders entity to markdown
9. System writes file to `index.md`
10. System returns success

### Flow 3: Automated Publish (P3)
1. GitHub Actions workflow triggered (schedule or manual)
2. Workflow runs: `catholic-liturgy generate-message`
3. Workflow runs: `catholic-liturgy generate-index`
4. Workflow commits generated files to repository
5. Workflow pushes to GitHub
6. GitHub Pages automatically deploys updated site

### Flow 4: Remote Trigger (P4)
1. User runs CLI: `catholic-liturgy trigger-publish`
2. System reads `GITHUB_TOKEN` from environment
3. System validates token exists
4. System creates Workflow Trigger entity
5. System sends POST request to GitHub API
6. System receives response (204 success or error)
7. System returns success/failure message to user

---

## Validation Summary

| Entity | Required Validations | Optional Validations |
|--------|---------------------|---------------------|
| Daily Message | Date format (YYYY-MM-DD), non-empty greeting, valid UTF-8 | Date not in future |
| Index Page | Valid frontmatter, no duplicate dates, reverse chronological order, valid UTF-8 | Links point to existing files |
| Workflow Trigger | Token present, non-empty owner/repo, valid workflow file | Token has correct scope (API returns error if not) |

---

## Storage Details

**File System Structure**:
```
Repository Root/
├── _posts/                              # Daily Messages storage
│   ├── 2025-11-22-daily-message.md     # Daily Message entity
│   ├── 2025-11-23-daily-message.md     # Daily Message entity
│   └── ...
├── index.md                             # Index Page entity
└── _config.yml                          # Jekyll configuration (metadata)
```

**File Format**: Markdown with YAML frontmatter (Jekyll convention)
**Encoding**: UTF-8
**Line Endings**: LF (Unix-style, GitHub standard)
**Permissions**: Standard file permissions (readable/writable by user)

---

## Error Scenarios & Data Integrity

### Scenario 1: Corrupted Message File
- **Detection**: File parsing fails (invalid YAML or date)
- **Handling**: Skip file in index generation, log warning
- **Recovery**: User can regenerate message for that date

### Scenario 2: Missing _posts Directory
- **Detection**: Directory doesn't exist when generating message
- **Handling**: Create directory automatically
- **Recovery**: N/A (automatic)

### Scenario 3: Permission Denied
- **Detection**: File write fails with permission error
- **Handling**: Raise clear error message to user
- **Recovery**: User fixes permissions manually

### Scenario 4: Duplicate Date in Index
- **Detection**: Multiple files for same date found
- **Handling**: Deduplicate (keep first/last based on filename sort)
- **Recovery**: N/A (handled automatically)

---

## Future Considerations (Out of Scope for P1-P4)

- **Message Content Extensibility**: Support for richer content (liturgical texts, saint of the day, etc.)
- **Historical Data Import**: Backfill messages for past dates
- **Message Editing**: CLI command to edit existing messages
- **Message Deletion**: CLI command to remove messages
- **Templating Engine**: Support for custom message templates
- **Metadata**: Tags, categories, authors (for Jekyll)

---

## Summary

The data model is intentionally simple:
- **3 core entities**: Daily Message (file), Index Page (file), Workflow Trigger (API call)
- **File-based storage**: No database, leveraging file system
- **Jekyll conventions**: YAML frontmatter + markdown content
- **Clear validation rules**: Ensure data integrity
- **Simple relationships**: One-to-many (index → messages), no complex joins

This simplicity aligns with the constitutional principle of minimalism and ensures the implementation remains straightforward and maintainable.
