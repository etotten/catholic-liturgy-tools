# Quickstart Guide: Site Content Restructure

**Feature**: 003-site-content-restructure  
**Target Version**: 0.3.0  
**Date**: 2025-11-25

## Overview

This guide helps developers quickly set up, test, and implement the site content restructuring feature. Follow these steps to work with the new `_site/` directory structure.

---

## Prerequisites

- Python 3.11 or higher
- Git repository cloned
- Virtual environment (recommended)

---

## Quick Setup

### 1. Install Package in Development Mode

```bash
cd /Users/etotten/dev/github.com/etotten/catholic-liturgy-tools
pip install -e .
```

**Why**: Installs CLI commands while allowing live code changes

### 2. Verify Installation

```bash
catholic-liturgy --version
# Expected: 0.3.0 (after implementation)
```

---

## Testing New Structure Locally

### Generate All Content

```bash
# Generate today's message
catholic-liturgy generate-message

# Generate today's readings
catholic-liturgy generate-readings

# Generate HTML index
catholic-liturgy generate-index
```

**Expected Output**:
```
_site/
├── index.html
├── messages/
│   └── 2025-11-25-daily-message.md
└── readings/
    └── 2025-11-25.html
```

### View Generated Site

**macOS**:
```bash
open _site/index.html
```

**Linux**:
```bash
xdg-open _site/index.html
```

**Windows**:
```bash
start _site/index.html
```

**What to Check**:
- ✅ Index page displays "Catholic Liturgy Tools" title
- ✅ Two sections: "Daily Messages" and "Daily Readings"
- ✅ Links point to correct files in subdirectories
- ✅ Links are reverse chronological (newest first)
- ✅ CSS styling looks clean and readable

---

## Development Workflow

### Standard Development Loop

1. **Make code changes** in `src/`
2. **Run generators**:
   ```bash
   catholic-liturgy generate-message
   catholic-liturgy generate-readings
   catholic-liturgy generate-index
   ```
3. **View results**: Open `_site/index.html` in browser
4. **Run tests**:
   ```bash
   pytest
   ```
5. **Verify coverage**:
   ```bash
   pytest --cov=src/catholic_liturgy_tools --cov-report=term-missing
   # Must be 90%+
   ```

---

## Key File Locations

### Source Code (to modify)

```
src/catholic_liturgy_tools/
├── cli.py                    # Update default paths
├── generator/
│   ├── message.py            # Change default output_dir
│   ├── readings.py           # Change default output_dir
│   └── index.py              # Major rewrite: HTML generation
```

### Tests (to update)

```
tests/
├── unit/
│   ├── test_cli.py           # Update default path assertions
│   ├── test_message.py       # Update output_dir tests
│   ├── test_readings_generator.py  # Update output_dir tests
│   └── test_index.py         # Rewrite for HTML generation
├── integration/
│   ├── test_message_workflow.py    # Update path expectations
│   └── test_index_workflow.py      # Major updates for HTML
└── e2e/
    ├── test_cli_generate.py  # Update path assertions
    └── test_cli_index.py     # Update for HTML output
```

### Contracts (reference specs)

```
specs/003-site-content-restructure/contracts/
├── cli-commands.md           # CLI interface specification
├── html-format.md            # HTML generation specification
└── github-actions.md         # Deployment workflow specification
```

---

## Testing Checklist

### Unit Tests
```bash
# Run specific test file
pytest tests/unit/test_index.py -v

# Run all unit tests
pytest tests/unit/ -v
```

**What to verify**:
- ✅ Default paths changed to `_site/messages/`, `_site/readings/`, `_site/`
- ✅ Custom paths still work (backward compatibility)
- ✅ HTML generation produces valid HTML5
- ✅ CSS is inline and correct
- ✅ Links use relative paths

### Integration Tests
```bash
pytest tests/integration/ -v
```

**What to verify**:
- ✅ End-to-end workflows generate correct structure
- ✅ Index page includes all generated content
- ✅ Files are written to correct locations

### E2E Tests
```bash
pytest tests/e2e/ -v
```

**What to verify**:
- ✅ CLI commands work with new defaults
- ✅ Output files exist in `_site/` structure
- ✅ Index HTML is valid and complete

### Coverage Check
```bash
pytest --cov=src/catholic_liturgy_tools --cov-report=term-missing --cov-fail-under=90
```

**Constitutional requirement**: Must maintain 90%+ coverage

---

## Common Development Tasks

### Add New HTML Elements to Index

1. **Reference**: `contracts/html-format.md`
2. **Modify**: `src/catholic_liturgy_tools/generator/index.py`
3. **Update tests**: `tests/unit/test_index.py`
4. **Verify output**: `open _site/index.html`

### Change CSS Styling

1. **Reference**: `contracts/html-format.md` (CSS section)
2. **Modify**: CSS in `src/catholic_liturgy_tools/generator/index.py`
3. **Test**: Generate index and view in browser
4. **Verify**: No layout breaks, readability maintained

### Update Workflow

1. **Reference**: `contracts/github-actions.md`
2. **Modify**: `.github/workflows/publish-content.yml`
3. **Test**: Push to feature branch, manually trigger workflow
4. **Verify**: Check gh-pages branch and live site

---

## Debugging Tips

### Issue: `_site/` directory not created

**Check**:
```bash
# Verify CLI installation
which catholic-liturgy

# Reinstall package
pip install -e .
```

### Issue: Index page empty or missing links

**Debug**:
```bash
# Check what files exist
ls -R _site/

# Run with verbose output (if implemented)
catholic-liturgy generate-index --verbose
```

**Common causes**:
- No message or readings files generated yet
- Incorrect path patterns in scanner functions
- Date format mismatch

### Issue: HTML not displaying correctly

**Verify**:
1. View page source in browser
2. Check for HTML validation errors (W3C validator)
3. Compare against `contracts/html-format.md` template
4. Verify CSS is inline and complete

### Issue: Links broken (404 errors)

**Check**:
- ✅ Links use relative paths (`messages/...`, `readings/...`)
- ✅ Files exist at expected locations
- ✅ Filenames match exactly (case-sensitive)
- ✅ No leading slashes in links

---

## One-Time Migration

**Note**: This is a development task, not part of CLI

### Manual Migration Steps

```bash
# 1. Generate all content with new structure
catholic-liturgy generate-message
catholic-liturgy generate-readings
catholic-liturgy generate-index

# 2. (Optional) Backup old files
mkdir _backup
cp -r _posts/ _backup/
cp -r readings/ _backup/
cp index.md _backup/

# 3. Delete old files (after verifying _site/ is correct)
rm -rf _posts/
rm -rf readings/
rm index.md

# 4. Update .gitignore to exclude _site/ locally
echo "_site/" >> .gitignore

# 5. Commit changes
git add .
git commit -m "Restructure site content to _site/ directory"
```

**Important**: Test thoroughly before deleting old files!

---

## GitHub Pages Setup (First Time)

### After Merging Feature

1. **Trigger workflow**:
   - Wait for scheduled run (daily at noon UTC)
   - OR manually trigger via GitHub Actions UI

2. **Verify gh-pages branch**:
   ```bash
   git fetch origin
   git checkout gh-pages
   ls -la
   # Should see: index.html, messages/, readings/
   ```

3. **Configure GitHub Pages**:
   - Go to repository Settings → Pages
   - Source: "Deploy from a branch"
   - Branch: `gh-pages`, Folder: `/ (root)`
   - Click "Save"

4. **Wait for deployment** (~1-2 minutes)

5. **Verify live site**:
   - Visit: https://etotten.github.io/catholic-liturgy-tools/
   - Check: Title, links, content all work

---

## Helpful Commands Reference

### Content Generation
```bash
# Generate for today
catholic-liturgy generate-message
catholic-liturgy generate-readings
catholic-liturgy generate-index

# Generate for specific date
catholic-liturgy generate-message --date 2025-12-25
catholic-liturgy generate-readings --date 2025-12-25
```

### Testing
```bash
# All tests
pytest

# Specific test type
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# With coverage
pytest --cov=src/catholic_liturgy_tools --cov-report=html
open htmlcov/index.html  # View coverage report
```

### Development Server (Optional)
```bash
# Serve _site/ locally for testing
cd _site/
python -m http.server 8000
# Visit: http://localhost:8000
```

---

## File Structure Quick Reference

### Before (v0.2.0)
```
<repo-root>/
├── _posts/YYYY-MM-DD-daily-message.md
├── readings/YYYY-MM-DD.html
└── index.md
```

### After (v0.3.0)
```
<repo-root>/
└── _site/
    ├── index.html
    ├── messages/YYYY-MM-DD-daily-message.md
    └── readings/YYYY-MM-DD.html
```

### Main Branch (source code)
```
<repo-root>/
├── src/                   # Source code
├── tests/                 # Test suite
├── specs/                 # Feature specifications
├── _site/                 # Generated (not committed)
└── [config files]
```

### gh-pages Branch (published)
```
<repo-root>/
├── index.html
├── messages/
└── readings/
```

---

## Next Steps After Implementation

1. ✅ Run full test suite and verify 90%+ coverage
2. ✅ Generate content locally and verify structure
3. ✅ Push to feature branch
4. ✅ Manually trigger GitHub Actions workflow
5. ✅ Verify gh-pages branch is correct
6. ✅ Configure GitHub Pages settings
7. ✅ Verify live site works
8. ✅ Create pull request
9. ✅ Perform one-time migration of existing content
10. ✅ Delete old files after verifying migration

---

## Support & Resources

### Documentation
- Feature Spec: `specs/003-site-content-restructure/spec.md`
- Implementation Plan: `specs/003-site-content-restructure/plan.md`
- Data Model: `specs/003-site-content-restructure/data-model.md`
- Contracts: `specs/003-site-content-restructure/contracts/`

### Constitution
- Location: `.specify/memory/constitution.md`
- Key Principle: Maintain 90%+ test coverage
- Version Policy: MINOR bump (0.2.0 → 0.3.0)

### Contacts
- Repository: https://github.com/etotten/catholic-liturgy-tools
- Issues: https://github.com/etotten/catholic-liturgy-tools/issues

---

## Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| `catholic-liturgy` command not found | Run `pip install -e .` |
| Tests failing after changes | Run `pytest -v` to see specific failures |
| Coverage below 90% | Run `pytest --cov-report=term-missing` to see uncovered lines |
| Index not generating | Check `_site/messages/` and `_site/readings/` have files |
| HTML looks wrong | Compare against `contracts/html-format.md` template |
| Workflow failing | Check GitHub Actions logs, verify permissions |
| gh-pages not updating | Verify workflow completed, check branch manually |
| Live site 404 | Check GitHub Pages settings, verify branch and folder |

---

**Ready to implement?** Start with updating `cli.py` default paths, then move to generators, then tests!
