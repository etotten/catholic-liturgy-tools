# Research: Site Content Restructuring

**Feature**: 003-site-content-restructure  
**Date**: 2025-11-25  
**Status**: Complete

## Overview

This document consolidates research findings for restructuring the site content organization. All clarifications have been resolved during the specification phase, so research focuses on validating technical approaches and documenting decisions.

---

## Research Areas

### 1. GitHub Pages Deployment Strategy

**Question**: How to deploy `_site/` contents to serve from repository root URL?

**Decision**: Use `gh-pages` branch containing only `_site/` directory contents

**Rationale**:
- GitHub Pages natively supports publishing from specific branches
- Keeps source code separate from published content
- Clean deployment model - branch contains only what should be published
- Standard practice used by many static site generators (Jekyll, etc.)

**Alternatives Considered**:
- **Publishing from `/docs`**: Would require renaming `_site` to `docs`, less intuitive for "site content"
- **Root-level publishing**: Would clutter repository root with generated content alongside source
- **Subtree deployment**: More complex, harder to maintain

**Implementation Notes**:
- GitHub Actions workflow will build content in `_site/` on main branch
- Workflow will force-push `_site/` contents to `gh-pages` branch
- Repository settings will be configured to publish from `gh-pages` branch
- This approach allows preview on main branch before deployment

**References**:
- GitHub Pages documentation: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- Standard pattern used by Jekyll, Hugo, and other static site generators

---

### 2. HTML Index Page Generation

**Question**: What structure and styling for HTML index page?

**Decision**: Semantic HTML with basic inline CSS for readability

**Structure**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catholic Liturgy Tools</title>
    <style>
        /* Basic inline CSS for readability */
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #333; }
        h2 { color: #666; margin-top: 2em; }
        ul { list-style: none; padding: 0; }
        li { margin: 0.5em 0; }
        a { color: #0066cc; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Catholic Liturgy Tools</h1>
    
    <h2>Daily Messages</h2>
    <ul>
        <li><a href="messages/2025-11-25-daily-message.md">2025-11-25</a></li>
        <!-- more messages in reverse chronological order -->
    </ul>
    
    <h2>Daily Readings</h2>
    <ul>
        <li><a href="readings/2025-11-25.html">2025-11-25 - Liturgical Day Name</a></li>
        <!-- more readings in reverse chronological order -->
    </ul>
</body>
</html>
```

**Rationale**:
- Self-contained (no external dependencies)
- Works in all browsers without JavaScript
- Accessible and printable
- Easy to maintain and extend
- Sufficient for project's simple needs

**Alternatives Considered**:
- **No styling**: Poor user experience, harder to read
- **External CSS file**: Unnecessary complexity for simple styling needs
- **JavaScript enhancements**: Out of scope, adds complexity

---

### 3. Path Resolution & Link Structure

**Question**: How to structure relative paths for reliable navigation?

**Decision**: Use relative paths from `_site/` root

**Path Patterns**:
- Index page: `_site/index.html`
- Message links: `messages/YYYY-MM-DD-daily-message.md` (relative to index)
- Reading links: `readings/YYYY-MM-DD.html` (relative to index)

**Rationale**:
- Simple and predictable
- Works correctly when GitHub Pages serves from branch root
- No need for absolute URLs or complex path resolution
- Matches standard static site conventions

**Testing Strategy**:
- Verify links work when opening `_site/index.html` locally in browser
- Verify links work after deployment to GitHub Pages
- Verify both `/` and `/index.html` routes work on deployed site

---

### 4. File Migration Strategy

**Question**: How to migrate existing content to new structure?

**Decision**: One-time manual migration during implementation, not built into CLI

**Migration Steps**:
1. Create `_site/messages/` and `_site/readings/` directories
2. Move files from `_posts/` to `_site/messages/`
3. Move files from `readings/` to `_site/readings/`
4. Generate new `_site/index.html` (replacing root `index.md`)
5. Delete old directories: `_posts/`, `readings/`, `index.md`
6. Update `.gitignore` if needed
7. Commit migration in feature branch

**Rationale**:
- Personal project with small content volume (~10-20 files)
- One-time operation, not recurring need
- Simpler than building migration logic into CLI
- Aligns with simplicity principle from constitution
- Git history preserves old structure if needed

**Alternatives Considered**:
- **Automatic migration in CLI**: Unnecessary complexity, would clutter simple generation commands
- **Separate migration command**: Overkill for one-time operation
- **Manual migration with script**: Could work but still more complex than needed

---

### 5. GitHub Actions Workflow Updates

**Question**: How to modify workflow for gh-pages deployment?

**Decision**: Use peaceiris/actions-gh-pages action for deployment

**Workflow Changes**:
```yaml
# After content generation steps:
- name: Deploy to GitHub Pages
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./_site
    force_orphan: true  # Clean gh-pages branch each time
```

**Rationale**:
- Standard, well-maintained action for gh-pages deployment
- Handles branch creation, force pushing, and cleanup
- Simpler than custom git commands
- Supports force-orphan mode for clean deployments

**Alternatives Considered**:
- **Manual git commands**: More error-prone, harder to maintain
- **actions/deploy-pages**: Requires different permissions model, less flexible
- **Custom script**: Reinventing the wheel

**References**:
- peaceiris/actions-gh-pages: https://github.com/peaceiris/actions-gh-pages

---

### 6. Python Implementation Patterns

**Question**: Best practices for updating generator modules?

**Decision**: Update existing functions with new default paths, preserve output_dir parameter

**Code Pattern**:
```python
def generate_message(output_dir: str = "_site/messages") -> Path:
    """Generate daily message in new location."""
    # Existing logic, just changed default output_dir
    pass

def generate_index(output_file: str = "_site/index.html") -> Path:
    """Generate index as HTML instead of Markdown."""
    # New HTML generation logic
    pass
```

**Rationale**:
- Backward compatible - users can override output_dir if needed
- Minimal code changes
- Maintains existing test patterns
- Clear parameter defaults document new structure

**Testing Approach**:
- Update unit tests to verify new default paths
- Update integration tests to verify HTML output
- Update E2E tests to verify `_site/` structure
- Maintain 90%+ coverage requirement

---

## Dependencies & Prerequisites

### External Dependencies
- **GitHub Pages**: For hosting (already in use)
- **GitHub Actions**: For automated deployment (already in use)
- **peaceiris/actions-gh-pages**: For gh-pages deployment (new dependency)

### Internal Dependencies
- Existing generator modules: `message.py`, `readings.py`, `index.py`
- Existing utilities: `file_ops.py`, `date_utils.py`
- Existing CLI: `cli.py`

### No New Python Dependencies
All changes can be implemented with standard library and existing dependencies.

---

## Risk Assessment

### Low Risk Areas
✅ **Path changes**: Straightforward, well-tested pattern  
✅ **HTML generation**: Simple string construction, easy to test  
✅ **File migration**: One-time operation, can be verified manually  

### Medium Risk Areas
⚠️ **GitHub Actions workflow**: Need to test deployment to gh-pages branch  
⚠️ **Test coverage**: Must update all tests to maintain 90%+ coverage  

### Mitigation Strategies
- Test gh-pages deployment on feature branch before merging
- Run full test suite after each change
- Verify live site after deployment
- Keep feature branch until verification complete

---

## Open Questions

**None** - All questions resolved during specification/clarification phase:
- ✅ Deployment strategy (gh-pages branch)
- ✅ Index page title ("Catholic Liturgy Tools")
- ✅ Migration approach (one-time dev task)
- ✅ Old file cleanup (delete after migration)
- ✅ Styling approach (basic inline CSS)

---

## Summary

All research complete. Implementation can proceed to Phase 1 (Design & Contracts) with confidence. No technical blockers identified. Approach aligns with project constitution and minimalism principle.
