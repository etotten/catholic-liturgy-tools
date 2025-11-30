# Research: Preserve Site Historical Content

**Feature**: 004-preserve-site-history  
**Date**: 2025-11-30  
**Phase**: 0 - Outline & Research

## Problem Analysis

### Root Cause Investigation

**Decision**: The issue stems from the GitHub Actions workflow not preserving `_site/` directory content between runs

**Rationale**: 
- Examined current implementation in `src/catholic_liturgy_tools/generator/index.py`
- The index generator already scans directories: `scan_message_files()` and `scan_readings_files()` 
- These functions correctly discover all files in `_site/messages/` and `_site/readings/`
- The generator code itself is **not the problem** - it already lists all discovered files
- The problem is that the `_site/` directory is being wiped out between GitHub Actions runs
- GitHub Actions workflows run in clean environments, so generated content doesn't persist unless explicitly committed

**Alternatives Considered**:
1. ❌ Modify index.py to scan files differently - Rejected: Code already scans all files correctly
2. ❌ Cache _site/ directory between workflow runs - Rejected: Doesn't provide Git versioning or durability
3. ✅ **Commit _site/ to repository** - Selected: Provides versioning, durability, and accumulation

### GitHub Actions Best Practices for Content Accumulation

**Decision**: Modify workflow to commit generated content back to the source branch before deploying to gh-pages

**Rationale**:
- Standard pattern for content-generating workflows: generate → commit → deploy
- Ensures content persists in Git history (recovery capability)
- Allows the index generator to discover previously generated files on next run
- The gh-pages branch deployment can pull from the committed _site/ directory
- Follows immutable infrastructure pattern: each deployment contains complete history

**Implementation Pattern**:
```yaml
# Pseudo-workflow steps:
1. Checkout repository
2. Run CLI commands to generate new content (messages/readings for today)
3. Commit _site/ changes to current branch (workflow step, NOT CLI)
4. Deploy entire _site/ directory to gh-pages branch
```

**Note**: The CLI commands remain pure content generators. They do not perform Git operations. Only the workflow commits changes. This allows users to experiment manually without unwanted commits.

**Alternatives Considered**:
1. ❌ Store content in external database - Rejected: Adds complexity, violates simplicity principle
2. ❌ Use GitHub releases for storage - Rejected: Not designed for this use case
3. ❌ Separate content repository - Rejected: Unnecessary complexity for small-scale project

### File Overwrite Strategy for Same-Date Regeneration

**Decision**: Allow overwrite when regenerating content for existing dates

**Rationale**:
- User explicitly chose this option during clarification
- Enables bug fixes and corrections
- Git history preserves previous versions
- Standard behavior for content management systems
- No additional logic needed - file write naturally overwrites

**Alternatives Considered**:
1. ❌ Skip existing files - Rejected: Prevents corrections
2. ❌ Version files (file-v2.html) - Rejected: Adds complexity, clutters directory
3. ✅ **Overwrite with Git safety net** - Selected: Simple, with recovery via Git

### Directory Scanning and Discovery

**Decision**: Continue using existing glob patterns for file discovery

**Rationale**:
- Current implementation in index.py already works correctly
- `Path.glob("*-daily-message.md")` discovers all message files
- `Path.glob("*.html")` discovers all readings files  
- Both are sorted reverse chronologically (newest first)
- No changes needed to discovery logic

**Technology**: Python `pathlib.Path.glob()` - Standard library, reliable, well-tested

## Technology Choices

### Git Operations for Content Persistence

**Decision**: Use Git CLI commands via GitHub Actions for committing generated content

**Rationale**:
- GitHub Actions provides git automatically in workflows
- Standard approach: `git add _site/`, `git commit`, `git push`
- No additional dependencies needed
- Well-documented and reliable
- Aligns with existing workflow patterns in the project

**Example Commands**:
```bash
git config user.name "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"
git add _site/
git commit -m "Generated content for YYYY-MM-DD"
git push
```

**Alternatives Considered**:
1. ❌ Use GitHub API for commits - Rejected: More complex than CLI
2. ❌ Use git Python library (GitPython) - Rejected: Adds dependency, workflow already has git
3. ✅ **Git CLI in workflow** - Selected: Simple, no dependencies, standard practice

### Testing Strategy for Accumulation Behavior

**Decision**: Multi-run E2E tests that verify content persists across generations

**Rationale**:
- Constitution requires 90% coverage and E2E tests for all CLI options
- Must verify that content accumulates, not just that generation succeeds
- Test approach:
  1. Generate content for Day 1, verify file exists
  2. Generate content for Day 2, verify both Day 1 and Day 2 files exist
  3. Regenerate Day 1, verify overwrite works and Day 2 remains
  4. Verify index page lists all content in correct order

**Testing Framework**: pytest (already in use)

**Alternatives Considered**:
1. ❌ Manual testing only - Rejected: Constitution requires automated tests
2. ❌ Unit tests only - Rejected: Doesn't verify integration with filesystem
3. ✅ **E2E + Unit tests** - Selected: Comprehensive coverage, verifies behavior

### GitHub Actions Workflow Modification

**Decision**: Update existing `publish-site.yml` workflow to add commit step before deployment

**Rationale**:
- Existing workflow already generates content and deploys to gh-pages
- Need to insert one additional step: commit _site/ to source branch
- Minimal change to existing proven workflow
- Preserves all existing functionality

**Workflow Structure**:
```yaml
jobs:
  publish:
    steps:
      - name: Checkout
      - name: Setup Python
      - name: Install dependencies
      - name: Generate content (messages + readings)
      - name: Generate index
      - name: Commit _site/ to repository    # NEW STEP
      - name: Deploy to gh-pages branch     # EXISTING STEP
```

**Alternatives Considered**:
1. ❌ Create separate workflow for commits - Rejected: Splits responsibility unnecessarily
2. ❌ Use scheduled commits separate from deployment - Rejected: Risk of divergence
3. ✅ **Single integrated workflow** - Selected: Atomic operation, simpler to maintain

## Implementation Risks and Mitigations

### Risk: Merge Conflicts in _site/ Directory

**Likelihood**: Medium  
**Impact**: Medium  
**Mitigation**: 
- _site/ directory contains generated files only, no manual editing
- Conflicts would only occur if workflow runs simultaneously (GitHub Actions queues jobs)
- If conflict occurs, workflow can retry automatically
- Git history allows recovery

### Risk: Repository Size Growth

**Likelihood**: High (by design)  
**Impact**: Low  
**Mitigation**:
- Text files compress well in Git
- Daily content is small (KB range per day)
- Years of content unlikely to exceed reasonable repo size limits
- If needed in future: Git LFS or separate archive repository
- Current scope: Accumulation is the goal, not a problem

### Risk: Workflow Failure After Generation But Before Commit

**Likelihood**: Low  
**Impact**: Medium  
**Mitigation**:
- Generated files are idempotent - can regenerate safely
- Next workflow run will generate missing content
- No data loss since generation is deterministic (scrapes from USCCB)
- Overwrite behavior allows corrections

## Summary

**All technical questions resolved** - No NEEDS CLARIFICATION items remain.

**Key Decisions**:
1. **Root cause**: GitHub Actions not persisting _site/ directory → Solution: Commit to repository
2. **Discovery**: Existing code already works correctly - no changes needed
3. **Persistence**: Add git commit step to workflow before deployment
4. **Overwrite**: Allow overwrites for same-date regeneration
5. **Testing**: Multi-run E2E tests to verify accumulation behavior

**Technologies Affirmed**:
- Python 3.13 with pathlib for file operations
- Git CLI in GitHub Actions for persistence
- pytest for testing (existing)
- GitHub Pages for deployment (existing)

**Next Phase**: Design data model and contracts
