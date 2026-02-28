# Implementation Plan: Daily Reflections with AI-Augmented Content

**Branch**: `005-daily-reflections` | **Date**: November 30, 2025 | **Spec**: [spec.md](./spec.md)  
**Status**: ✅ **PHASE 1 COMPLETE** - Design artifacts ready, ready for Phase 2 (tasks.md)  
**Input**: Feature specification from `/specs/005-daily-reflections/spec.md`

---

## Plan Status Overview

| Phase | Status | Artifacts |
|-------|--------|-----------|
| **Phase 0: Research** | ✅ Complete | [research.md](./research.md) - 7 technical decisions documented |
| **Phase 1: Design** | ✅ Complete | [data-model.md](./data-model.md), [contracts/](./contracts/), [quickstart.md](./quickstart.md) |
| **Phase 2: Tasks** | ⏳ Pending | Run `/speckit.tasks` to generate tasks.md |
| **Constitution Check** | ✅ Pass | All 8 principles compliant (see Post-Design Constitution Check below) |
| **Agent Context** | ✅ Updated | GitHub Copilot context file updated with project technologies |

**Next Step**: Invoke `/speckit.tasks` to generate implementation task breakdown (tasks.md).

---

## Summary

Transform the daily readings feature into an AI-augmented daily reflection experience by adding: (1) one-line AI-generated synopses for each Scripture reading, (2) a unified daily reflection with pondering questions and CCC citations, (3) sourced Catholic prayers at the top of each page, and (4) feast day/saint biographical information. Content will be generated daily at 6:00 AM CT using Anthropic Claude API, with on-demand generation for historical dates. AI API costs must stay below $0.04 per reflection.

## Technical Context

**Language/Version**: Python 3.11+ (per constitution Principle 7)  
**Primary Dependencies**: 
- Anthropic SDK (Claude API) for AI text generation
- python-dotenv for environment variable management (.env file)
- BeautifulSoup4 (existing) for HTML parsing
- requests (existing) for HTTP requests
- pytest/pytest-cov (existing) for testing

**Storage**: File-based HTML generation (existing pattern in `_site/readings/`), no database required  
**Testing**: pytest with 90%+ coverage requirement (per constitution Principle 4)  
**Target Platform**: GitHub Pages static site + GitHub Actions for scheduled generation  
**Project Type**: Single CLI-based project (extends existing `catholic-liturgy` CLI)  
**Performance Goals**: AI generation must complete in <60 seconds per date, cost <$0.04 per reflection  
**Constraints**: 
- Must preserve existing readings functionality (FR-014)
- Scheduled generation at 6:00 AM CT daily (FR-016)
- Graceful degradation when AI service unavailable (FR-011)
- Theological accuracy through prompt engineering (FR-013)

**Scale/Scope**: Daily generation (1 reflection/day), historical on-demand generation, ~365 pages/year

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle 1: Liturgical Authenticity ✅ COMPLIANT
- **Status**: PASS
- **Verification**: 
  - AI-generated synopses and reflections will reference existing Scripture from USCCB (authoritative source)
  - Prayers sourced from authorized Catholic websites (USCCB, Vatican, Catholic Online, EWTN, Loyola Press)
  - CCC citations validated against Vatican's official online CCC (2865 paragraphs)
  - Feast day/saint information from reputable Catholic sources
  - All AI-generated content will emphasize orthodox Catholic teaching per FR-013

### Principle 2: Simplicity and Minimalism ✅ COMPLIANT
- **Status**: PASS
- **Verification**:
  - Building incrementally on existing readings infrastructure
  - Priority-based user stories (P1: synopses, P2: reflection/prayer, P3: feast days)
  - Reusing existing patterns (HTML generation, CLI commands, file structure)
  - No premature abstraction - direct integration with Anthropic SDK

### Principle 3: Correctness Over Performance ✅ COMPLIANT
- **Status**: PASS
- **Verification**:
  - Correctness prioritized: theological accuracy (FR-013), CCC validation (FR-012)
  - Performance goal (60s generation) is adequate, not optimized
  - Graceful error handling ensures correct display even on failures

### Principle 4: Testing Discipline ⚠️ NEEDS ATTENTION
- **Status**: MUST VERIFY DURING DEVELOPMENT
- **Requirements**:
  - 90%+ unit test coverage required
  - E2E tests for all new CLI options/behaviors
  - Test AI integration with mocked responses
  - Test cost tracking and limits
- **Risk**: AI API calls difficult to test without mocking strategy

### Principle 5: CLI-First Development ✅ COMPLIANT
- **Status**: PASS
- **Verification**:
  - Extends existing `generate-readings` command
  - May add optional flags for manual reflection generation
  - Error messages for AI failures, cost overruns
  - CLI enables manual verification during development

### Principle 6: Semantic Versioning ✅ COMPLIANT
- **Status**: PASS
- **Next Version**: 0.3.0 (MINOR - new feature, backward compatible)
- **Rationale**: Adds reflection features without breaking existing readings functionality

### Principle 7: Python 3.11 Standard ✅ COMPLIANT
- **Status**: PASS
- **Verification**: All code will be Python 3.11+, leveraging existing project patterns

### Principle 8: Scope Constraints for Early Development ✅ COMPLIANT
- **Status**: PASS
- **Verification**:
  - English-only content (AI prompts in English)
  - No accessibility features beyond basic HTML
  - No performance optimization unless demonstrated need
  - Focus on core reflection functionality first

## Project Structure

### Documentation (this feature)

```text
specs/005-daily-reflections/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (in progress)
├── research.md          # Phase 0: Research unknowns (to be generated)
├── data-model.md        # Phase 1: Data model (to be generated)
├── quickstart.md        # Phase 1: Quick start guide (to be generated)
├── contracts/           # Phase 1: API/CLI contracts (to be generated)
│   ├── cli-commands.md  # CLI command extensions
│   └── ai-prompts.md    # AI prompt templates
├── checklists/
│   └── requirements.md  # Quality checklist (completed)
└── tasks.md             # Phase 2: Implementation tasks (NOT created by /speckit.plan)
```

### Source Code (repository root)

**Structure Decision**: Single Python project (Option 1) - extends existing `catholic-liturgy-tools` CLI structure

```text
src/catholic_liturgy_tools/
├── __init__.py
├── __main__.py
├── cli.py                      # MODIFIED: Extend generate-readings command
├── constants.py
│
├── scraper/                    # EXISTING: USCCB readings scraper
│   ├── __init__.py
│   ├── usccb.py               # Existing USCCB scraper
│   ├── models.py              # Existing reading models (DailyReading, ReadingEntry)
│   └── exceptions.py
│
├── generator/                  # EXISTING + NEW: HTML generation
│   ├── __init__.py
│   ├── index.py               # MODIFIED: Update for reflections
│   ├── readings.py            # MODIFIED: Integrate reflection content
│   └── message.py             # EXISTING: Message generation
│
├── ai/                         # NEW: AI integration module
│   ├── __init__.py
│   ├── client.py              # Anthropic API client wrapper
│   ├── prompts.py             # Prompt templates for synopses, reflections
│   ├── models.py              # AI response models (Synopsis, Reflection, etc.)
│   └── cost_tracker.py        # Track API costs per reflection
│
├── liturgy/                    # NEW: Liturgical calendar and prayer sourcing
│   ├── __init__.py
│   ├── calendar.py            # Feast day detection and information
│   ├── prayers.py             # Prayer sourcing from Catholic websites
│   └── ccc_validator.py       # CCC paragraph validation (1-2865)
│
├── utils/                      # EXISTING + NEW
│   ├── __init__.py
│   ├── date_utils.py          # EXISTING
│   ├── file_ops.py            # EXISTING
│   ├── html_utils.py          # EXISTING
│   └── retry.py               # EXISTING
│
└── github/                     # EXISTING
    ├── __init__.py
    └── actions.py             # MODIFIED: Update for 6am CT scheduled generation

tests/
├── conftest.py                 # EXISTING + MODIFIED: Add AI mocking fixtures
├── unit/                       # Unit tests (90%+ coverage)
│   ├── test_cli.py            # MODIFIED: Test reflection command options
│   ├── test_ai_client.py      # NEW: Test AI client (mocked)
│   ├── test_prompts.py        # NEW: Test prompt generation
│   ├── test_cost_tracker.py   # NEW: Test cost tracking
│   ├── test_calendar.py       # NEW: Test liturgical calendar
│   ├── test_prayers.py        # NEW: Test prayer sourcing (mocked HTTP)
│   ├── test_ccc_validator.py  # NEW: Test CCC validation
│   └── [existing tests]
│
├── integration/                # Integration tests
│   ├── test_reflection_workflow.py  # NEW: End-to-end reflection generation
│   ├── test_ai_integration.py       # NEW: Real API calls (optional, gated)
│   └── [existing tests]
│
└── e2e/                        # End-to-end CLI tests
    ├── test_cli_readings.py   # MODIFIED: Test reflection generation via CLI
    └── [existing tests]

.github/workflows/
├── publish-site.yml            # MODIFIED: Update schedule to 6am CT
└── [other workflows]

_site/                          # Generated site content
├── index.html                  # MODIFIED: Update for reflections
└── readings/                   # MODIFIED: Enhanced with reflection content
    └── YYYY-MM-DD.html        # Now includes: prayer, synopses, reflection, feast info
```

**Key Additions**:
- **New `ai/` module**: Encapsulates all AI integration (client, prompts, cost tracking)
- **New `liturgy/` module**: Handles liturgical calendar, prayers, CCC validation
- **Modified `generator/`**: Extends HTML generation to include AI-augmented content
- **Modified GitHub Actions**: Updates schedule to 6:00 AM CT daily generation

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**Status**: ✅ No constitutional violations requiring justification

All design decisions align with constitutional principles:
- Simple, incremental approach building on existing infrastructure
- No premature abstraction or over-engineering
- Clear module boundaries (ai/, liturgy/) for maintainability
- Focus on core functionality first (P1 → P2 → P3)

---

## Post-Design Constitution Check

**Phase**: Phase 1 Design Complete (data-model.md, contracts/, quickstart.md)  
**Date**: November 30, 2025

### Re-evaluation of Constitutional Principles

#### ✅ Principle 1: Liturgical Authenticity
- **Status**: COMPLIANT
- **Evidence**:
  - Data model enforces source attribution (SourcedPrayer.source_name, source_url)
  - Prayer database schema requires approved sources only (USCCB, Vatican, Catholic Online, EWTN, Loyola Press per FR-007)
  - CCC validation ensures paragraph numbers in valid range (1-2865 per CCCCitation.paragraph_number)
  - Feast day information derived from authoritative liturgical calendar (romcal NPM package)
  - AI prompts include explicit theological constraints ("Stay within bounds of Catholic teaching")
- **Post-Design Notes**: Design strengthens liturgical authenticity through explicit validation and source tracking

#### ✅ Principle 2: Simplicity and Minimalism
- **Status**: COMPLIANT
- **Evidence**:
  - Data model uses simple Python dataclasses (no complex ORM)
  - File-based storage (JSON for prayers, HTML for output) avoids database complexity
  - Module structure is flat and focused: ai/ (4 files), liturgy/ (3 files)
  - Contracts specify minimal CLI extensions (5 new options to existing command)
  - Prayer selection algorithm is straightforward context-matching (no machine learning)
- **Post-Design Notes**: Design maintains simplicity through incremental extension of existing patterns

#### ✅ Principle 3: Correctness Over Performance
- **Status**: COMPLIANT
- **Evidence**:
  - CCC validation uses simple range check (1-2865) with optional HTTP verification
  - Cost tracking uses explicit token counting, not estimation heuristics
  - Graceful degradation on errors (ai_service_status enum: "success", "partial", "failed")
  - Retry logic clearly defined (max 3 retries with exponential backoff)
  - Data model includes comprehensive validation rules for each entity
- **Post-Design Notes**: Design prioritizes correctness with clear error handling and validation

#### ✅ Principle 4: Testing Discipline
- **Status**: COMPLIANT (will be verified during implementation)
- **Evidence**:
  - Contract includes comprehensive testing checklist (13 test scenarios for CLI)
  - Prayer database schema includes validation test cases (7 tests)
  - AI prompts contract includes validation checklist (10 items)
  - Data model documents validation rules for all entities
  - Example tests shown in contracts (e.g., test_prayer_selection_advent)
- **Post-Design Notes**: Design provides clear testable contracts and validation rules to support 90%+ coverage requirement

#### ✅ Principle 5: CLI-First Development
- **Status**: COMPLIANT
- **Evidence**:
  - CLI contract extends existing generate-readings command (backward compatible)
  - Comprehensive usage examples (5 examples covering all options)
  - Error handling documented with clear messages and exit codes
  - Quickstart guide provides CLI-focused workflow
  - All features accessible via CLI options (--with-reflections, --max-cost, etc.)
- **Post-Design Notes**: Design maintains CLI as primary interface with helpful error messages

#### ✅ Principle 6: Semantic Versioning
- **Status**: COMPLIANT
- **Evidence**:
  - Prayer database schema includes version field (semantic versioning: "1.0.0")
  - Changes are backward compatible (existing readings-only workflow preserved with --no-reflections)
  - New features are additive (extends DailyReading with optional fields)
  - Graceful degradation ensures old behavior continues to work
- **Post-Design Notes**: Design ensures backward compatibility for smooth version increments

#### ✅ Principle 7: Python 3.11 Standard
- **Status**: COMPLIANT with justified exception
- **Evidence**:
  - All modules use Python 3.11+ (dataclasses, type hints, pathlib)
  - Exception: romcal NPM package (Node.js) for liturgical calendar
  - Justification: Python wrapper (subprocess) isolates Node.js dependency
  - Anthropic SDK is Python-native (anthropic>=0.8.0)
- **Post-Design Notes**: Python remains primary language with justified, documented exception for liturgical calendar

#### ✅ Principle 8: Scope Constraints for Early Development
- **Status**: COMPLIANT
- **Evidence**:
  - English-only: All prompts and content in English (language field in prayer database: "en")
  - No accessibility features: HTML output is plain semantic HTML
  - No premature optimization: Cost tracking is simple token counting
  - Focus on core functionality: P1 features prioritized (synopses, reflection, prayer)
- **Post-Design Notes**: Design respects early-stage scope constraints

### Final Assessment

**Overall Compliance**: ✅ PASS  
**Constitutional Violations**: None  
**Justifications Required**: None

**Summary**:
All 8 constitutional principles are satisfied post-design. The data model, contracts, and quickstart guide maintain the project's commitment to liturgical authenticity, simplicity, correctness, testing discipline, CLI-first development, semantic versioning, Python standardization, and appropriate scope constraints. The design is ready for implementation.

**Next Phase**: Ready to proceed to Phase 2 (tasks.md generation via /speckit.tasks command)
