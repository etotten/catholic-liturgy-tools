---
description: "Task list for implementing site content preservation and accumulation"
---

# Tasks: 004-preserve-site-history

**Input**: Design documents from `/specs/004-preserve-site-history/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli-commands.md, contracts/github-actions.md, quickstart.md

**Tests**: Tests are included as this feature requires verification of accumulation behavior and regression prevention.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below are absolute from repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and workflow configuration validation

- [ ] T001 Verify current workflow structure in `.github/workflows/publish-content.yml`
- [ ] T002 [P] Review current CLI command implementations for content generation
- [ ] T003 [P] Verify Python 3.13 configuration in workflow and pyproject.toml

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Modify workflow permissions from `contents: read` to `contents: write` in `.github/workflows/publish-content.yml`
- [ ] T005 Add new workflow step "Commit generated content to repository" after "Generate index page" step in `.github/workflows/publish-content.yml`
- [ ] T006 Configure Git user credentials (github-actions[bot]) in new commit step
- [ ] T007 Implement git add, commit, and push commands for `_site/` directory in new workflow step
- [ ] T008 Add idempotent handling for "nothing to commit" scenario in workflow

**Checkpoint**: Foundation ready - workflow can now preserve content between runs

---

## Phase 3: User Story 1 - Accumulate Content Across Runs (Priority: P1) 🎯 MVP

**Goal**: Generated content accumulates in _site/ directory over time, persisted via Git commits in workflow

**Independent Test**: Trigger workflow multiple times for different dates, verify _site/ contains all generated files with increasing count

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T009 [P] [US1] Create integration test `tests/integration/test_content_accumulation.py` to verify multiple runs accumulate files
- [ ] T010 [P] [US1] Create test helper in `tests/integration/test_content_accumulation.py` to simulate workflow runs
- [ ] T011 [P] [US1] Add test case for message accumulation: verify 3 dates produce 3 message files
- [ ] T012 [P] [US1] Add test case for readings accumulation: verify 3 dates produce 3 readings files

### Implementation for User Story 1

- [ ] T013 [US1] Validate that CLI commands (generate-message, generate-readings) preserve existing directory contents
- [ ] T014 [US1] Test workflow change locally using `act` or manual workflow_dispatch trigger
- [ ] T015 [US1] Verify git commit step executes successfully on first workflow run
- [ ] T016 [US1] Verify git commit step handles "nothing to commit" on repeat run

**Checkpoint**: At this point, content accumulation should work - workflow persists _site/ across runs

---

## Phase 4: User Story 2 - Index Shows Full History (Priority: P2)

**Goal**: Index page lists all accumulated content in reverse chronological order

**Independent Test**: After multiple workflow runs, verify index.html shows all dates with newest first

### Tests for User Story 2 ⚠️

- [ ] T017 [P] [US2] Create integration test `tests/integration/test_index_accumulation.py` to verify index lists all content
- [ ] T018 [P] [US2] Add test case: generate 5 dates of content, verify index contains 5 entries
- [ ] T019 [P] [US2] Add test case: verify index maintains reverse chronological order (newest first)
- [ ] T020 [P] [US2] Add test case: verify index includes both messages and readings links

### Implementation for User Story 2

- [ ] T021 [US2] Verify `src/catholic_liturgy_tools/generator/index.py` scan_message_files() works correctly with accumulated content
- [ ] T022 [US2] Verify `src/catholic_liturgy_tools/generator/index.py` scan_readings_files() works correctly with accumulated content
- [ ] T023 [US2] Validate index generation produces correct HTML with all historical entries
- [ ] T024 [US2] Test index page rendering in browser with 10+ dates of content

**Checkpoint**: At this point, index page should display full content history correctly

---

## Phase 5: User Story 3 - Prevent Content Loss (Priority: P3)

**Goal**: Same-date regeneration overwrites safely, workflow handles edge cases without data loss

**Independent Test**: Regenerate content for existing date, verify overwrite works and other dates preserved

### Tests for User Story 3 ⚠️

- [ ] T025 [P] [US3] Create integration test `tests/integration/test_overwrite_behavior.py` to verify same-date regeneration
- [ ] T026 [P] [US3] Add test case: generate date X twice, verify only one file for date X exists
- [ ] T027 [P] [US3] Add test case: generate date X, Y, regenerate X, verify both X and Y still exist
- [ ] T028 [P] [US3] Add test case: verify workflow handles empty _site/ directory on first run

### Implementation for User Story 3

- [ ] T029 [US3] Validate CLI commands handle overwrite scenario (same date, different content)
- [ ] T030 [US3] Test workflow commit step handles "no changes" when regenerating same date with same content
- [ ] T031 [US3] Verify workflow doesn't create empty commits when content unchanged
- [ ] T032 [US3] Add workflow documentation comment explaining content preservation behavior

**Checkpoint**: All user stories should now be independently functional with safe overwrite behavior

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [ ] T033 [P] Update `quickstart.md` with actual test results and validation steps
- [ ] T034 [P] Add workflow monitoring documentation in `specs/004-preserve-site-history/research.md`
- [ ] T035 Run full test suite to verify 90% coverage maintained (per constitution)
- [ ] T036 Execute `quickstart.md` validation scenarios end-to-end
- [ ] T037 [P] Update `CHANGELOG.md` with feature 004 changes
- [ ] T038 [P] Create PR description with before/after workflow comparison
- [ ] T039 Manual verification: trigger workflow for new date, check GitHub commit history
- [ ] T040 Manual verification: check GitHub Pages deployment shows accumulated content

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational (Phase 2) - No dependencies on other stories
  - User Story 2 (P2): Can start after Foundational (Phase 2) - Depends on US1 for content to exist, but validates index logic independently
  - User Story 3 (P3): Can start after Foundational (Phase 2) - Depends on US1 for workflow behavior, validates overwrite safety
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: FOUNDATIONAL - Must complete first. Enables content accumulation via workflow commits.
- **User Story 2 (P2)**: Depends on US1 (needs accumulated content to verify index). Tests index correctness with multiple dates.
- **User Story 3 (P3)**: Depends on US1 (needs workflow commits working). Tests edge cases and safety of overwrite behavior.

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Integration tests before validation
- Core implementation before edge case handling
- Story complete before moving to next priority

### Parallel Opportunities

- **Setup (Phase 1)**: All 3 tasks can run in parallel
- **Foundational (Phase 2)**: T004-T008 are sequential (workflow modification steps in order)
- **User Story 1 Tests**: T009-T012 can all run in parallel (different test cases)
- **User Story 1 Implementation**: T013-T016 are sequential (validation steps)
- **User Story 2 Tests**: T017-T020 can all run in parallel (different test cases)
- **User Story 2 Implementation**: T021-T024 are sequential (validation steps)
- **User Story 3 Tests**: T025-T028 can all run in parallel (different test cases)
- **User Story 3 Implementation**: T029-T032 are sequential (validation steps)
- **Polish (Phase 6)**: T033-T034, T037-T038 can run in parallel (documentation updates)

**Critical Path**: Phase 1 → Phase 2 → User Story 1 → User Story 2 → User Story 3 → Polish

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task T009: "Create integration test tests/integration/test_content_accumulation.py"
Task T010: "Create test helper in tests/integration/test_content_accumulation.py"
Task T011: "Add test case for message accumulation"
Task T012: "Add test case for readings accumulation"

# After tests written and failing, run implementation sequentially:
Task T013: "Validate CLI commands preserve existing directory contents"
Task T014: "Test workflow change locally"
Task T015: "Verify git commit step on first run"
Task T016: "Verify git commit step handles nothing to commit"
```

---

## Parallel Example: User Story 2

```bash
# Launch all tests for User Story 2 together:
Task T017: "Create integration test tests/integration/test_index_accumulation.py"
Task T018: "Add test case: verify index contains 5 entries"
Task T019: "Add test case: verify reverse chronological order"
Task T020: "Add test case: verify index includes messages and readings links"

# After tests written and failing, run implementation sequentially:
Task T021: "Verify scan_message_files() works with accumulated content"
Task T022: "Verify scan_readings_files() works with accumulated content"
Task T023: "Validate index generation produces correct HTML"
Task T024: "Test index page rendering with 10+ dates"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (Tasks T001-T003)
2. Complete Phase 2: Foundational (Tasks T004-T008) - CRITICAL workflow changes
3. Complete Phase 3: User Story 1 (Tasks T009-T016)
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Trigger workflow manually for date 1
   - Trigger workflow manually for date 2
   - Verify _site/ contains both dates
   - Verify Git commits show both additions
5. Deploy/demo if ready - MVP achieved!

**Estimated Time**: ~2-3 hours for MVP (Phases 1-3)

### Incremental Delivery

1. **Complete Setup + Foundational** (1 hour) → Workflow can commit _site/
2. **Add User Story 1** (1-2 hours) → Test accumulation works → Deploy/Demo (MVP!)
3. **Add User Story 2** (1 hour) → Test index lists all content → Deploy/Demo
4. **Add User Story 3** (1 hour) → Test overwrite safety → Deploy/Demo
5. **Polish** (1 hour) → Documentation and final validation

**Total Estimated Time**: ~5-6 hours for complete feature

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers (not typical for this project, but possible):

1. Team completes Setup + Foundational together (~1 hour)
2. Once Foundational is done:
   - Developer A: User Story 1 (accumulation tests and validation)
   - Developer B: User Story 2 (index tests - will need to wait for US1 to have data)
   - Developer C: User Story 3 (overwrite tests - will need to wait for US1 workflow)
3. Stories complete and integrate independently

**Note**: Due to dependencies (US2 and US3 need US1 complete), sequential implementation is more practical for this feature.

---

## Notes

- **[P] tasks** = different files, no dependencies
- **[Story] label** maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD approach)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- **CRITICAL**: No Python code changes needed - only workflow modification
- **CRITICAL**: CLI commands remain pure generators (no Git operations)
- **CRITICAL**: Workflow handles all Git commits for content persistence

---

## Success Criteria

### User Story 1 Success (MVP)

- ✅ Workflow runs successfully with new commit step
- ✅ Multiple workflow runs accumulate files in _site/
- ✅ Git history shows commits for each workflow run
- ✅ File count increases with each run

### User Story 2 Success

- ✅ Index page lists all accumulated dates
- ✅ Index maintains reverse chronological order
- ✅ Index includes links to all messages and readings

### User Story 3 Success

- ✅ Same-date regeneration overwrites safely
- ✅ Other dates remain untouched during overwrite
- ✅ Workflow handles edge cases without errors
- ✅ No empty commits or Git conflicts

### Overall Feature Success

- ✅ All 40 tasks completed
- ✅ 90% test coverage maintained (per constitution)
- ✅ All integration tests passing
- ✅ quickstart.md validation scenarios pass
- ✅ GitHub Pages shows accumulated content history
- ✅ Manual verification confirms expected behavior
