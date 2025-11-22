# Research & Technical Decisions

**Feature**: GitHub Pages Daily Message  
**Branch**: 001-github-pages  
**Phase**: 0 (Research & Resolution)  
**Date**: 2025-11-22

## Purpose

This document resolves all "NEEDS CLARIFICATION" items from the Technical Context and documents key technical decisions with rationales.

---

## Research Areas

### 1. Jekyll Integration for GitHub Pages

**Question**: How to structure markdown files for optimal Jekyll compatibility?

**Decision**: Use Jekyll's `_posts/` directory with date-prefixed filenames and YAML frontmatter.

**Rationale**:
- Jekyll's convention for blog posts is `_posts/YYYY-MM-DD-title.md`
- YAML frontmatter provides metadata (title, date, layout)
- GitHub Pages automatically processes `_posts/` directory
- No custom Jekyll plugins needed (aligns with constraints)
- Index page can be root `index.md` (Jekyll default homepage)

**Implementation Details**:
```markdown
---
layout: post
title: "Daily Message for 2025-11-22"
date: 2025-11-22
---

# 2025-11-22

Hello Catholic World
```

**Alternatives Considered**:
- Custom directory structure: Rejected because requires Jekyll configuration
- No frontmatter: Rejected because Jekyll won't process files correctly
- Using `docs/` directory: Rejected because `_posts/` is Jekyll standard

---

### 2. File Organization and Output Directory

**Question**: Where should generated markdown files be stored?

**Decision**: Generate files in repository root `_posts/` directory for Jekyll, with `index.md` at root.

**Rationale**:
- Jekyll expects `_posts/` at repository root (or in configured directory)
- Root `index.md` becomes the homepage automatically
- GitHub Pages can deploy from root or `/docs` folder; root is simpler
- Keeps generated content separate from source code (`src/`)
- Easy to `.gitignore` if needed, or commit for versioning

**Directory Structure**:
```
Repository Root/
├── _posts/                          # Jekyll posts (generated)
│   ├── 2025-11-22-daily-message.md
│   └── 2025-11-23-daily-message.md
├── index.md                         # Generated index page
├── _config.yml                      # Jekyll config (minimal)
└── src/catholic_liturgy_tools/      # Python source code
```

**Alternatives Considered**:
- Generate in `docs/`: Possible but adds complexity, no benefit
- Generate in `src/`: Wrong location (source vs output)
- Separate output directory: Requires Jekyll configuration

---

### 3. GitHub Actions Workflow Strategy

**Question**: How should GitHub Actions workflow be structured and triggered?

**Decision**: Use workflow_dispatch (manual trigger) and schedule (cron) with Python execution steps.

**Rationale**:
- `workflow_dispatch` allows manual triggering (required for P3 and P4)
- `schedule` with cron enables daily automation
- Workflow runs Python CLI commands directly (reuses tested code)
- Commits generated files to repository
- GitHub Pages deployment is automatic once files are committed

**Workflow Structure**:
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

**Alternatives Considered**:
- Push trigger: Rejected because we want scheduled generation
- Separate Python script in workflow: Rejected to avoid duplication (use CLI)
- External deployment service: Rejected for simplicity (GitHub Actions + Pages sufficient)

---

### 4. GitHub API for Remote Workflow Triggering (P4)

**Question**: How to trigger GitHub Actions workflow from CLI?

**Decision**: Use GitHub REST API `POST /repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches` endpoint with personal access token (PAT).

**Rationale**:
- Official GitHub API for triggering `workflow_dispatch` events
- Requires PAT with `workflow` scope (user provides via environment variable)
- Standard REST API, well-documented, stable
- Python `requests` library sufficient for implementation
- Returns immediately (async trigger), user can check status on GitHub

**Implementation Approach**:
```python
import os
import requests

def trigger_workflow(workflow_file='publish-daily-message.yml'):
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable not set")
    
    url = f"https://api.github.com/repos/etotten/catholic-liturgy-tools/actions/workflows/{workflow_file}/dispatches"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {'ref': 'main'}
    
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.status_code == 204
```

**Alternatives Considered**:
- GitHub CLI (`gh`): Requires external dependency, CLI wraps API anyway
- PyGithub library: Overkill for single API call, adds dependency
- Manual trigger only: Rejected because spec requires CLI trigger (P4)

---

### 5. Date Handling and Timezone

**Question**: Which date should be used (UTC vs local timezone)?

**Decision**: Use system local date for message generation, document in README.

**Rationale**:
- GitHub Actions runs in UTC, but this is acceptable (generates "today's" message for UTC)
- Local CLI uses local date (generates "today's" message for developer's timezone)
- Per spec assumptions, no timezone conversion needed at this stage
- Keeps implementation simple (no pytz or zoneinfo complexity)
- Future enhancement can add timezone support if needed

**Implementation**:
```python
from datetime import date

def get_today():
    return date.today().strftime('%Y-%m-%d')
```

**Alternatives Considered**:
- Always use UTC: Confusing for local development
- Timezone configuration: Premature complexity (not in spec)
- Parse date from CLI argument: Out of scope (always "today")

---

### 6. Idempotency (Multiple Runs Per Day)

**Question**: What happens if the command runs multiple times in the same day?

**Decision**: Overwrite existing day's file, regenerate index without duplicates.

**Rationale**:
- File-based storage naturally handles overwrites
- Index generation scans `_posts/` directory and deduplicates by date
- Simple implementation (no state tracking needed)
- Aligns with spec edge case handling
- No harm in regenerating (content is deterministic)

**Implementation Strategy**:
- Message generation: Always write to `_posts/{date}-daily-message.md`
- Index generation: Parse all files in `_posts/`, extract dates, sort, deduplicate, write links

---

### 7. Testing Strategy

**Question**: How to achieve 90% coverage with E2E tests for CLI?

**Decision**: Three-tier testing approach (unit, integration, E2E).

**Rationale**:
- **Unit tests**: Test individual functions (message_generator, index_generator, file operations) with mocks
- **Integration tests**: Test file generation workflows with temporary directories
- **E2E tests**: Execute CLI commands in subprocess, verify file outputs (actual CLI behavior)
- pytest fixtures for temp directories and cleanup
- pytest-cov for coverage measurement and enforcement
- Mock GitHub API calls in unit/integration tests (use `responses` or `unittest.mock`)

**Coverage Targets**:
- Unit tests: Cover all business logic (generator functions, utils)
- Integration tests: Cover workflows (generate + verify file structure)
- E2E tests: Cover all CLI commands (one test per command per priority level)
- Aim for >90% automatically via comprehensive unit tests

**Tools**:
- pytest for test execution
- pytest-cov for coverage measurement
- unittest.mock for mocking (stdlib, no extra dependency)
- tempfile for temporary test directories

---

### 8. Error Handling Strategy

**Question**: What error handling is needed?

**Decision**: Explicit error messages for common failure modes, fail fast.

**Rationale**:
- File I/O errors: Check directory permissions, create if missing, report clearly
- GitHub API errors: Check for token, handle 401/403/404, provide helpful messages
- Date parsing errors: Not applicable (always use today's date)
- Jekyll compatibility: Validate frontmatter format before writing
- Exit codes: 0 for success, non-zero for errors (standard CLI practice)

**Error Scenarios**:
1. Missing write permissions for `_posts/` → Create directory or fail with clear message
2. Missing GITHUB_TOKEN (P4) → Error: "GITHUB_TOKEN environment variable required"
3. GitHub API failure (P4) → Error: "Failed to trigger workflow: {reason}"
4. Empty _posts directory for index → Generate empty index (not an error)

---

## Dependencies Finalized

### Production Dependencies
- **Python 3.11** (stdlib): `argparse`, `datetime`, `pathlib`, `os`, `sys`
- **requests**: For GitHub API calls (P4 only)
  - Version: `>=2.31.0`
  - Rationale: Widely used, stable, simple HTTP client

### Development Dependencies
- **pytest**: `>=7.4.0` (testing framework)
- **pytest-cov**: `>=4.1.0` (coverage measurement)
- **black**: `>=23.0.0` (code formatting)
- **ruff**: `>=0.1.0` (linting)

### External Services
- **GitHub Actions**: CI/CD automation (included with GitHub)
- **GitHub Pages**: Static site hosting (included with GitHub)
- **Jekyll**: Static site generator (provided by GitHub Pages, no installation needed)

---

## Configuration Files Needed

### 1. `_config.yml` (Jekyll Configuration)
Minimal configuration for GitHub Pages:
```yaml
title: Catholic Liturgy Tools - Daily Messages
description: Daily messages from Catholic Liturgy Tools
theme: minima  # GitHub Pages default theme
```

### 2. `.github/workflows/publish-daily-message.yml` (GitHub Actions)
Workflow for automated publishing (detailed in Research Area 3).

### 3. `pyproject.toml` Updates
Add `requests` dependency:
```toml
dependencies = [
    "requests>=2.31.0",
]
```

---

## Open Questions Resolved

All open questions from Technical Context have been resolved:
- ✅ Jekyll integration approach defined
- ✅ File organization structure determined
- ✅ GitHub Actions workflow strategy chosen
- ✅ GitHub API approach for CLI trigger (P4) documented
- ✅ Date/timezone handling clarified
- ✅ Idempotency strategy established
- ✅ Testing strategy defined
- ✅ Error handling approach outlined
- ✅ Dependencies finalized

No remaining "NEEDS CLARIFICATION" items.

---

## Summary

All technical decisions have been documented with clear rationales. The implementation can proceed to Phase 1 (Design & Contracts) with confidence. Key decisions:
1. Use Jekyll's `_posts/` convention with YAML frontmatter
2. Generate files at repository root for GitHub Pages
3. GitHub Actions with manual and scheduled triggers
4. GitHub REST API for remote workflow triggering (P4)
5. System local date (simple, no timezone complexity)
6. Overwrite-based idempotency (simple, effective)
7. Three-tier testing (unit/integration/E2E) for 90% coverage
8. Explicit error handling with helpful messages

Ready to proceed to Phase 1 (Data Model & Contracts).
