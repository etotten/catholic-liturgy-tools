# GitHub Actions Deployment Contract

**Feature**: 003-site-content-restructure  
**Date**: 2025-11-25

## Overview

This document defines the GitHub Actions workflow changes required to deploy generated content from `_site/` directory to the `gh-pages` branch for GitHub Pages publishing.

---

## Workflow File

**Location**: `.github/workflows/publish-content.yml`

**Changes**: Major restructuring of deployment steps

---

## Complete Updated Workflow

```yaml
name: Publish Daily Content

on:
  workflow_dispatch:    # Allow manual trigger
  schedule:
    - cron: '0 12 * * *'  # Run daily at 6 AM Central Time (noon UTC)

permissions:
  contents: write  # Required to push to gh-pages branch

jobs:
  generate-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install package
        run: |
          pip install -e .
      
      - name: Generate daily message
        run: |
          catholic-liturgy generate-message
      
      - name: Generate daily readings
        run: |
          catholic-liturgy generate-readings
      
      - name: Generate index page
        run: |
          catholic-liturgy generate-index
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./_site
          force_orphan: true
```

---

## Key Changes

### Removed Steps

❌ **Configure Git**  
❌ **Commit and push changes**  
❌ **Upload Pages artifact** (old deployment method)  
❌ **Separate deploy job**

**Rationale**: No longer committing to main branch, deploying directly to gh-pages

### Modified Steps

✅ **Permissions**: Simplified to only `contents: write`  
✅ **Single job**: Combined generate and deploy

### New Steps

✅ **Deploy to GitHub Pages** using peaceiris/actions-gh-pages action

---

## Step-by-Step Specification

### Step 1: Checkout Repository
```yaml
- name: Checkout repository
  uses: actions/checkout@v4
```

**Purpose**: Clone repository to runner  
**Required**: YES  
**Changes**: None from v0.2.0

### Step 2: Set up Python
```yaml
- name: Set up Python 3.11
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'
```

**Purpose**: Install Python runtime  
**Required**: YES  
**Changes**: None from v0.2.0

### Step 3: Install Package
```yaml
- name: Install package
  run: |
    pip install -e .
```

**Purpose**: Install catholic-liturgy-tools CLI  
**Required**: YES  
**Changes**: None from v0.2.0

### Step 4: Generate Daily Message
```yaml
- name: Generate daily message
  run: |
    catholic-liturgy generate-message
```

**Purpose**: Generate today's message  
**Output**: `_site/messages/YYYY-MM-DD-daily-message.md`  
**Changes**: Output path changed (command unchanged)

### Step 5: Generate Daily Readings
```yaml
- name: Generate daily readings
  run: |
    catholic-liturgy generate-readings
```

**Purpose**: Fetch and generate today's readings  
**Output**: `_site/readings/YYYY-MM-DD.html`  
**Changes**: Output path changed (command unchanged)

### Step 6: Generate Index Page
```yaml
- name: Generate index page
  run: |
    catholic-liturgy generate-index
```

**Purpose**: Generate HTML index linking to all content  
**Output**: `_site/index.html`  
**Changes**: Output path and format changed (command unchanged)

### Step 7: Deploy to GitHub Pages
```yaml
- name: Deploy to GitHub Pages
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./_site
    force_orphan: true
```

**Purpose**: Deploy `_site/` contents to `gh-pages` branch  
**Required**: YES  
**Changes**: **NEW STEP** replacing old deployment method

---

## Deployment Action Details

### Action: peaceiris/actions-gh-pages@v3

**Repository**: https://github.com/peaceiris/actions-gh-pages  
**License**: MIT  
**Popularity**: 10k+ stars, widely used  
**Maintenance**: Active

### Input Parameters

#### `github_token`
```yaml
github_token: ${{ secrets.GITHUB_TOKEN }}
```
- **Required**: YES
- **Type**: String (secret)
- **Purpose**: Authenticate for pushing to gh-pages branch
- **Source**: Automatically provided by GitHub Actions

#### `publish_dir`
```yaml
publish_dir: ./_site
```
- **Required**: YES
- **Type**: String (directory path)
- **Purpose**: Specify which directory contents to deploy
- **Value**: `./_site` (relative to repository root)

#### `force_orphan`
```yaml
force_orphan: true
```
- **Required**: NO (but recommended)
- **Type**: Boolean
- **Default**: `false`
- **Purpose**: Create orphan branch (no git history) for cleaner deployments
- **Benefit**: Keeps gh-pages branch lightweight, prevents history bloat

---

## Workflow Permissions

### Before (v0.2.0)
```yaml
permissions:
  contents: write  # Push commits to main
  pages: write     # Deploy to GitHub Pages
  id-token: write  # For Pages deployment
```

### After (v0.3.0)
```yaml
permissions:
  contents: write  # Push to gh-pages branch only
```

**Changes**:
- ❌ Removed `pages: write` (not using GitHub Pages deployment action)
- ❌ Removed `id-token: write` (not needed)
- ✅ Kept `contents: write` (required for pushing to gh-pages)

---

## Branch Strategy

### Main Branch
- **Contains**: Source code, specs, documentation
- **Generated Files**: `_site/` directory created by generators
- **Commits**: No automatic commits from GitHub Actions
- **Purpose**: Development and source control

### gh-pages Branch
- **Contains**: Only `_site/` directory contents (flattened to root)
- **Generated By**: GitHub Actions using peaceiris/actions-gh-pages
- **Commits**: Automatic commits on each workflow run
- **History**: Orphan (no shared history with main)
- **Purpose**: Publishing to GitHub Pages

### Branch Content Mapping

**Main Branch**:
```
<repo-root>/
├── src/
├── tests/
├── specs/
├── _site/          # Generated, not committed
│   ├── index.html
│   ├── messages/
│   └── readings/
└── [other files]
```

**gh-pages Branch** (after deployment):
```
<repo-root>/
├── index.html      # From _site/index.html
├── messages/       # From _site/messages/
└── readings/       # From _site/readings/
```

---

## Deployment Flow Diagram

```
┌─────────────────────────────────────────────┐
│  1. Workflow Triggered (schedule/manual)    │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│  2. Checkout main branch                    │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│  3. Install Python & package                │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│  4. Generate content to _site/              │
│     - messages/YYYY-MM-DD-daily-message.md  │
│     - readings/YYYY-MM-DD.html              │
│     - index.html                            │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│  5. peaceiris/actions-gh-pages              │
│     - Reads _site/ directory                │
│     - Creates/updates gh-pages branch       │
│     - Force pushes contents (orphan)        │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│  6. GitHub Pages serves from gh-pages       │
│     https://etotten.github.io/              │
│           catholic-liturgy-tools/           │
└─────────────────────────────────────────────┘
```

---

## Error Handling

### Generation Failures

**Scenario**: Any `generate-*` command fails

**Behavior**:
- Workflow stops at failed step
- No deployment occurs
- Exit code non-zero
- GitHub Actions UI shows failure

**Recovery**: Fix issue and re-run workflow

### Deployment Failures

**Scenario**: peaceiris/actions-gh-pages fails

**Possible Causes**:
- Permissions issue (missing `contents: write`)
- Invalid `publish_dir` path
- GitHub API issues

**Behavior**:
- Workflow fails at deployment step
- `_site/` directory was generated successfully
- No changes to gh-pages branch

**Recovery**: Check permissions, verify path, re-run

---

## GitHub Pages Configuration

### Repository Settings

**Navigate**: Settings → Pages

**Required Configuration**:
- **Source**: Deploy from a branch
- **Branch**: `gh-pages`
- **Folder**: `/ (root)`

**Important**: This configuration must be set **manually** after first deployment

### First-Time Setup Steps

1. ✅ Merge restructuring feature to main
2. ✅ Run GitHub Actions workflow (manually or wait for schedule)
3. ✅ Verify `gh-pages` branch is created
4. ✅ Go to repository Settings → Pages
5. ✅ Select "Deploy from a branch"
6. ✅ Choose `gh-pages` branch, `/ (root)` folder
7. ✅ Save configuration
8. ✅ Wait for Pages build (~1-2 minutes)
9. ✅ Visit https://etotten.github.io/catholic-liturgy-tools/

---

## Testing Strategy

### Local Testing
```bash
# Generate content locally
catholic-liturgy generate-message
catholic-liturgy generate-readings
catholic-liturgy generate-index

# Verify _site/ structure
ls -R _site/

# Open index in browser
open _site/index.html  # macOS
# or
xdg-open _site/index.html  # Linux
```

### Workflow Testing

**On Feature Branch**:
1. Push feature branch to remote
2. Manually trigger workflow on feature branch
3. Verify gh-pages branch is updated
4. Check GitHub Pages deployment
5. Verify site works at live URL

**Before Merge**:
- ✅ Workflow completes successfully
- ✅ gh-pages branch contains correct files
- ✅ Live site shows new structure
- ✅ All links work correctly

---

## Rollback Strategy

### If Deployment Fails

**Option 1**: Revert main branch
```bash
git revert <commit-hash>
git push origin main
```

**Option 2**: Restore gh-pages branch
```bash
git checkout gh-pages
git reset --hard <previous-commit>
git push --force origin gh-pages
```

**Option 3**: Manual fix
- Fix issue in main branch
- Re-run workflow
- Verify deployment

---

## Monitoring & Verification

### Workflow Success Indicators
- ✅ All generation steps complete
- ✅ Deploy step shows success
- ✅ gh-pages branch commit appears
- ✅ Workflow duration ~2-3 minutes

### Deployment Verification Checklist
- [ ] gh-pages branch exists
- [ ] Branch contains only site files (no src/, tests/, etc.)
- [ ] index.html is at branch root
- [ ] messages/ and readings/ subdirectories exist
- [ ] Site loads at live URL
- [ ] Links navigate correctly
- [ ] No 404 errors

---

## Summary

✅ **Simplified workflow** - Single job, cleaner steps  
✅ **Standard deployment** - Using peaceiris/actions-gh-pages  
✅ **Clean separation** - Main for source, gh-pages for publishing  
✅ **Orphan history** - Keeps gh-pages lightweight  
✅ **No main commits** - Actions don't clutter source history  
✅ **Easy rollback** - Both main and gh-pages can be reverted
