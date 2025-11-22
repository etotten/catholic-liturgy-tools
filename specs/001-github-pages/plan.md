# Implementation Plan: GitHub Pages Daily Message

**Branch**: `001-github-pages` | **Date**: 2025-11-22 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-github-pages/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a Python CLI tool that generates daily markdown messages (date + "Hello Catholic World"), creates an index page linking all messages, and integrates with GitHub Actions to automatically publish to GitHub Pages using Jekyll. The implementation follows a thin-slice approach with 4 priority levels (P1-P4), starting with standalone local message generation and progressively adding index generation, GitHub Actions automation, and remote triggering capabilities.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: 
- Python stdlib (argparse, datetime, pathlib)
- requests (for GitHub API interaction - P4 only)
- pytest, pytest-cov (testing)
- GitHub Actions (CI/CD automation)
- Jekyll (provided by GitHub Pages, no installation needed)

**Storage**: File system (markdown files in `_posts/` directory for Jekyll compatibility)  
**Testing**: pytest with 90% coverage requirement, including E2E tests for all CLI commands  
**Target Platform**: 
- Local: macOS/Linux/Windows with Python 3.11+
- CI/CD: GitHub Actions Ubuntu runner
- Deployment: GitHub Pages with Jekyll

**Project Type**: Single project (CLI + library)  
**Performance Goals**: 
- Local message generation: < 5 seconds
- GitHub Action complete workflow: < 2 minutes (generation + commit + deploy)
- CLI to live site end-to-end: < 3 minutes

**Constraints**: 
- Must work with GitHub's default Jekyll configuration (no custom plugins)
- Generated markdown must be Jekyll-compatible (YAML frontmatter + content)
- No external databases or services (except GitHub API for P4)
- Must handle multiple runs per day idempotently (no duplicates)

**Scale/Scope**: 
- Small scale: ~365 message files per year
- Single user/developer workflow
- Minimal dependencies to reduce maintenance burden

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**✅ Principle 1: Liturgical Authenticity**
- Status: N/A for this feature (fixed greeting, not liturgical content)
- Note: Future features adding liturgical content must follow sourcing requirements

**✅ Principle 2: Simplicity and Minimalism**
- Simple file-based storage (no database)
- Minimal dependencies (mostly stdlib)
- Thin-slice approach with P1-P4 priorities
- No premature abstractions or frameworks

**✅ Principle 3: Correctness Over Performance**
- Clear, readable code prioritized
- No performance optimizations planned
- Current performance goals are easily achievable without optimization

**✅ Principle 4: Testing Discipline**
- 90% unit test coverage enforced via pytest-cov
- E2E tests for all CLI commands (P1-P4)
- Tests developed alongside features

**✅ Principle 5: CLI-First Development**
- Primary interface is CLI
- All features accessible via CLI commands
- Clear error messages and help text

**✅ Principle 6: Semantic Versioning**
- This is a MINOR version bump (new feature, backward compatible)
- Version will be incremented in pyproject.toml and __init__.py

**✅ Principle 7: Python 3.11 Standard**
- Using Python 3.11 exclusively
- No alternative languages needed

**✅ Principle 8: Scope Constraints for Early Development**
- English-only (messages in English)
- No accessibility features at this stage
- No performance optimizations
- Focused on core functionality

**GATE STATUS: ✅ PASSED** - All constitutional principles satisfied

## Project Structure

### Documentation (this feature)

```text
specs/001-github-pages/
├── spec.md              # Feature specification (already created)
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0 output (technical decisions)
├── data-model.md        # Phase 1 output (entity definitions)
├── quickstart.md        # Phase 1 output (developer guide)
├── contracts/           # Phase 1 output (CLI interface contracts)
│   └── cli-commands.md  # CLI command specifications
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

Using **Option 1: Single project** structure (CLI + library):

```text
src/catholic_liturgy_tools/
├── __init__.py                 # Package initialization, version
├── cli.py                      # Main CLI entry point (existing, to be enhanced)
├── generator/
│   ├── __init__.py
│   ├── message.py              # Daily message generation logic
│   └── index.py                # Index page generation logic
├── github/
│   ├── __init__.py
│   └── actions.py              # GitHub Actions workflow trigger (P4)
└── utils/
    ├── __init__.py
    ├── file_ops.py             # File I/O utilities
    └── date_utils.py           # Date formatting utilities

tests/
├── conftest.py                 # Pytest configuration and fixtures
├── unit/
│   ├── test_message.py         # Unit tests for message generation
│   ├── test_index.py           # Unit tests for index generation
│   ├── test_github_actions.py  # Unit tests for GitHub API (P4)
│   └── test_utils.py           # Unit tests for utilities
├── integration/
│   ├── test_message_workflow.py    # Integration tests
│   └── test_index_workflow.py      # Integration tests
└── e2e/
    ├── test_cli_generate.py        # E2E test for generate-message (P1)
    ├── test_cli_index.py           # E2E test for generate-index (P2)
    └── test_cli_trigger.py         # E2E test for trigger-publish (P4)

.github/
├── workflows/
│   └── publish-daily-message.yml   # GitHub Actions workflow (P3)
└── CODEOWNERS                      # (optional)

_posts/                          # Jekyll posts directory (generated)
├── 2025-11-22-daily-message.md
├── 2025-11-23-daily-message.md
└── ...

index.md                         # Generated index page (Jekyll homepage)

_config.yml                      # Jekyll configuration (P3)

pyproject.toml                   # Updated with new dependencies
```

**Structure Decision**: Selected single project structure because:
- Feature is a CLI tool with library functions (not a web app or mobile app)
- All code is Python, no frontend/backend split needed
- Simple, flat structure aligns with constitutional principle of minimalism
- Existing `src/catholic_liturgy_tools/` structure is reused and extended
- Generator modules (message, index) contain core business logic
- GitHub module isolated for P4 feature (GitHub API interaction)
- Tests organized by type (unit/integration/e2e) for clarity

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations** - All constitutional principles are satisfied. No complexity tracking needed.
