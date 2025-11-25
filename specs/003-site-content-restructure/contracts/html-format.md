# HTML Index Format Contract

**Feature**: 003-site-content-restructure  
**Date**: 2025-11-25

## Overview

This document defines the precise HTML structure and styling for the generated index page. The index page is the entry point to the site and must be valid HTML5 with inline CSS.

---

## Complete HTML Template

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
            color: #333;
        }
        h1 {
            color: #333;
            border-bottom: 2px solid #666;
            padding-bottom: 10px;
            margin-bottom: 20px;
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
            padding: 5px 0;
        }
        a {
            color: #0066cc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
            color: #0052a3;
        }
    </style>
</head>
<body>
    <h1>Catholic Liturgy Tools</h1>
    
    <h2>Daily Messages</h2>
    <ul>
        <li><a href="messages/2025-11-25-daily-message.md">2025-11-25</a></li>
        <li><a href="messages/2025-11-24-daily-message.md">2025-11-24</a></li>
        <!-- More messages in reverse chronological order -->
    </ul>
    
    <h2>Daily Readings</h2>
    <ul>
        <li><a href="readings/2025-11-25.html">2025-11-25 - Monday of the Thirty-Fourth Week in Ordinary Time</a></li>
        <li><a href="readings/2025-11-24.html">2025-11-24 - The Solemnity of Our Lord Jesus Christ, King of the Universe</a></li>
        <!-- More readings in reverse chronological order -->
    </ul>
</body>
</html>
```

---

## Required HTML Elements

### Document Type Declaration
```html
<!DOCTYPE html>
```
- **Required**: YES
- **Purpose**: Declares HTML5 document
- **Position**: First line of file

### Root Element
```html
<html lang="en">
```
- **Required**: YES
- **Attributes**: `lang="en"` (English content)
- **Purpose**: Root container for HTML document

### Head Section

#### Character Encoding
```html
<meta charset="UTF-8">
```
- **Required**: YES
- **Purpose**: Ensures proper character rendering

#### Viewport Meta Tag
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```
- **Required**: YES
- **Purpose**: Responsive sizing on mobile devices

#### Title
```html
<title>Catholic Liturgy Tools</title>
```
- **Required**: YES
- **Exact Text**: "Catholic Liturgy Tools"
- **Purpose**: Browser tab title, bookmark name

#### Style Block
```html
<style>
    /* CSS rules here */
</style>
```
- **Required**: YES
- **Purpose**: Inline CSS for styling
- **Content**: See CSS specification below

---

## Required CSS Rules

### Body Styling
```css
body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    line-height: 1.6;
    color: #333;
}
```

**Properties Explained**:
- `font-family`: Arial (widely available sans-serif)
- `max-width`: 800px (optimal reading width)
- `margin: 0 auto`: Centers content horizontally
- `padding`: 20px breathing room on all sides
- `line-height`: 1.6 for better readability
- `color`: #333 (dark gray text, easier on eyes than pure black)

### H1 (Main Heading) Styling
```css
h1 {
    color: #333;
    border-bottom: 2px solid #666;
    padding-bottom: 10px;
    margin-bottom: 20px;
}
```

**Properties Explained**:
- `color`: Matches body text
- `border-bottom`: Visual separator below title
- `padding-bottom`: Space before border
- `margin-bottom`: Space after heading

### H2 (Section Heading) Styling
```css
h2 {
    color: #666;
    margin-top: 2em;
    margin-bottom: 1em;
}
```

**Properties Explained**:
- `color`: Lighter than h1 for hierarchy
- `margin-top`: Significant spacing above sections
- `margin-bottom`: Moderate spacing before list

### List Styling
```css
ul {
    list-style: none;
    padding: 0;
}

li {
    margin: 0.5em 0;
    padding: 5px 0;
}
```

**Properties Explained**:
- `list-style: none`: Remove bullet points (cleaner)
- `padding: 0`: Remove default indentation
- `margin: 0.5em 0`: Vertical spacing between items
- `padding: 5px 0`: Small vertical padding for touch targets

### Link Styling
```css
a {
    color: #0066cc;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
    color: #0052a3;
}
```

**Properties Explained**:
- `color`: Standard blue for links (#0066cc)
- `text-decoration: none`: No underline by default (cleaner)
- `:hover text-decoration`: Underline on hover (feedback)
- `:hover color`: Darker blue on hover (#0052a3)

---

## Body Content Structure

### Main Heading
```html
<h1>Catholic Liturgy Tools</h1>
```
- **Required**: YES
- **Exact Text**: "Catholic Liturgy Tools"
- **Tag**: `<h1>` (semantic importance)

### Messages Section

#### Section Heading
```html
<h2>Daily Messages</h2>
```
- **Required**: YES
- **Exact Text**: "Daily Messages"
- **Tag**: `<h2>` (section-level heading)

#### Message List
```html
<ul>
    <li><a href="messages/2025-11-25-daily-message.md">2025-11-25</a></li>
    <!-- More messages -->
</ul>
```

**Link Format**:
- **href**: `messages/{YYYY-MM-DD}-daily-message.md`
- **Text**: `{YYYY-MM-DD}` (just the date)
- **Order**: Reverse chronological (newest first)

### Readings Section

#### Section Heading
```html
<h2>Daily Readings</h2>
```
- **Required**: YES
- **Exact Text**: "Daily Readings"
- **Tag**: `<h2>` (section-level heading)

#### Readings List
```html
<ul>
    <li><a href="readings/2025-11-25.html">2025-11-25 - Monday of the Thirty-Fourth Week in Ordinary Time</a></li>
    <!-- More readings -->
</ul>
```

**Link Format**:
- **href**: `readings/{YYYY-MM-DD}.html`
- **Text**: `{YYYY-MM-DD} - {Liturgical Day Name}`
- **Order**: Reverse chronological (newest first)

---

## Link Path Specifications

### Relative Path Structure

**From**: `_site/index.html`  
**To Messages**: `_site/messages/YYYY-MM-DD-daily-message.md`  
**Relative Path**: `messages/YYYY-MM-DD-daily-message.md`

**From**: `_site/index.html`  
**To Readings**: `_site/readings/YYYY-MM-DD.html`  
**Relative Path**: `readings/YYYY-MM-DD.html`

### Path Validation Rules
- ✅ Must be relative (no leading `/`)
- ✅ Must use forward slashes (`/`)
- ✅ Must resolve to existing file
- ❌ No backslashes (`\`)
- ❌ No absolute paths (`/path` or `https://`)
- ❌ No parent directory references (`../`)

---

## Sorting Requirements

### Message Sorting
- **Order**: Reverse chronological (newest first)
- **Sort Key**: Date extracted from filename
- **Algorithm**: String sort on YYYY-MM-DD format (natural ordering)

**Example**:
```html
<li><a href="messages/2025-11-25-daily-message.md">2025-11-25</a></li>  <!-- Newest -->
<li><a href="messages/2025-11-24-daily-message.md">2025-11-24</a></li>
<li><a href="messages/2025-11-23-daily-message.md">2025-11-23</a></li>
<li><a href="messages/2025-11-22-daily-message.md">2025-11-22</a></li>  <!-- Oldest -->
```

### Readings Sorting
- **Order**: Reverse chronological (newest first)
- **Sort Key**: Date extracted from filename
- **Algorithm**: String sort on YYYY-MM-DD format (natural ordering)

**Example**:
```html
<li><a href="readings/2025-11-25.html">2025-11-25 - ...</a></li>  <!-- Newest -->
<li><a href="readings/2025-11-24.html">2025-11-24 - ...</a></li>
<li><a href="readings/2025-11-23.html">2025-11-23 - ...</a></li>
<li><a href="readings/2025-11-22.html">2025-11-22 - ...</a></li>  <!-- Oldest -->
```

---

## Validation Rules

### HTML Validation
- ✅ Must pass W3C HTML5 validation
- ✅ All tags must be properly closed
- ✅ Attributes must be properly quoted
- ✅ No deprecated elements or attributes
- ✅ Proper nesting (no invalid parent-child relationships)

### Accessibility (Basic)
- ✅ `lang` attribute on `<html>` tag
- ✅ Semantic heading hierarchy (h1 → h2)
- ✅ Links must have meaningful text (dates and liturgical names)
- ⚠️ Advanced WCAG compliance not required (per constitution scope constraints)

### Browser Compatibility
- ✅ Must work in all modern browsers
- ✅ No browser-specific features or vendor prefixes
- ✅ No JavaScript required
- ✅ Graceful degradation (works with CSS disabled)

---

## Edge Cases

### Empty Lists

**No Messages**:
```html
<h2>Daily Messages</h2>
<ul>
    <!-- Empty list - no <li> elements -->
</ul>
```

**No Readings**:
```html
<h2>Daily Readings</h2>
<ul>
    <!-- Empty list - no <li> elements -->
</ul>
```

**Behavior**: Sections still rendered with empty lists (no conditional hiding)

### Special Characters in Liturgical Names

**Example**: Liturgical day contains ampersand or quotes
```html
<li><a href="readings/2025-12-25.html">2025-12-25 - The Nativity of the Lord &amp; Christmas Day</a></li>
```

**Rule**: Must be properly HTML-escaped:
- `&` → `&amp;`
- `<` → `&lt;`
- `>` → `&gt;`
- `"` → `&quot;` (in attributes)
- `'` → `&#39;` (in attributes)

---

## Testing Contract

### Visual Tests
- ✅ Page renders correctly in major browsers
- ✅ Styling is applied as specified
- ✅ Links are visually distinct (blue color)
- ✅ Hover states work correctly

### Functional Tests
- ✅ All links resolve to correct files
- ✅ Both `/` and `/index.html` routes work
- ✅ Content is sorted correctly (newest first)
- ✅ Empty lists render without errors

### Validation Tests
- ✅ HTML passes W3C validator
- ✅ No console errors when opening page
- ✅ Works without JavaScript
- ✅ Mobile viewport meta tag is effective

---

## Implementation Notes

### Python String Generation

**Recommended Approach**: Use f-strings with multiline strings

```python
def generate_html_index(messages: List[Path], readings: List[ReadingsEntry]) -> str:
    """Generate HTML index page."""
    
    # Generate message list items
    message_items = "\n".join(
        f'        <li><a href="messages/{msg.name}">{msg.stem.split("-daily-message")[0]}</a></li>'
        for msg in sorted(messages, reverse=True)
    )
    
    # Generate readings list items
    reading_items = "\n".join(
        f'        <li><a href="readings/{r.link}">{r.title}</a></li>'
        for r in sorted(readings, key=lambda x: x.date, reverse=True)
    )
    
    # Generate complete HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catholic Liturgy Tools</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #666;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        h2 {{
            color: #666;
            margin-top: 2em;
            margin-bottom: 1em;
        }}
        ul {{
            list-style: none;
            padding: 0;
        }}
        li {{
            margin: 0.5em 0;
            padding: 5px 0;
        }}
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
            color: #0052a3;
        }}
    </style>
</head>
<body>
    <h1>Catholic Liturgy Tools</h1>
    
    <h2>Daily Messages</h2>
    <ul>
{message_items}
    </ul>
    
    <h2>Daily Readings</h2>
    <ul>
{reading_items}
    </ul>
</body>
</html>
"""
    return html
```

**Note**: Double curly braces `{{}}` in CSS to escape f-string interpolation

---

## Summary

✅ **Format**: Valid HTML5  
✅ **Styling**: Inline CSS for basic readability  
✅ **Title**: "Catholic Liturgy Tools"  
✅ **Sections**: Daily Messages, Daily Readings  
✅ **Sorting**: Reverse chronological (newest first)  
✅ **Links**: Relative paths to subdirectories  
✅ **Validation**: W3C HTML5 compliant
