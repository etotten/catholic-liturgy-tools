# Implementation Plan: Site Content Restructuring

**Branch**: `003-site-content-restructure` | **Date**: 2025-11-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-site-content-restructure/spec.md`

**Note**: This plan follows the speckit methodology for systematic implementation.

## Summary

Restructure the site to separate generated content from source code by moving all publishable files into a `_site/` directory with feature-specific subdirectories (`messages/`, `readings/`). Convert the index page from Markdown to HTML with basic inline CSS and "Catholic Liturgy Tools" as the main heading. Configure GitHub Pages to publish from a dedicated `gh-pages` branch containing only `_site/` contents. Update all generators and CLI commands to output to the new structure. Perform one-time migration of existing content files and delete old locations.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: Standard library (pathlib, re), existing utilities (file_ops, date_utils), BeautifulSoup4 for HTML parsing  
**Storage**: File system - static files in `_site/` directory structure  
**Testing**: pytest with 90%+ coverage requirement  
**Target Platform**: GitHub Actions (Ubuntu), GitHub Pages static hosting  
**Project Type**: Single project - Python CLI tool generating static site content  
**Performance Goals**: Generation time <5 seconds for full site rebuild, suitable for daily automated runs  
**Constraints**: Must maintain backward compatibility with existing CLI interface, no breaking changes to generation logic  
**Scale/Scope**: Small static site (~365 files/year for daily content), single-user personal project

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle 1: Liturgical Authenticity
✅ **PASS** - No liturgical content changes; only restructuring site organization

### Principle 2: Simplicity and Minimalism  
✅ **PASS** - Solution is straightforward: update output paths, convert index to HTML, add gh-pages deployment. No unnecessary abstraction.

### Principle 3: Correctness Over Performance
✅ **PASS** - Focus is on correct file placement and link resolution. Performance is not a concern for static file generation.

### Principle 4: Testing Discipline
⚠️ **REQUIRES ATTENTION** - Must maintain 90%+ coverage. Existing tests will need updates for new paths. New tests for HTML generation and gh-pages deployment required.

### Principle 5: CLI-First Development
✅ **PASS** - No CLI changes required (output_dir parameter already exists). Existing E2E tests need path updates.

### Principle 6: Semantic Versioning
✅ **PASS** - This will be a MINOR version bump (0.3.0) - new functionality (HTML index, gh-pages deployment) added in backward-compatible manner

### Principle 7: Python 3.11 Standard
✅ **PASS** - Implementation remains Python 3.11, no additional languages needed

### Principle 8: Scope Constraints
✅ **PASS** - Stays within scope: English-only, no accessibility features, no performance optimization

---

## Plan Completion Report

### Phase 0: Research - ✅ COMPLETE

**Objective**: Resolve all technical unknowns and validate approach decisions

**Deliverable**: `research.md` (6 research areas, all questions resolved)

**Key Findings**:
1. **GitHub Pages Deployment**: gh-pages branch strategy using peaceiris/actions-gh-pages action
2. **HTML Index Generation**: Inline CSS approach with f-string templates
3. **Path Resolution**: Relative paths for links (`messages/`, `readings/`)
4. **Migration Strategy**: One-time developer task, not part of CLI
5. **Workflow Updates**: Simplified deployment removing commit-to-main pattern
6. **Implementation Patterns**: Standard Python file I/O with pathlib, HTML escaping best practices

**Decision Summary**:
- ✅ All NEEDS CLARIFICATION items from Technical Context resolved
- ✅ Best practices identified for each technology choice
- ✅ Integration patterns documented with code examples
- ✅ No blocking technical issues discovered

---

### Phase 1: Design & Contracts - ✅ COMPLETE

**Objective**: Define data models, API contracts, and implementation specifications

**Deliverables**:
1. ✅ `data-model.md` - 4 core entities, transformations, validation rules
2. ✅ `contracts/cli-commands.md` - CLI interface with backward compatibility
3. ✅ `contracts/html-format.md` - Complete HTML/CSS specification
4. ✅ `contracts/github-actions.md` - Workflow deployment specification
5. ✅ `quickstart.md` - Developer setup and testing guide

**Design Decisions**:

**Data Model**:
- Site Content Directory (`_site/`) as root container
- Subdirectories for feature-specific content (`messages/`, `readings/`)
- Index Page entity with HTML structure and inline CSS
- Path transformations from current to target state clearly defined

**CLI Interface**:
- Backward compatible parameter handling (output_dir, output_file)
- New defaults: `_site/messages/`, `_site/readings/`, `_site/index.html`
- No breaking changes to existing CLI commands
- Version compatibility matrix documented

**HTML Format**:
- Valid HTML5 with DOCTYPE declaration
- Meta tags: charset UTF-8, viewport responsive
- Title: "Catholic Liturgy Tools"
- Inline CSS with 7 rule blocks (body, h1, h2, ul, li, a, a:hover)
- Two main sections: Daily Messages, Daily Readings
- Relative link paths for messages and readings
- Reverse chronological sorting
- W3C validation requirements
- Edge case handling (empty lists, special characters with HTML escaping)
- Python implementation using f-string templates

**GitHub Actions Deployment**:
- Single job workflow (generate-and-deploy)
- Simplified permissions (contents: write only)
- peaceiris/actions-gh-pages@v3 for deployment
- Orphan branch strategy (force_orphan: true)
- No commits to main branch from Actions
- gh-pages branch contains flattened _site/ contents
- Error handling and rollback procedures documented

**Constitution Re-Check (Post-Design)**:
- ✅ All 8 principles still satisfied
- ✅ Design maintains 90%+ coverage path (tests identified)
- ✅ Backward compatibility preserved
- ✅ No scope creep introduced

---

### Phase 2: Task Breakdown - ⏳ PENDING

**Objective**: Break implementation into discrete, trackable tasks

**Process**: Invoke `/speckit.tasks` command (separate from /speckit.plan)

**Expected Output**: `tasks.md` with:
- Prioritized task list
- Time estimates
- Dependencies between tasks
- Success criteria per task
- Testing requirements

**Note**: This phase is intentionally separate to allow review of design artifacts before committing to implementation schedule.

---

## Implementation Readiness

### ✅ Prerequisites Met

1. **Specification Complete**: All requirements defined, clarifications integrated
2. **Research Complete**: All technical unknowns resolved
3. **Design Complete**: Data model and contracts documented
4. **Constitution Validated**: All principles satisfied, no violations
5. **Tools Ready**: Python 3.11, pytest, Git, GitHub Actions available

### 📋 Contract Specifications Ready

**CLI Interface** (`contracts/cli-commands.md`):
- ✅ 3 commands specified: generate-message, generate-readings, generate-index
- ✅ Parameter changes documented with defaults
- ✅ Backward compatibility matrix provided
- ✅ Testing contracts defined

**HTML Format** (`contracts/html-format.md`):
- ✅ Complete HTML5 template with required elements
- ✅ Inline CSS with 7 rule blocks specified
- ✅ Link path patterns documented (relative paths)
- ✅ Sorting requirements defined (reverse chronological)
- ✅ Validation rules stated (W3C HTML5)
- ✅ Edge cases handled (empty lists, special characters)
- ✅ Python implementation example provided

**GitHub Actions** (`contracts/github-actions.md`):
- ✅ Complete workflow YAML specification
- ✅ peaceiris/actions-gh-pages action configured
- ✅ Branch strategy documented (main vs gh-pages)
- ✅ Deployment flow diagram included
- ✅ Error handling and rollback procedures defined
- ✅ First-time setup steps provided

### 📚 Documentation Ready

**Quickstart Guide** (`quickstart.md`):
- ✅ Setup instructions for developers
- ✅ Testing workflow documented
- ✅ Key file locations identified
- ✅ Testing checklist provided
- ✅ Common development tasks explained
- ✅ Debugging tips included
- ✅ One-time migration steps outlined
- ✅ GitHub Pages setup guide provided

### 🎯 Implementation Path Clear

**Source Files to Modify**:
1. `src/catholic_liturgy_tools/cli.py` - Update default paths
2. `src/catholic_liturgy_tools/generator/message.py` - Change output_dir default
3. `src/catholic_liturgy_tools/generator/readings.py` - Change output_dir default
4. `src/catholic_liturgy_tools/generator/index.py` - Rewrite for HTML generation
5. `.github/workflows/publish-content.yml` - Update deployment strategy

**Test Files to Update**:
1. `tests/unit/test_cli.py` - Update default path assertions
2. `tests/unit/test_message.py` - Update output_dir tests
3. `tests/unit/test_readings_generator.py` - Update output_dir tests
4. `tests/unit/test_index.py` - Rewrite for HTML generation testing
5. `tests/integration/test_message_workflow.py` - Update path expectations
6. `tests/integration/test_index_workflow.py` - Major updates for HTML
7. `tests/e2e/test_cli_generate.py` - Update path assertions
8. `tests/e2e/test_cli_index.py` - Update for HTML output

**New Files to Create**: None (all changes are modifications)

---

## Next Steps

### Immediate Action Required

**Command**: `/speckit.tasks`

**Purpose**: Break implementation into discrete, trackable tasks

**Expected Result**: `tasks.md` file containing:
- Prioritized task list with time estimates
- Dependencies mapped between tasks
- Success criteria per task
- Testing requirements per task
- Implementation sequence

### After Task Breakdown

1. ✅ Review task list for completeness
2. ✅ Confirm time estimates are realistic
3. ✅ Validate task dependencies
4. ✅ Begin implementation following task order
5. ✅ Track progress against task list
6. ✅ Update tests as code is modified
7. ✅ Verify 90%+ coverage maintained throughout
8. ✅ Test locally before pushing
9. ✅ Deploy to feature branch for testing
10. ✅ Create pull request after validation

---

## Summary

**Planning Status**: ✅ COMPLETE (Phases 0 and 1)

**Branch**: `003-site-content-restructure`

**Key Artifacts**:
- `spec.md` - Feature specification with clarifications
- `research.md` - Technical research findings
- `data-model.md` - Data entity definitions
- `contracts/cli-commands.md` - CLI interface specification
- `contracts/html-format.md` - HTML generation specification
- `contracts/github-actions.md` - Deployment workflow specification
- `quickstart.md` - Developer guide

**Implementation Ready**: YES

**Next Command**: `/speckit.tasks` to generate task breakdown

**Estimated Complexity**: Medium (significant changes to index generator and workflow, moderate test updates)

**Risk Level**: Low (well-defined contracts, backward compatible, existing patterns reusable)

---

*Plan generated following speckit methodology | Phase 2 (Task Breakdown) pending*

**OVERALL GATE STATUS**: ✅ **PASS** - All constitutional requirements met. Testing discipline requires attention but is achievable.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
# Existing source structure (no changes to src/)
src/catholic_liturgy_tools/
├── __init__.py
├── __main__.py
├── cli.py                    # Updated: paths for new _site structure
├── constants.py
├── generator/
│   ├── __init__.py
│   ├── message.py           # Updated: output to _site/messages/
│   ├── readings.py          # Updated: output to _site/readings/
│   └── index.py             # Updated: output _site/index.html with HTML format
├── scraper/
│   └── [unchanged]
├── utils/
│   └── [unchanged]
└── github/
    └── [unchanged]

# New site content structure (generated files)
_site/                        # NEW: All generated content goes here
├── index.html               # NEW: HTML format (was index.md at root)
├── messages/                # NEW: subdirectory for messages
│   └── YYYY-MM-DD-daily-message.md
└── readings/                # NEW: subdirectory for readings
    └── YYYY-MM-DD.html

# Testing structure (updates required)
tests/
├── conftest.py
├── unit/
│   ├── test_message.py      # Updated: new paths
│   ├── test_index.py        # Updated: HTML generation, new paths
│   └── test_readings_generator.py  # Updated: new paths
├── integration/
│   ├── test_message_workflow.py    # Updated: new paths
│   └── test_index_workflow.py      # Updated: HTML format
└── e2e/
    ├── test_cli_generate.py         # Updated: verify _site paths
    ├── test_cli_index.py            # Updated: verify HTML output
    └── test_cli_readings.py         # Updated: verify _site paths

# GitHub Actions (significant updates)
.github/workflows/
└── publish-content.yml      # Updated: deploy to gh-pages branch

# Legacy files (will be deleted during migration)
_posts/                      # DELETE: migrate to _site/messages/
readings/                    # DELETE: migrate to _site/readings/
index.md                     # DELETE: replaced by _site/index.html
```

**Structure Decision**: Using existing single-project Python structure. Primary change is addition of `_site/` directory for all generated content, replacing the previous root-level approach. This provides clear separation between source code (`src/`) and published content (`_site/`). The `gh-pages` branch will contain only `_site/` contents.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations** - All constitutional principles satisfied. This implementation follows the simplicity principle by making minimal changes to achieve the restructuring goals.
