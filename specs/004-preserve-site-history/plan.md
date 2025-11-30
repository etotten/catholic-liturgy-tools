# Implementation Plan: Preserve Site Historical Content

**Branch**: `004-preserve-site-history` | **Date**: 2025-11-30 | **Spec**: [spec.md](spec.md)  
**Input**: Feature specification from `/specs/004-preserve-site-history/spec.md`

## Summary

**Primary Requirement**: Fix the site content preservation issue where the index page only shows the latest reading and message, causing loss of historical content. The site must accumulate all generated content over time, with each generation adding to (not replacing) existing content.

**Technical Approach**: The root cause is that the `_site/` directory is not committed to the Git repository between GitHub Actions workflow runs. Each run starts with a clean environment, losing previous content. The solution is to add a Git commit step to the workflow after content generation, persisting `_site/` to the repository. The existing index generator code already scans all files correctly - it just needs files to be present. This is a minimal, focused fix requiring only workflow changes and test additions.

## Technical Context

**Language/Version**: Python 3.13  
**Primary Dependencies**: pathlib (stdlib), pytest, pytest-cov  
**Storage**: File-based storage in `_site/` directory, committed to Git repository  
**Testing**: pytest with 90% coverage requirement, E2E tests for CLI commands  
**Target Platform**: GitHub Actions (Ubuntu latest) + GitHub Pages deployment  
**Project Type**: Single project (CLI tool with content generation)  
**Performance Goals**: Handle hundreds of content files without degradation  
**Constraints**: Must not delete existing content, must maintain reverse chronological order in index  
**Scale/Scope**: Daily content accumulation, targeting years of historical content (hundreds to thousands of files)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Principle 1: Liturgical Authenticity
**Status**: Not Applicable  
**Rationale**: This feature deals with content preservation and site structure, not liturgical content itself. Content authenticity is maintained by existing scraping and generation features.

### ✅ Principle 2: Simplicity and Minimalism
**Status**: PASS  
**Rationale**: The solution is minimal - adding one Git commit step to the workflow. No new complexity in content generation code. The existing index generator already works correctly. Straightforward solution without abstractions.

### ✅ Principle 3: Correctness Over Performance
**Status**: PASS  
**Rationale**: Solution prioritizes correctness (preserve all content) over optimization. File accumulation is acceptable, no premature optimization. Clear, verifiable behavior.

### ✅ Principle 4: Testing Discipline
**Status**: PASS - Will comply  
**Rationale**: Plan includes comprehensive E2E tests for multi-run accumulation and same-date overwrite scenarios. Tests verify the core requirement: content persists across runs. Existing unit tests for index generation remain valid. Coverage target of 90% will be maintained.

### ✅ Principle 5: CLI-First Development
**Status**: PASS  
**Rationale**: No CLI changes required - existing commands already work correctly. The problem is in workflow persistence, not CLI behavior. E2E tests will continue to cover all CLI options.

### ✅ Principle 6: Semantic Versioning
**Status**: PASS  
**Rationale**: This is a bug fix (content loss). Will be released as a PATCH version (0.x.y → 0.x.y+1). No breaking changes, no new features. Backward compatible.

### ✅ Principle 7: Python 3.13 Standard
**Status**: PASS  
**Rationale**: All changes are in Python 3.13 or YAML (GitHub Actions). No alternative languages introduced.

### ✅ Principle 8: Scope Constraints for Early Development  
**Status**: PASS  
**Rationale**: Remains English-only, no accessibility features, no performance optimizations. Focused on core functionality fix.

**Overall Constitution Status**: ✅ **ALL CHECKS PASS** - No violations, ready to proceed

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
.github/
└── workflows/
    └── publish-content.yml       # MODIFY: Add commit step (primary change)

src/
└── catholic_liturgy_tools/
    ├── cli.py                     # NO CHANGE: CLI interface unchanged
    ├── generator/
    │   ├── message.py            # NO CHANGE: Already creates files correctly
    │   ├── readings.py           # NO CHANGE: Already creates files correctly
    │   └── index.py              # VERIFY ONLY: Already scans all files
    └── utils/
        └── file_ops.py           # NO CHANGE: File operations work correctly

tests/
├── e2e/
│   ├── test_cli_generate.py     # NO CHANGE: Existing tests remain valid
│   ├── test_cli_readings.py     # NO CHANGE: Existing tests remain valid
│   └── test_cli_index.py        # ADD: Multi-run accumulation tests
├── integration/
│   └── test_index_workflow.py   # VERIFY: May need updates for multi-run tests
└── unit/
    ├── test_index.py             # NO CHANGE: Unit tests remain valid
    └── ...                       # NO CHANGE: Other unit tests unaffected

_site/                             # COMMITTED: Now tracked in Git (was ignored/ephemeral)
├── index.html
├── messages/
│   └── YYYY-MM-DD-daily-message.md
└── readings/
    └── YYYY-MM-DD.html
```

**Structure Decision**: Single project (Option 1). This is a CLI tool with content generation. All code resides in `src/catholic_liturgy_tools/`. The primary change is to the GitHub Actions workflow file. Python code changes are minimal (verification only). Test additions are in existing test directories.

**Key Insight**: The existing codebase is already structured correctly for content accumulation. The bug is NOT in the Python code - the index generator already discovers all files. The bug is that `_site/` wasn't being persisted between workflow runs. This means implementation is mostly workflow changes, not code changes.

## Complexity Tracking

> **No violations to justify** - All constitution checks pass. No additional complexity introduced.

---

## Phase Summary

### Phase 0: Research (Completed)
- ✅ **research.md** created
- Root cause identified: `_site/` not persisted between workflow runs
- Solution validated: Git commit step in workflow
- No NEEDS CLARIFICATION items - all technical questions resolved

### Phase 1: Design (Completed)
- ✅ **data-model.md** created - Entities and relationships defined
- ✅ **contracts/cli-commands.md** created - CLI behavior requirements documented
- ✅ **contracts/github-actions.md** created - Workflow changes specified
- ✅ **quickstart.md** created - Implementation guide for developers
- ✅ **Agent context updated** - Copilot context file updated with feature info
- ✅ **Constitution check re-run** - All principles validated post-design

### Phase 2: Tasks (Not Started - Use `/speckit.tasks`)
- Generate detailed task breakdown for implementation
- Create task ordering and dependencies
- Estimate effort for each task

---

## Next Steps

**This plan is now complete**. To proceed with implementation:

```bash
# Generate task breakdown
/speckit.tasks

# Review and adjust tasks.md as needed

# Begin implementation following tasks.md
```

**Key Deliverables from This Plan**:
1. ✅ Technical root cause identified
2. ✅ Solution architecture defined (minimal workflow change)
3. ✅ Data model documented (entities, relationships, invariants)
4. ✅ API contracts defined (CLI behavior, workflow changes)
5. ✅ Quickstart guide for implementers
6. ✅ Constitution compliance verified
7. ✅ No blockers or unclear requirements remain

**Implementation Readiness**: ✅ **READY** - All planning phases complete, proceed to tasks generation
