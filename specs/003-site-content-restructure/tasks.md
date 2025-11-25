# Tasks: Site Content Restructuring

**Feature**: 003-site-content-restructure  
**Branch**: `003-site-content-restructure`  
**Date**: 2025-11-25

**Input**: Design documents from `/specs/003-site-content-restructure/`
- plan.md (tech stack, structure, approach)
- spec.md (user stories with priorities P1-P4)
- data-model.md (entities: Site Content Directory, Messages/Readings subdirectories, Index Page)
- contracts/cli-commands.md (CLI interface with backward compatibility)
- contracts/html-format.md (HTML5 structure with inline CSS)
- contracts/github-actions.md (deployment workflow specification)

**Tests**: All test tasks are included per constitutional requirement (90%+ coverage).

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

---

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Maps to user story (US1, US2, US3, US4)
- File paths are exact and absolute where applicable

---

## Phase 1: Setup

**Purpose**: Project initialization and environment preparation

- [X] T001 Create feature branch `003-site-content-restructure` from main
- [X] T002 [P] Update pyproject.toml version from 0.2.0 to 0.3.0
- [X] T003 [P] Add `_site/` to .gitignore to exclude locally generated content

**Checkpoint**: Branch and version ready for development

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Create `_site/` directory structure helper in src/catholic_liturgy_tools/utils/file_ops.py (ensure_directory function enhancement)
- [X] T005 [P] Add constants for new paths in src/catholic_liturgy_tools/constants.py (SITE_DIR, MESSAGES_DIR, READINGS_DIR, INDEX_FILE)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Reorganize Generated Content into _site Directory (Priority: P1) 🎯 MVP

**Goal**: Move all generated content into `_site/` directory with feature-specific subdirectories

**Independent Test**: Run generation commands, verify files in `_site/messages/`, `_site/readings/`, `_site/index.html`

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T006 [P] [US1] Update unit test for message generator in tests/unit/test_message.py (verify default output_dir changed to `_site/messages`)
- [X] T007 [P] [US1] Update unit test for readings generator in tests/unit/test_readings_generator.py (verify default output_dir changed to `_site/readings`)
- [X] T008 [P] [US1] Update unit test for CLI commands in tests/unit/test_cli.py (verify new default paths)
- [X] T009 [P] [US1] Update integration test in tests/integration/test_message_workflow.py (verify end-to-end message generation to new path)
- [X] T010 [P] [US1] Update E2E test in tests/e2e/test_cli_generate.py (verify CLI outputs to `_site/` structure)

### Implementation for User Story 1

- [X] T011 [P] [US1] Update default output_dir in src/catholic_liturgy_tools/generator/message.py (change `_posts` to `_site/messages`)
- [X] T012 [P] [US1] Update default output_dir in src/catholic_liturgy_tools/generator/readings.py (change `readings` to `_site/readings`)
- [X] T013 [US1] Update CLI command defaults in src/catholic_liturgy_tools/cli.py for generate-message command
- [X] T014 [US1] Update CLI command defaults in src/catholic_liturgy_tools/cli.py for generate-readings command
- [X] T015 [US1] Ensure directory creation logic handles `_site/messages/` and `_site/readings/` automatically

**Checkpoint**: User Story 1 complete - content generates to `_site/` structure, all US1 tests pass

---

## Phase 4: User Story 2 - Convert Index Page from Markdown to HTML (Priority: P2)

**Goal**: Generate index as HTML with "Catholic Liturgy Tools" heading, inline CSS, and proper structure

**Independent Test**: Generate index, verify HTML file with correct structure, CSS, and links working in browser

### Tests for User Story 2

- [X] T016 [P] [US2] Rewrite unit tests in tests/unit/test_index.py for HTML generation (verify HTML structure, CSS presence, title)
- [X] T017 [P] [US2] Update integration test in tests/integration/test_index_workflow.py (verify HTML output, not Markdown)
- [X] T018 [P] [US2] Update E2E test in tests/e2e/test_cli_index.py (verify `_site/index.html` created, not `index.md`)
- [X] T019 [US2] Add HTML validation test in tests/unit/test_index.py (verify well-formed HTML5, proper DOCTYPE)

### Implementation for User Story 2

- [X] T020 [US2] Rewrite index generator in src/catholic_liturgy_tools/generator/index.py to generate HTML instead of Markdown
- [X] T021 [US2] Implement HTML template with inline CSS per contracts/html-format.md specification
- [X] T022 [US2] Add DOCTYPE, meta tags (charset UTF-8, viewport), and title "Catholic Liturgy Tools"
- [X] T023 [US2] Implement two sections: "Daily Messages" and "Daily Readings" with proper h2 headings
- [X] T024 [US2] Update default output path in index generator to `_site/index.html`
- [X] T025 [US2] Update CLI command default in src/catholic_liturgy_tools/cli.py for generate-index command
- [X] T026 [US2] Ensure HTML escaping for special characters in link text per contracts/html-format.md

**Checkpoint**: User Story 2 complete - index generates as HTML with CSS, all US2 tests pass

---

## Phase 5: User Story 3 - Configure Root URL to Serve Index Page (Priority: P3)

**Goal**: Deploy to gh-pages branch so root URL serves index page automatically

**Independent Test**: Deploy, visit root URL, verify index loads without `/index.html` in URL

### Tests for User Story 3

- [X] T027 [US3] Add workflow validation test (verify workflow YAML syntax is valid)
- [X] T028 [US3] Manual test: Deploy to feature branch, verify gh-pages branch created with correct structure

### Implementation for User Story 3

- [X] T029 [US3] Update .github/workflows/publish-content.yml per contracts/github-actions.md (remove git commit steps)
- [X] T030 [US3] Add peaceiris/actions-gh-pages@v3 deployment step to workflow
- [X] T031 [US3] Configure publish_dir to `./_site` in workflow
- [X] T032 [US3] Set force_orphan to true in workflow for clean gh-pages history
- [X] T033 [US3] Update workflow permissions to only `contents: write`
- [X] T034 [US3] Remove old Pages artifact upload and deploy job from workflow

**Checkpoint**: User Story 3 complete - workflow deploys to gh-pages branch, all US3 tests pass

---

## Phase 6: User Story 4 - Update All Internal Links for New Structure (Priority: P4)

**Goal**: Ensure all links use correct relative paths for subdirectory structure

**Independent Test**: Generate full site, click all links, verify no 404 errors

### Tests for User Story 4

- [X] T035 [P] [US4] Add link format test in tests/unit/test_index.py (verify relative paths: `messages/...`, `readings/...`)
- [X] T036 [P] [US4] Add link sorting test in tests/unit/test_index.py (verify reverse chronological order)
- [X] T037 [US4] Add integration test for complete site generation and link validation

### Implementation for User Story 4

- [X] T038 [US4] Update link generation in src/catholic_liturgy_tools/generator/index.py (ensure relative paths per contracts/html-format.md)
- [X] T039 [US4] Implement reverse chronological sorting for messages list in index generator
- [X] T040 [US4] Implement reverse chronological sorting for readings list in index generator
- [X] T041 [US4] Add link text formatting for readings (include liturgical day title per contracts/html-format.md)

**Checkpoint**: User Story 4 complete - all links work correctly, all US4 tests pass

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, documentation, and cleanup

- [X] T042 [P] Run full test suite and verify 90%+ coverage with `pytest --cov=src/catholic_liturgy_tools --cov-fail-under=90`
- [X] T043 [P] Update CHANGELOG.md with v0.3.0 changes (new _site/ structure, HTML index, gh-pages deployment)
- [X] T044 Generate content locally and verify structure matches contracts (run quickstart.md validation steps)
- [X] T045 Test backward compatibility: verify custom --output-dir paths still work
- [X] T046 Perform one-time migration: move existing content from `_posts/`, `readings/`, `index.md` to `_site/` structure
- [X] T047 Delete old files after successful migration verification (`_posts/`, `readings/`, `index.md`)
- [X] T048 Push feature branch and manually trigger GitHub Actions workflow
- [X] T049 Verify GitHub Pages deployment using artifact-based deployment (no gh-pages branch needed)
- [X] T050 Configure GitHub Pages settings: Settings → Pages → Source: GitHub Actions
- [X] T051 Verify live site at https://etotten.github.io/catholic-liturgy-tools/ loads correctly
- [X] T052 Test all links on live site to ensure no 404 errors
- [X] T053 [P] Update README.md with new site structure information and deployment details

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - US1 can start after Phase 2
  - US2 depends on US1 (needs _site/ structure)
  - US3 depends on US1 and US2 (needs generated content to deploy)
  - US4 depends on US2 (needs HTML index to update links)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories ✅ INDEPENDENT
- **User Story 2 (P2)**: Depends on US1 - needs `_site/` structure in place
- **User Story 3 (P3)**: Depends on US1 and US2 - needs generated content in `_site/` to deploy
- **User Story 4 (P4)**: Depends on US2 - needs HTML index to update link paths

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Tests marked [P] can run in parallel (different test files)
- Implementation tasks follow test tasks
- Story complete before moving to next priority

### Parallel Opportunities

- **Setup tasks**: T002 and T003 can run in parallel
- **Foundational tasks**: T004 and T005 can run in parallel
- **US1 tests**: T006, T007, T008, T009, T010 can all run in parallel (different test files)
- **US1 implementation**: T011 and T012 can run in parallel (different generator files)
- **US2 tests**: T016, T017, T018 can run in parallel (different test files)
- **US4 tests**: T035 and T036 can run in parallel (different test aspects)
- **Polish tasks**: T042, T043, T053 can run in parallel (different files)

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
# T006: Update tests/unit/test_message.py
# T007: Update tests/unit/test_readings_generator.py
# T008: Update tests/unit/test_cli.py
# T009: Update tests/integration/test_message_workflow.py
# T010: Update tests/e2e/test_cli_generate.py

# Launch parallel implementation tasks:
# T011: Update src/catholic_liturgy_tools/generator/message.py
# T012: Update src/catholic_liturgy_tools/generator/readings.py
```

---

## Parallel Example: User Story 2

```bash
# Launch all tests for User Story 2 together:
# T016: Rewrite tests/unit/test_index.py
# T017: Update tests/integration/test_index_workflow.py
# T018: Update tests/e2e/test_cli_index.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (3 tasks)
2. Complete Phase 2: Foundational (2 tasks) - CRITICAL
3. Complete Phase 3: User Story 1 (10 tasks: 5 tests + 5 implementation)
4. **STOP and VALIDATE**: Test US1 independently
5. Generate content, verify `_site/` structure
6. Deploy/demo if ready (or continue to US2 for full MVP)

**Recommended MVP**: Complete through User Story 2 (HTML index) for complete value

### Incremental Delivery

1. **Sprint 1**: Setup + Foundational + US1 → `_site/` structure works
2. **Sprint 2**: US2 → HTML index ready, site viewable in browser
3. **Sprint 3**: US3 + US4 → Live deployment with clean URLs
4. **Sprint 4**: Polish → Production ready

### Sequential Implementation (Single Developer)

1. Phase 1: Setup (30 mins)
2. Phase 2: Foundational (1 hour)
3. Phase 3: User Story 1 (3-4 hours)
   - Write tests first (1.5 hours)
   - Implement changes (1.5 hours)
   - Verify tests pass (0.5 hours)
4. Phase 4: User Story 2 (4-5 hours)
   - Write tests first (1.5 hours)
   - Implement HTML generation (2.5 hours)
   - Verify tests pass (0.5 hours)
5. Phase 5: User Story 3 (2-3 hours)
   - Update workflow (1 hour)
   - Test deployment (1-2 hours)
6. Phase 6: User Story 4 (2 hours)
   - Write tests (0.5 hours)
   - Update links (1 hour)
   - Verify (0.5 hours)
7. Phase 7: Polish (3-4 hours)
   - Migration and testing (2-3 hours)
   - Documentation (1 hour)

**Total Estimated Time**: 15-20 hours

---

## Task Count Summary

- **Total Tasks**: 53
- **Setup Phase**: 3 tasks
- **Foundational Phase**: 2 tasks
- **User Story 1**: 10 tasks (5 tests + 5 implementation)
- **User Story 2**: 11 tasks (4 tests + 7 implementation)
- **User Story 3**: 8 tasks (2 tests + 6 implementation)
- **User Story 4**: 7 tasks (3 tests + 4 implementation)
- **Polish Phase**: 12 tasks

### Parallel Opportunities Identified

- **Setup**: 2 tasks can run in parallel
- **Foundational**: 2 tasks can run in parallel
- **US1**: 5 test tasks + 2 implementation tasks (7 parallel opportunities)
- **US2**: 3 test tasks (3 parallel opportunities)
- **US4**: 2 test tasks (2 parallel opportunities)
- **Polish**: 3 tasks can run in parallel

**Total Parallel Opportunities**: 19 tasks can run in parallel

---

## Independent Test Criteria Per Story

### User Story 1
- ✅ Run `catholic-liturgy generate-message` → file in `_site/messages/`
- ✅ Run `catholic-liturgy generate-readings` → file in `_site/readings/`
- ✅ Run `catholic-liturgy generate-index` → file at `_site/index.html`
- ✅ Verify no files in old locations (`_posts/`, `readings/`, `index.md`)
- ✅ All US1 tests pass

### User Story 2
- ✅ Open `_site/index.html` in browser
- ✅ Verify "Catholic Liturgy Tools" heading displays
- ✅ Verify inline CSS applied (fonts, colors, spacing)
- ✅ Verify two sections: "Daily Messages" and "Daily Readings"
- ✅ View page source, verify HTML5 structure with DOCTYPE
- ✅ All US2 tests pass

### User Story 3
- ✅ Push to feature branch, manually trigger workflow
- ✅ Verify gh-pages branch exists with only _site/ contents at root
- ✅ Configure GitHub Pages: Settings → Pages → gh-pages branch
- ✅ Visit https://etotten.github.io/catholic-liturgy-tools/
- ✅ Verify index loads without `/index.html` in URL
- ✅ All US3 tests pass

### User Story 4
- ✅ Click every link in index page
- ✅ Verify all links navigate correctly (no 404 errors)
- ✅ Verify links use relative paths (`messages/...`, `readings/...`)
- ✅ Verify lists sorted reverse chronologically
- ✅ All US4 tests pass

---

## Suggested MVP Scope

**Minimum Viable Product**: User Stories 1 + 2

**Rationale**:
- US1 establishes `_site/` structure (foundation)
- US2 provides HTML index viewable in browser (user value)
- Can be tested locally without deployment
- Provides immediate improvement to user experience
- US3 and US4 add deployment polish but US1+US2 delivers core functionality

**MVP Deliverable**: Locally generated site with HTML index in clean `_site/` structure

---

## Format Validation

✅ **ALL tasks follow checklist format**: `- [ ] [ID] [P?] [Story?] Description with file path`

**Examples**:
- ✅ `- [ ] T001 Create feature branch` (Setup, no story label)
- ✅ `- [ ] T005 [P] Add constants for new paths in src/catholic_liturgy_tools/constants.py` (Foundational, parallelizable, no story label)
- ✅ `- [ ] T006 [P] [US1] Update unit test for message generator in tests/unit/test_message.py` (User Story 1, parallelizable)
- ✅ `- [ ] T013 [US1] Update CLI command defaults in src/catholic_liturgy_tools/cli.py for generate-message command` (User Story 1, sequential)

---

## Notes

- All tasks include exact file paths for implementation
- Tests written first (TDD approach per constitution)
- Each user story independently testable
- Backward compatibility maintained throughout (--output-dir parameter preserved)
- 90%+ coverage requirement satisfied by comprehensive test tasks
- Git history preserves old files even after deletion (safe to remove old structure)
- One-time migration is manual development task (T046-T047), not automated in CLI

---

**Implementation Ready**: YES  
**Next Action**: Begin Phase 1 (Setup) → T001, T002, T003  
**Estimated Completion**: 15-20 hours total development time
