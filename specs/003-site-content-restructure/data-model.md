# Data Model: Site Content Restructuring

**Feature**: 003-site-content-restructure  
**Date**: 2025-11-25  
**Status**: Complete

## Overview

This feature is primarily a restructuring effort focused on file organization and HTML generation. The data model is simple, focusing on file paths and HTML structure rather than complex domain entities.

---

## Core Entities

### 1. Site Content Directory

**Concept**: Root container for all generated publishable content

**Properties**:
- `path`: String - Always `"_site"` at repository root
- `subdirectories`: List[String] - `["messages", "readings"]`

**Purpose**: Provides clean separation between source code and published content

**Validation Rules**:
- Must exist at repository root
- Must be created automatically if missing during generation
- Subdirectories must be created as needed

**Relationships**:
- Contains: Messages Subdirectory, Readings Subdirectory, Index Page

---

### 2. Messages Subdirectory

**Concept**: Container for all daily message markdown files

**Properties**:
- `path`: String - `"_site/messages"`
- `file_pattern`: String - `"{YYYY-MM-DD}-daily-message.md"`

**Content Files**:
- Format: Markdown with YAML frontmatter
- Naming: Date-based (`2025-11-25-daily-message.md`)
- Sorting: Reverse chronological (newest first)

**Validation Rules**:
- Files must match naming pattern
- Must contain valid date in filename (YYYY-MM-DD format)

**Relationships**:
- Contained by: Site Content Directory
- Referenced by: Index Page

---

### 3. Readings Subdirectory

**Concept**: Container for all daily readings HTML files

**Properties**:
- `path`: String - `"_site/readings"`
- `file_pattern`: String - `"{YYYY-MM-DD}.html"`

**Content Files**:
- Format: HTML
- Naming: Date-based (`2025-11-25.html`)
- Sorting: Reverse chronological (newest first)
- Metadata: Liturgical day name extracted from `<h1>` tag

**Validation Rules**:
- Files must match naming pattern
- Must contain valid date in filename (YYYY-MM-DD format)
- Must contain `<h1>` tag with liturgical day name

**Relationships**:
- Contained by: Site Content Directory
- Referenced by: Index Page

---

### 4. Index Page

**Concept**: Single HTML entry point linking to all content

**Properties**:
- `path`: String - `"_site/index.html"`
- `format`: String - `"HTML"`
- `title`: String - `"Catholic Liturgy Tools"`
- `sections`: List[Section] - Messages section, Readings section

**Structure**:
```
Index Page
├── HTML Head
│   ├── Title: "Catholic Liturgy Tools"
│   ├── Charset: UTF-8
│   ├── Viewport meta tag
│   └── Inline CSS styles
├── Body
│   ├── Main Heading (h1): "Catholic Liturgy Tools"
│   ├── Messages Section (h2)
│   │   └── Unordered list of message links
│   └── Readings Section (h2)
│       └── Unordered list of reading links
```

**Validation Rules**:
- Must be valid HTML5
- Must include all required meta tags
- Must contain inline CSS for styling
- Links must use correct relative paths
- Content must be sorted reverse chronologically

**Relationships**:
- Contained by: Site Content Directory
- Links to: Message files, Reading files

---

## File Path Patterns

### Current State (Before Restructuring)
```
<repository-root>/
├── _posts/
│   └── YYYY-MM-DD-daily-message.md
├── readings/
│   └── YYYY-MM-DD.html
└── index.md
```

### Target State (After Restructuring)
```
<repository-root>/
└── _site/
    ├── messages/
    │   └── YYYY-MM-DD-daily-message.md
    ├── readings/
    │   └── YYYY-MM-DD.html
    └── index.html
```

---

## Link Structure

### Index Page to Messages
```
<a href="messages/YYYY-MM-DD-daily-message.md">YYYY-MM-DD</a>
```

**Path Resolution**:
- Index is at: `_site/index.html`
- Message is at: `_site/messages/YYYY-MM-DD-daily-message.md`
- Relative path from index: `messages/YYYY-MM-DD-daily-message.md`

### Index Page to Readings
```
<a href="readings/YYYY-MM-DD.html">YYYY-MM-DD - Liturgical Day Name</a>
```

**Path Resolution**:
- Index is at: `_site/index.html`
- Reading is at: `_site/readings/YYYY-MM-DD.html`
- Relative path from index: `readings/YYYY-MM-DD.html`

---

## HTML Structure Details

### Complete Index Page Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catholic Liturgy Tools</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        h1 {
            color: #333;
            border-bottom: 2px solid #666;
            padding-bottom: 10px;
        }
        h2 {
            color: #666;
            margin-top: 2em;
            margin-bottom: 1em;
        }
        ul {
            list-style: none;
            padding: 0;
        }
        li {
            margin: 0.5em 0;
        }
        a {
            color: #0066cc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>Catholic Liturgy Tools</h1>
    
    <h2>Daily Messages</h2>
    <ul>
        <!-- Message links, newest first -->
    </ul>
    
    <h2>Daily Readings</h2>
    <ul>
        <!-- Reading links, newest first -->
    </ul>
</body>
</html>
```

### CSS Properties Explained

**Body Styling**:
- `font-family`: Arial for universal readability
- `max-width`: 800px prevents overly wide text lines
- `margin: 0 auto`: Centers content
- `padding`: Adds breathing room on all sides
- `line-height`: Improves text readability

**Heading Styling**:
- `h1`: Main title, dark color, bottom border for emphasis
- `h2`: Section headings, lighter color, spacing for separation

**Link Styling**:
- Default: Blue, no underline (cleaner appearance)
- Hover: Underline appears (provides feedback)

---

## Data Transformations

### 1. Message File Path Transformation
```
Input:  _posts/2025-11-25-daily-message.md
Output: _site/messages/2025-11-25-daily-message.md
```

**Logic**: Change directory from `_posts` to `_site/messages`, preserve filename

### 2. Reading File Path Transformation
```
Input:  readings/2025-11-25.html
Output: _site/readings/2025-11-25.html
```

**Logic**: Add `_site/` prefix, preserve `readings/` directory name

### 3. Index Format Transformation
```
Input:  index.md (Markdown)
Output: _site/index.html (HTML)
```

**Logic**: Complete format change - generate HTML from scratch, not convert existing Markdown

### 4. Link Generation Transformation

**For Messages**:
```
Input:  File path: _site/messages/2025-11-25-daily-message.md
Output: HTML link: <a href="messages/2025-11-25-daily-message.md">2025-11-25</a>
```

**For Readings**:
```
Input:  File path: _site/readings/2025-11-25.html
        Liturgical day: "Monday of the Thirty-Fourth Week in Ordinary Time"
Output: HTML link: <a href="readings/2025-11-25.html">2025-11-25 - Monday of the Thirty-Fourth Week in Ordinary Time</a>
```

---

## State Management

### File System State

**Generation Process**:
1. Check if `_site/` exists → create if missing
2. Check if `_site/messages/` exists → create if missing
3. Check if `_site/readings/` exists → create if missing
4. Generate/write content files
5. Scan directories for existing files
6. Generate index with links to all files

**Idempotency**: All operations are idempotent
- Re-running generation overwrites existing files
- No state accumulation or corruption risk

---

## Validation Rules

### Path Validation
- All paths must be relative to repository root
- No absolute paths allowed
- No path traversal (../) in generated content

### Date Validation
- Date format must be YYYY-MM-DD
- Date must be valid (e.g., not 2025-13-45)
- Used for both filename extraction and link generation

### HTML Validation
- Must be valid HTML5
- Required elements: `<!DOCTYPE html>`, `<html>`, `<head>`, `<body>`
- Required meta tags: charset, viewport
- Required title: "Catholic Liturgy Tools"

### Link Validation
- All links must resolve to existing files
- Relative paths must be correct from index location
- No broken links allowed

---

## Entity Relationships Diagram

```
┌─────────────────────────┐
│  Site Content Directory │
│      (_site/)           │
└───────────┬─────────────┘
            │
            ├──────────────────────────────────────────┐
            │                                          │
            ▼                                          ▼
┌─────────────────────┐                  ┌─────────────────────┐
│ Messages Subdirectory│                  │Readings Subdirectory│
│  (_site/messages/)   │                  │ (_site/readings/)   │
└──────────┬──────────┘                  └──────────┬──────────┘
           │                                         │
           │                                         │
           └─────────────┐         ┌─────────────────┘
                         ▼         ▼
                   ┌──────────────────┐
                   │   Index Page     │
                   │(_site/index.html)│
                   └──────────────────┘
```

**Relationship Types**:
- Containment: Directory contains files
- Reference: Index page links to content files
- One-to-many: One index page, many content files

---

## Summary

The data model is intentionally simple:
- **3 directories**: Root (`_site`), Messages, Readings
- **1 index file**: HTML entry point
- **N content files**: Messages (Markdown) and Readings (HTML)

All relationships are straightforward file-system based containment and linking. No database, no complex state management, no ORM required.
