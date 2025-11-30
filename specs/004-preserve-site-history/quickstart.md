# Quickstart Guide: Preserve Site Historical Content

**Feature**: 004-preserve-site-history  
**Date**: 2025-11-30  
**For**: Developers implementing this feature

## What This Feature Does

Fixes the site content preservation issue where the index page only shows the latest reading and message. After this fix, the site will accumulate all generated content over time, with the index page growing to show links to all historical messages and readings.

## The Problem

Currently, when content is generated:
1. A new message and reading are created
2. The `_site/` directory is NOT committed to Git
3. The next GitHub Actions run starts with a clean environment
4. Previous content is lost
5. Index page only shows the latest content

## The Solution

1. **Commit `_site/` to repository** after each content generation
2. Each workflow run starts with previous content present
3. New content is added to existing content
4. Index generator scans ALL files and includes them
5. Result: Accumulating content, growing index page

## High-Level Implementation Steps

### 1. Update GitHub Actions Workflow

**File**: `.github/workflows/publish-content.yml`

**What to change**: Add a new step after "Generate index page" step

**New step**:
```yaml
- name: Commit generated content to repository
  run: |
    git config user.name "github-actions[bot]"
    git config user.email "github-actions[bot]@users.noreply.github.com"
    git add _site/
    git diff --staged --quiet || git commit -m "Generated content for $(date +%Y-%m-%d)"
    git push
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Permission change**:
```yaml
permissions:
  contents: write   # Changed from 'read'
  pages: write
  id-token: write
```

**That's it for the workflow!** All other steps remain unchanged.

### 2. Verify Index Generator Behavior

**File**: `src/catholic_liturgy_tools/generator/index.py`

**What to verify**: The index generator already scans all files correctly. The functions `scan_message_files()` and `scan_readings_files()` discover all files in their respective directories.

**No changes needed** to the scanning logic - it already works! The problem was just that the `_site/` directory was being wiped between runs.

**Important**: The CLI commands do NOT commit to Git. They only generate files. The workflow commits. This allows manual experimentation without unwanted commits.

**Optional improvement**: Add defensive checks to ensure we're discovering all files, not just one.

### 3. Add Tests for Accumulation Behavior

**File**: `tests/e2e/test_cli_index.py` (or create if doesn't exist)

**Test scenario 1**: Multi-run accumulation
```python
def test_content_accumulates_across_runs():
    """Verify content persists across multiple generation runs."""
    # Generate content for Day 1
    # Verify 1 message, 1 reading exists
    
    # Generate content for Day 2  
    # Verify 2 messages, 2 readings exist (Day 1 + Day 2)
    
    # Generate content for Day 3
    # Verify 3 messages, 3 readings exist (all three days)
    
    # Verify index lists all 3 dates
    # Verify order is Day 3, Day 2, Day 1 (newest first)
```

**Test scenario 2**: Same-date overwrite
```python
def test_same_date_regeneration_overwrites():
    """Verify regenerating same date overwrites, doesn't duplicate."""
    # Generate content for Day 1
    # Regenerate content for Day 1
    # Verify still only 1 message file (not 2)
    # Verify still only 1 reading file (not 2)
    # Verify index lists Day 1 exactly once
```

## Testing Your Changes

### Local Testing

```bash
# 1. Clean _site directory
rm -rf _site/

# 2. Generate content for multiple dates
catholic-liturgy generate-message --date 2025-11-23
catholic-liturgy generate-readings --date 2025-11-23
catholic-liturgy generate-index

catholic-liturgy generate-message --date 2025-11-24
catholic-liturgy generate-readings --date 2025-11-24
catholic-liturgy generate-index

catholic-liturgy generate-message --date 2025-11-25
catholic-liturgy generate-readings --date 2025-11-25
catholic-liturgy generate-index

# 3. Verify accumulation
ls _site/messages/  # Should show 3 files
ls _site/readings/  # Should show 3 files

# 4. Check index page
open _site/index.html  # Should show 3 dates in each section

# 5. Run automated tests
python -m pytest tests/e2e/test_cli_index.py -v
python -m pytest tests/ --cov=src/catholic_liturgy_tools --cov-report=term-missing
```

### Workflow Testing

```bash
# 1. Push workflow changes to feature branch
git add .github/workflows/publish-content.yml
git commit -m "Add content preservation to workflow"
git push origin 004-preserve-site-history

# 2. Manually trigger workflow for first date
# Go to GitHub Actions tab → Publish Daily Content → Run workflow
# Select branch: 004-preserve-site-history
# Date: 2025-11-23

# 3. Verify commit created in branch
git pull origin 004-preserve-site-history
ls _site/messages/  # Should show 2025-11-23-daily-message.md

# 4. Manually trigger workflow for second date
# Date: 2025-11-24

# 5. Verify accumulation
git pull origin 004-preserve-site-history
ls _site/messages/  # Should show BOTH 2025-11-23 and 2025-11-24

# 6. Check deployed site
# Visit: https://etotten.github.io/catholic-liturgy-tools/
# Verify index shows both dates
```

## Success Criteria Checklist

- [ ] Workflow includes new commit step
- [ ] Workflow has `contents: write` permission
- [ ] Workflow runs successfully on first date
- [ ] Workflow commits `_site/` to repository
- [ ] Second workflow run starts with first run's content present
- [ ] Both dates' content exists after second run
- [ ] Index page lists both dates
- [ ] Dates are ordered newest first
- [ ] All links work (no broken links)
- [ ] Test coverage ≥ 90%
- [ ] E2E tests pass for multi-run accumulation
- [ ] E2E tests pass for same-date overwrite

## Common Issues and Solutions

### Issue: "nothing to commit" error in workflow

**Solution**: Use `git diff --staged --quiet ||` before commit to handle this gracefully:
```bash
git diff --staged --quiet || git commit -m "..."
```

### Issue: Permission denied when pushing

**Solution**: Verify `contents: write` permission is set and `GITHUB_TOKEN` is passed

### Issue: Index only shows one date despite multiple files existing

**Solution**: Check that `scan_message_files()` and `scan_readings_files()` return full lists, not just first item

### Issue: Merge conflicts in _site/

**Solution**: This shouldn't happen with GitHub Actions concurrency control, but if it does:
- Cancel in-progress workflow
- Pull latest changes
- Re-trigger workflow

## Rollback Plan

If issues arise:

```bash
# 1. Revert workflow changes
git revert <commit-sha-of-workflow-change>
git push origin 004-preserve-site-history

# 2. Manually commit any lost content
git add _site/
git commit -m "Preserve existing content"
git push

# 3. Re-evaluate approach
```

## Next Steps After Implementation

1. Monitor first few automated daily runs
2. Verify content continues to accumulate
3. Check site weekly to ensure index grows appropriately
4. Consider adding pagination if index becomes too long (future enhancement)

## Key Files to Modify

1. `.github/workflows/publish-content.yml` - Add commit step
2. `tests/e2e/test_cli_index.py` - Add accumulation tests
3. (Optional) `src/catholic_liturgy_tools/generator/index.py` - Add defensive checks

## Key Files to Review (No Changes Needed)

1. `src/catholic_liturgy_tools/generator/message.py` - Already creates files correctly
2. `src/catholic_liturgy_tools/generator/readings.py` - Already creates files correctly
3. `src/catholic_liturgy_tools/generator/index.py` - Already scans correctly

## Estimated Effort

- Workflow changes: 15 minutes
- Test additions: 1-2 hours  
- Testing and verification: 1 hour
- **Total: ~3 hours**

This is a small, focused fix with minimal code changes and high impact!
