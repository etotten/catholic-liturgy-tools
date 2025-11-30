# GitHub Actions Workflow Contract

**Feature**: 004-preserve-site-history  
**Date**: 2025-11-30

## Overview

This contract defines the required changes to the `publish-content.yml` GitHub Actions workflow to enable content accumulation and preservation.

## Current Workflow Flow

```yaml
jobs:
  generate-and-deploy:
    steps:
      1. Checkout repository
      2. Setup Python 3.13
      3. Install package
      4. Generate daily message         # Creates/overwrites file
      5. Generate daily readings        # Creates/overwrites file
      6. Generate index page            # Scans existing files
      7. Setup Pages
      8. Upload artifact (_site/)       # Uploads current _site/ content
      9. Deploy to GitHub Pages         # Deploys to gh-pages branch

# PROBLEM: _site/ exists only in workflow run, not committed to repository
# Next run starts fresh, previous content lost
```

## Required Workflow Flow

```yaml
jobs:
  generate-and-deploy:
    steps:
      1. Checkout repository
      2. Setup Python 3.13
      3. Install package
      4. Generate daily message         # Creates/overwrites file
      5. Generate daily readings        # Creates/overwrites file
      6. Generate index page            # Scans ALL existing files
      7. *** NEW: Commit _site/ to repository ***
      8. Setup Pages
      9. Upload artifact (_site/)       # Uploads complete accumulated content
      10. Deploy to GitHub Pages        # Deploys all historical content

# SOLUTION: _site/ committed to main branch, persists between runs
# Next run starts with all previous content, adds to it
```

## New Step: Commit Generated Content

**Step Name**: `Commit generated content to repository`

**Position**: After `Generate index page`, before `Setup Pages`

**Purpose**: Persist generated content in Git so it survives between workflow runs

**Requirements**:
- MUST commit all files in `_site/` directory
- MUST include both new and existing content files
- MUST push to the branch that triggered the workflow
- MUST handle case where no changes exist (nothing to commit)
- MUST configure Git user for commits
- MUST use meaningful commit message with date

**Pseudo-Implementation**:
```yaml
- name: Commit generated content to repository
  run: |
    # Configure Git for commits
    git config user.name "github-actions[bot]"
    git config user.email "github-actions[bot]@users.noreply.github.com"
    
    # Stage all _site/ content
    git add _site/
    
    # Commit if there are changes
    git diff --staged --quiet || git commit -m "Generated content for $(date +%Y-%m-%d)"
    
    # Push to current branch
    git push
  env:
    # Use GITHUB_TOKEN for authentication
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Edge Cases Handled**:
- No changes to commit (idempotent - safe to run multiple times)
- Content already committed manually
- Workflow triggered from feature branch (commits to that branch)
- Multiple workflow runs queued (GitHub Actions serializes by default)

**Permissions Required**:
```yaml
permissions:
  contents: write   # CHANGED: Need write permission to commit
  pages: write      # EXISTING: Deploy to Pages
  id-token: write   # EXISTING: OIDC authentication
```

## Deployment Step Behavior

**Step Name**: `Upload artifact` (existing step, no changes)

**Requirements**:
- MUST upload entire `_site/` directory
- MUST include all files (accumulated content + newly generated)
- Upload size grows over time as content accumulates

**Step Name**: `Deploy to GitHub Pages` (existing step, no changes)

**Requirements**:
- MUST deploy all uploaded content
- gh-pages branch receives complete _site/ contents
- Historical content visible on published site

## Workflow Triggers (No Changes)

**Existing Triggers Remain**:
- `workflow_dispatch`: Manual trigger with optional date parameter
- `push`: Automatic on push to main or 003-* branches  
- `schedule`: Daily at 6 AM Central (noon UTC)

**Behavior with Triggers**:
- **Manual trigger**: Generates content for specified date, commits to current branch
- **Scheduled run**: Generates content for today, commits to main branch
- **Push trigger**: Generates content for today, commits to pushed branch

## Concurrency Control (No Changes)

**Existing Concurrency Settings**:
```yaml
concurrency:
  group: "pages"
  cancel-in-progress: false
```

**Why This Works**:
- Prevents multiple deployments from running simultaneously
- Workflows queue if triggered while one is running
- Git push conflicts avoided by serialization
- Content accumulation preserved across queued runs

## Environment Configuration (No Changes)

**Existing Environment**:
```yaml
environment:
  name: github-pages
  url: ${{ steps.deployment.outputs.page_url }}
```

**No changes needed** - Environment configuration remains identical

## Date Parameter Handling (No Changes)

**Existing Behavior**:
```yaml
workflow_dispatch:
  inputs:
    date:
      description: 'Date to generate content for (YYYY-MM-DD, leave empty for today)'
      required: false
      type: string
```

**Usage in Steps**:
```bash
# Message generation
if [ -n "${{ inputs.date }}" ]; then
  catholic-liturgy generate-message --date "${{ inputs.date }}"
else
  catholic-liturgy generate-message
fi

# Readings generation
if [ -n "${{ inputs.date }}" ]; then
  catholic-liturgy generate-readings --date "${{ inputs.date }}"
else
  catholic-liturgy generate-readings
fi
```

**No changes needed** - Date handling already correct

## Testing Contract

### Test: Workflow Accumulates Content Over Multiple Runs

**Setup**:
```bash
# Start with clean _site/ in repository
git rm -rf _site/
git commit -m "Clean _site for test"
git push
```

**Test Steps**:
1. Trigger workflow for 2025-11-23
   - Verify commit created with _site/messages/2025-11-23-daily-message.md
   - Verify commit created with _site/readings/2025-11-23.html
   - Verify _site/index.html committed
   - Verify gh-pages contains all 3 files

2. Trigger workflow for 2025-11-24
   - Verify new commit created
   - Verify _site/ now contains:
     - messages/2025-11-23-daily-message.md (from previous run)
     - messages/2025-11-24-daily-message.md (new)
     - readings/2025-11-23.html (from previous run)
     - readings/2025-11-24.html (new)
     - index.html (regenerated with both dates)
   - Verify gh-pages contains all 5 files
   - Verify index page on live site shows both dates

3. Trigger workflow for 2025-11-25
   - Verify new commit created
   - Verify _site/ now contains 6 files (3 messages, 3 readings)
   - Verify gh-pages contains all 7 files (6 content + 1 index)
   - Verify index page shows all 3 dates in correct order

**Expected Result**: Each run adds to previous content, nothing deleted

---

### Test: Same-Date Regeneration

**Setup**:
```bash
# Generate content for a date
# Trigger workflow for 2025-11-23
# Verify initial content committed
```

**Test Steps**:
1. Trigger workflow again for 2025-11-23
   - Verify commit created (even if content identical)
   - Verify only 1 message file for 2025-11-23 (not duplicated)
   - Verify only 1 readings file for 2025-11-23 (not duplicated)
   - Verify index shows 2025-11-23 exactly once

**Expected Result**: Overwrite behavior works, no duplicates

---

### Test: No Changes to Commit

**Setup**:
```bash
# Generate content and commit
# Trigger workflow for 2025-11-23
# Verify content committed
```

**Test Steps**:
1. Trigger workflow again for 2025-11-23 (same date, no code changes)
2. Verify workflow completes successfully
3. Verify "nothing to commit" is handled gracefully (no error)
4. Verify deployment still succeeds

**Expected Result**: Workflow handles "no changes" case without failing

---

### Test: Feature Branch Deployment

**Setup**:
```bash
# Create feature branch
git checkout -b test-feature
git push origin test-feature
```

**Test Steps**:
1. Trigger workflow from test-feature branch
2. Verify commit is added to test-feature branch (not main)
3. Verify gh-pages deployment uses test-feature content
4. Verify main branch is unaffected

**Expected Result**: Branch isolation works correctly

## Summary of Changes

**Only One New Step Required**:
- Add "Commit generated content to repository" step after index generation

**Only One Permission Change Required**:
- Change `contents: read` to `contents: write`

**All Other Steps Unchanged**:
- Checkout, Python setup, package installation
- Content generation commands
- Pages setup and deployment

**Minimal Risk**:
- Single focused change
- Existing functionality preserved
- Backward compatible
- Easily testable
- Easily reversible if issues arise

## Implementation Notes

**Why commit to source branch instead of directly to gh-pages?**
- Source branch contains full history in _site/
- gh-pages is deployment target (can be rebuilt from source)
- Separation of concerns: source = storage, gh-pages = deployment
- Allows review of generated content via source branch commits

**Why push before deployment instead of after?**
- Ensures content is persisted even if deployment fails
- Failed deployment can be retried without re-generating content
- Git becomes single source of truth

**Why use github-actions[bot] as committer?**
- Standard practice for automated commits
- Clearly identifies commits as automation-generated
- No personal credentials needed
- Uses built-in GITHUB_TOKEN authentication
