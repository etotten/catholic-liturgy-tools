# Quickstart Guide: GitHub Pages Daily Message

**Feature**: GitHub Pages Daily Message  
**Branch**: 001-github-pages  
**Phase**: 1 (Design & Contracts)  
**Date**: 2025-11-22

## Purpose

This guide helps developers quickly understand, set up, and work on the GitHub Pages Daily Message feature. It covers local development, testing, and GitHub Actions integration.

---

## Overview

This feature adds daily message generation and publishing capabilities to the Catholic Liturgy Tools project:
- **P1**: Generate daily messages locally (`generate-message` command)
- **P2**: Generate index page with links (`generate-index` command)
- **P3**: Automated publishing via GitHub Actions
- **P4**: Remote workflow triggering (`trigger-publish` command)

---

## Prerequisites

- **Python 3.11** or higher
- **Git** installed and repository cloned
- **GitHub account** (for P3/P4 features)
- **GitHub Personal Access Token** (for P4 only, with `workflow` scope)

---

## Quick Setup

### 1. Install Development Environment

```bash
# Navigate to repository root
cd catholic-liturgy-tools

# Create virtual environment (if not already created)
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Install package in editable mode with dev dependencies
pip install -e ".[dev]"
```

### 2. Verify Installation

```bash
# Check CLI is working
catholic-liturgy --version

# Should output: catholic-liturgy 0.1.0 (or current version)
```

---

## Local Development Workflow

### Generate a Daily Message (P1)

```bash
# Generate message for today
catholic-liturgy generate-message

# Output: Generated daily message for 2025-11-22
#         File: _posts/2025-11-22-daily-message.md

# Verify file was created
cat _posts/2025-11-22-daily-message.md
```

**Expected Output**:
```markdown
---
layout: post
title: "Daily Message for 2025-11-22"
date: 2025-11-22
---

# 2025-11-22

Hello Catholic World
```

### Generate Index Page (P2)

```bash
# First, generate a few messages (optionally backdate for testing)
catholic-liturgy generate-message

# Generate the index
catholic-liturgy generate-index

# Output: Generated index page with 1 messages
#         File: index.md

# View the index
cat index.md
```

**Expected Output**:
```markdown
---
layout: page
title: "Catholic Liturgy Tools - Daily Messages"
---

# Catholic Liturgy Tools - Daily Messages

## Recent Messages

- [Daily Message for 2025-11-22](_posts/2025-11-22-daily-message.md)
```

---

## Running Tests

### Run All Tests

```bash
# Run all tests with coverage
pytest

# Should output: Coverage report showing 90%+ coverage
```

### Run Specific Test Suites

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# E2E tests only
pytest tests/e2e/

# Specific test file
pytest tests/unit/test_message.py

# Specific test function
pytest tests/e2e/test_cli_generate.py::test_generate_message_creates_file
```

### Generate Coverage Report

```bash
# Run tests and generate HTML coverage report
pytest --cov-report=html

# Open in browser
open htmlcov/index.html  # macOS
# or: start htmlcov/index.html  # Windows
# or: xdg-open htmlcov/index.html  # Linux
```

---

## GitHub Actions Setup (P3)

### 1. Enable GitHub Pages

1. Go to repository settings on GitHub
2. Navigate to **Pages** section
3. Set source to **Deploy from a branch**
4. Select branch: `main` (or your default branch)
5. Set folder: `/ (root)`
6. Click **Save**

### 2. Workflow File

The workflow file is located at `.github/workflows/publish-daily-message.yml`. It will be created during implementation.

**Preview**:
```yaml
name: Publish Daily Message
on:
  workflow_dispatch:    # Manual trigger
  schedule:
    - cron: '0 12 * * *'  # Daily at noon UTC
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -e .
      - run: catholic-liturgy generate-message
      - run: catholic-liturgy generate-index
      - run: git config user.name "GitHub Actions"
      - run: git config user.email "actions@github.com"
      - run: git add _posts/ index.md
      - run: git commit -m "Add daily message for $(date +%Y-%m-%d)" || echo "No changes"
      - run: git push
```

### 3. Manual Workflow Trigger (via GitHub UI)

1. Go to repository on GitHub
2. Click **Actions** tab
3. Select **Publish Daily Message** workflow
4. Click **Run workflow** button
5. Select branch (usually `main`)
6. Click **Run workflow**
7. Wait for workflow to complete (should take < 2 minutes)
8. Visit GitHub Pages site to see results

---

## Remote Workflow Trigger (P4)

### 1. Create GitHub Personal Access Token

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click **Generate new token (classic)**
3. Give it a descriptive name: `Catholic Liturgy Tools - Workflow Trigger`
4. Select scope: **workflow** (allows triggering workflows)
5. Set expiration as desired (30/60/90 days, or no expiration)
6. Click **Generate token**
7. **Copy the token** (you won't see it again!)

### 2. Set Environment Variable

```bash
# macOS/Linux (add to ~/.bashrc or ~/.zshrc for persistence)
export GITHUB_TOKEN=ghp_your_token_here

# Windows PowerShell
$env:GITHUB_TOKEN="ghp_your_token_here"

# Windows CMD
set GITHUB_TOKEN=ghp_your_token_here
```

### 3. Trigger Workflow from CLI

```bash
# Trigger the workflow remotely
catholic-liturgy trigger-publish

# Output: Successfully triggered GitHub Actions workflow
#         Workflow: publish-daily-message.yml
#         Check status at: https://github.com/etotten/catholic-liturgy-tools/actions
```

### 4. Verify Workflow Run

1. Visit the URL from the output message
2. You should see a new workflow run in progress
3. Wait for completion (< 2 minutes)
4. Check GitHub Pages site for updated content

---

## Jekyll Local Preview (Optional)

To preview the GitHub Pages site locally before publishing:

### 1. Install Jekyll

```bash
# macOS (requires Homebrew)
brew install ruby
gem install bundler jekyll

# Linux (Ubuntu/Debian)
sudo apt-get install ruby-full build-essential zlib1g-dev
gem install bundler jekyll

# Windows: Use RubyInstaller (https://rubyinstaller.org/)
```

### 2. Create Gemfile

```bash
# In repository root, create Gemfile:
cat > Gemfile << 'EOF'
source "https://rubygems.org"
gem "github-pages", group: :jekyll_plugins
EOF
```

### 3. Install Dependencies

```bash
bundle install
```

### 4. Serve Locally

```bash
bundle exec jekyll serve

# Output: Server running at http://127.0.0.1:4000/
```

### 5. View in Browser

Open http://127.0.0.1:4000/ to see the site.

**Note**: Jekyll preview is optional and not required for development. The GitHub Actions workflow handles publishing automatically.

---

## Directory Structure

After running the commands, your repository will have:

```
Repository Root/
├── _posts/                          # Generated daily messages
│   ├── 2025-11-22-daily-message.md
│   ├── 2025-11-23-daily-message.md
│   └── ...
├── index.md                         # Generated index page
├── _config.yml                      # Jekyll configuration (P3)
├── src/
│   └── catholic_liturgy_tools/
│       ├── __init__.py
│       ├── cli.py                   # Updated with new commands
│       ├── generator/
│       │   ├── message.py           # Message generation logic
│       │   └── index.py             # Index generation logic
│       ├── github/
│       │   └── actions.py           # GitHub API (P4)
│       └── utils/
│           ├── file_ops.py
│           └── date_utils.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── .github/
    └── workflows/
        └── publish-daily-message.yml  # GitHub Actions workflow (P3)
```

---

## Common Tasks

### Task: Add a New Message Manually

```bash
# Generate message for today
catholic-liturgy generate-message

# Update the index
catholic-liturgy generate-index

# Commit and push (if working on feature branch)
git add _posts/ index.md
git commit -m "Add daily message for $(date +%Y-%m-%d)"
git push
```

### Task: Clean Generated Files

```bash
# Remove all generated files
rm -rf _posts/
rm -f index.md

# Regenerate from scratch
catholic-liturgy generate-message
catholic-liturgy generate-index
```

### Task: Test Full Workflow Locally

```bash
# 1. Generate message
catholic-liturgy generate-message

# 2. Generate index
catholic-liturgy generate-index

# 3. Verify files exist
ls -la _posts/
cat index.md

# 4. Run tests
pytest

# 5. Check coverage
pytest --cov-report=term-missing
```

### Task: Debug GitHub Actions

```bash
# Check workflow file syntax
cat .github/workflows/publish-daily-message.yml

# View recent workflow runs
gh run list  # Requires GitHub CLI

# View specific run logs
gh run view <run-id>  # Requires GitHub CLI
```

---

## Troubleshooting

### Issue: `catholic-liturgy` command not found

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall package
pip install -e ".[dev]"
```

### Issue: Permission denied when writing files

**Solution**:
```bash
# Check directory permissions
ls -la

# Ensure you have write permissions
chmod u+w .
```

### Issue: `GITHUB_TOKEN` not set (P4)

**Solution**:
```bash
# Set environment variable
export GITHUB_TOKEN=ghp_your_token_here

# Verify it's set
echo $GITHUB_TOKEN
```

### Issue: GitHub Actions workflow not found (P4)

**Solution**:
- Ensure `.github/workflows/publish-daily-message.yml` exists
- Ensure workflow file is committed and pushed to GitHub
- Verify workflow name matches the one specified in `trigger-publish` command

### Issue: Tests failing with import errors

**Solution**:
```bash
# Reinstall package in editable mode
pip install -e ".[dev]"

# Verify installation
pip list | grep catholic-liturgy-tools
```

### Issue: Coverage below 90%

**Solution**:
```bash
# Generate detailed coverage report
pytest --cov-report=term-missing

# Identify uncovered lines (shown with `!!!!!`)
# Add tests for those lines
```

---

## Development Best Practices

1. **Always activate virtual environment** before working
2. **Run tests before committing** (ensure nothing breaks)
3. **Check coverage** (must be 90%+)
4. **Write E2E tests** for CLI commands (constitutional requirement)
5. **Keep it simple** (avoid premature abstractions)
6. **Document as you go** (update README with new commands)
7. **Follow thin-slice approach** (implement P1, then P2, then P3, then P4)

---

## Next Steps

After reading this guide:

1. **Set up local environment** (install dependencies)
2. **Generate your first message** (`generate-message`)
3. **Run the tests** (`pytest`)
4. **Implement priority P1** (if you're developing)
5. **Move to P2, P3, P4** incrementally

---

## Resources

- **Feature Spec**: [spec.md](./spec.md)
- **Implementation Plan**: [plan.md](./plan.md)
- **Data Model**: [data-model.md](./data-model.md)
- **CLI Contracts**: [contracts/cli-commands.md](./contracts/cli-commands.md)
- **Constitution**: [.specify/memory/constitution.md](../../.specify/memory/constitution.md)
- **Jekyll Docs**: https://jekyllrb.com/docs/
- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **GitHub Pages Docs**: https://docs.github.com/en/pages

---

## Summary

This quickstart guide provides everything needed to:
- ✅ Set up local development environment
- ✅ Generate messages and index locally (P1, P2)
- ✅ Run comprehensive tests with coverage
- ✅ Configure GitHub Actions (P3)
- ✅ Trigger workflows remotely (P4)
- ✅ Troubleshoot common issues

Happy coding! 🎉
