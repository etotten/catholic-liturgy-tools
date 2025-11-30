# Tasks: Daily Reflections with AI-Augmented Content

**Input**: Design documents from `/specs/005-daily-reflections/`  
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: 90%+ coverage required per constitution Principle 4. All test tasks included below are REQUIRED.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **- [ ]**: Checkbox for tracking completion
- **[ID]**: Sequential task ID (T001, T002, ...)
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

Project uses single Python package structure:
- Source code: `src/catholic_liturgy_tools/`
- Tests: `tests/unit/`, `tests/integration/`, `tests/e2e/`
- Data: `data/` (for prayer database)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependencies, and prayer database

- [ ] T001 Add dependencies to pyproject.toml: anthropic>=0.8.0, python-dotenv>=1.0.0
- [ ] T002 Install Node.js dependencies for romcal (liturgical calendar): npm install romcal
- [ ] T003 Create .env.example file with ANTHROPIC_API_KEY and ANTHROPIC_MAX_COST_PER_REFLECTION placeholders
- [ ] T004 [P] Update .gitignore to exclude .env file
- [ ] T005 [P] Create data/ directory for prayer database
- [ ] T006 AI generates data/prayers.json with 20-30 lesser-known Catholic prayers from 5 approved sources (excluding Hail Mary, Our Father, Glory Be)
- [ ] T007 Human reviews data/prayers.json for theological accuracy and appropriateness
- [ ] T008 Human commits data/prayers.json to repository (approval via Git commit)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### AI Module (Core Infrastructure)

- [ ] T009 [P] Create src/catholic_liturgy_tools/ai/__init__.py module initialization
- [ ] T010 [P] Implement AnthropicClient wrapper in src/catholic_liturgy_tools/ai/client.py with load_dotenv() for environment variables
- [ ] T011 [P] Create AI response models in src/catholic_liturgy_tools/ai/models.py: ReadingSynopsis, DailyReflection, CCCCitation
- [ ] T012 [P] Implement prompt templates in src/catholic_liturgy_tools/ai/prompts.py following contracts/ai-prompts.md
- [ ] T013 [P] Implement CostTracker in src/catholic_liturgy_tools/ai/cost_tracker.py with $0.04 limit enforcement

### Liturgy Module (Core Infrastructure)

- [ ] T014 [P] Create src/catholic_liturgy_tools/liturgy/__init__.py module initialization
- [ ] T015 [P] Implement liturgical calendar wrapper in src/catholic_liturgy_tools/liturgy/calendar.py calling romcal via subprocess with UTC timezone handling
- [ ] T016 [P] Implement prayer loader in src/catholic_liturgy_tools/liturgy/prayers.py to load and select from data/prayers.json
- [ ] T017 [P] Implement CCC validator in src/catholic_liturgy_tools/liturgy/ccc_validator.py with range 1-2865 validation

### Data Models (Core Infrastructure)

- [ ] T018 Extend existing DailyReading model in src/catholic_liturgy_tools/scraper/models.py with new optional attributes: synopses, reflection, prayer, feast_info, cost_summary, generation_timestamp, ai_service_status
- [ ] T019 [P] Create SourcedPrayer dataclass in src/catholic_liturgy_tools/scraper/models.py per data-model.md
- [ ] T020 [P] Create FeastDayInfo and SaintBiography dataclasses in src/catholic_liturgy_tools/scraper/models.py per data-model.md
- [ ] T021 [P] Create ReflectionCostSummary dataclass in src/catholic_liturgy_tools/scraper/models.py per data-model.md

### Test Infrastructure

- [ ] T022 [P] Update tests/conftest.py with AI mocking fixtures using pytest-mock
- [ ] T023 [P] Create tests/fixtures/sample_prayers.json with test prayer data
- [ ] T024 [P] Create tests/fixtures/sample_readings.json with test reading data

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View Daily Reading with AI-Generated Synopsis (Priority: P1) 🎯 MVP

**Goal**: Generate one-line synopses for each Scripture reading to make readings more accessible

**Independent Test**: Visit any daily readings page and verify each Scripture passage has a one-line italicized synopsis above it

### Tests for User Story 1 (TDD - Write First, Ensure Fail)

- [ ] T025 [P] [US1] Unit test for synopsis generation in tests/unit/test_ai_client.py (should fail initially)
- [ ] T026 [P] [US1] Unit test for prompt template in tests/unit/test_prompts.py (should fail initially)
- [ ] T027 [P] [US1] Unit test for cost tracking in tests/unit/test_cost_tracker.py (should fail initially)
- [ ] T028 [P] [US1] Integration test for synopsis workflow in tests/integration/test_synopsis_workflow.py (should fail initially)
- [ ] T029 [P] [US1] E2E test for CLI with --with-reflections in tests/e2e/test_cli_readings.py (should fail initially)

### Implementation for User Story 1

- [ ] T030 [US1] Implement generate_synopsis() method in src/catholic_liturgy_tools/ai/client.py using synopsis prompt template
- [ ] T031 [US1] Add synopsis generation to generate_readings() in src/catholic_liturgy_tools/generator/readings.py
- [ ] T032 [US1] Update HTML template in src/catholic_liturgy_tools/generator/readings.py to display synopses in italics above readings
- [ ] T033 [US1] Add error handling for AI service failures with graceful degradation (display readings without synopses)
- [ ] T034 [US1] Verify all US1 tests now pass (T025-T029)

**Checkpoint**: At this point, User Story 1 should be fully functional - readings display with synopses

---

## Phase 4: User Story 2 - Read Integrated Daily Reflection (Priority: P2)

**Goal**: Generate unified reflection synthesizing all readings with pondering questions and CCC citations

**Independent Test**: View daily readings page and confirm reflection section appears after all readings with synthesized insights, 2-3 questions, and 1-2 CCC citations

### Tests for User Story 2 (TDD - Write First, Ensure Fail)

- [ ] T035 [P] [US2] Unit test for reflection generation in tests/unit/test_ai_client.py (should fail initially)
- [ ] T036 [P] [US2] Unit test for CCC validation in tests/unit/test_ccc_validator.py (should fail initially)
- [ ] T037 [P] [US2] Unit test for reflection prompt template in tests/unit/test_prompts.py (should fail initially)
- [ ] T038 [P] [US2] Integration test for reflection workflow in tests/integration/test_reflection_workflow.py (should fail initially)
- [ ] T039 [P] [US2] E2E test for reflection display in tests/e2e/test_cli_readings.py (should fail initially)

### Implementation for User Story 2

- [ ] T040 [US2] Implement generate_reflection() method in src/catholic_liturgy_tools/ai/client.py using reflection prompt template
- [ ] T041 [US2] Implement validate_ccc_paragraph() in src/catholic_liturgy_tools/liturgy/ccc_validator.py
- [ ] T042 [US2] Add reflection generation to generate_readings() in src/catholic_liturgy_tools/generator/readings.py
- [ ] T043 [US2] Update HTML template to display reflection section with questions and CCC citations
- [ ] T044 [US2] Add retry logic for invalid CCC citations (up to 3 retries with corrected prompt)
- [ ] T045 [US2] Update cost tracking to aggregate synopsis + reflection costs and enforce $0.04 limit
- [ ] T046 [US2] Verify all US2 tests now pass (T035-T039)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - synopses + reflection displayed

---

## Phase 5: User Story 3 - Begin with Relevant Prayer (Priority: P2)

**Goal**: Display relevant Catholic prayer at top of page with attribution and source link

**Independent Test**: Visit readings page and verify prayer appears at top with proper attribution and source link to Catholic website

### Tests for User Story 3 (TDD - Write First, Ensure Fail)

- [ ] T047 [P] [US3] Unit test for prayer loading in tests/unit/test_prayers.py (should fail initially)
- [ ] T048 [P] [US3] Unit test for prayer selection algorithm in tests/unit/test_prayers.py (should fail initially)
- [ ] T049 [P] [US3] Integration test for prayer workflow in tests/integration/test_prayer_workflow.py (should fail initially)
- [ ] T050 [P] [US3] E2E test for prayer display in tests/e2e/test_cli_readings.py (should fail initially)

### Implementation for User Story 3

- [ ] T051 [US3] Implement load_prayers() in src/catholic_liturgy_tools/liturgy/prayers.py to load data/prayers.json
- [ ] T052 [US3] Implement select_prayer() in src/catholic_liturgy_tools/liturgy/prayers.py with liturgical context matching (per prayer-database-schema.md)
- [ ] T053 [US3] Integrate prayer selection in generate_readings() in src/catholic_liturgy_tools/generator/readings.py
- [ ] T054 [US3] Update HTML template to display prayer at top with source attribution and clickable link
- [ ] T055 [US3] Add fallback to default prayer (Prayer before Scripture) if no match found
- [ ] T056 [US3] Verify all US3 tests now pass (T047-T050)

**Checkpoint**: All core features working - synopses + reflection + prayer displayed

---

## Phase 6: User Story 4 - Learn About Feast Days and Saints (Priority: P3)

**Goal**: Display feast day information and saint biographies on appropriate days

**Independent Test**: View readings page on known feast day and confirm biographical section appears with all required elements

### Tests for User Story 4 (TDD - Write First, Ensure Fail)

- [ ] T057 [P] [US4] Unit test for romcal calendar wrapper in tests/unit/test_calendar.py (should fail initially)
- [ ] T058 [P] [US4] Unit test for feast day detection in tests/unit/test_calendar.py (should fail initially)
- [ ] T059 [P] [US4] Integration test for feast day workflow in tests/integration/test_feast_day_workflow.py (should fail initially)
- [ ] T060 [P] [US4] E2E test for saint biography display in tests/e2e/test_cli_readings.py (should fail initially)

### Implementation for User Story 4

- [ ] T061 [US4] Implement get_liturgical_day() in src/catholic_liturgy_tools/liturgy/calendar.py using romcal with UTC timezone
- [ ] T062 [US4] Implement parse_feast_info() in src/catholic_liturgy_tools/liturgy/calendar.py to extract feast type and saint info
- [ ] T063 [US4] Integrate feast day detection in generate_readings() in src/catholic_liturgy_tools/generator/readings.py
- [ ] T064 [US4] For saint days: fetch biographical information from Catholic sources (Catholic Online, EWTN) and populate SaintBiography
- [ ] T065 [US4] Update HTML template to display feast day synopsis or saint biography section
- [ ] T066 [US4] Update prayer selection to prioritize feast-specific prayers when applicable
- [ ] T067 [US4] Verify all US4 tests now pass (T057-T060)

**Checkpoint**: All user stories complete and independently functional

---

## Phase 7: CLI Integration & Environment Management

**Purpose**: Extend CLI with reflection options and environment variable management

- [ ] T068 Update src/catholic_liturgy_tools/cli.py to load environment variables using load_dotenv() at module initialization
- [ ] T069 [P] Add --with-reflections/--no-reflections flags to generate-readings command in src/catholic_liturgy_tools/cli.py
- [ ] T070 [P] Add validation for ANTHROPIC_API_KEY environment variable with helpful error message
- [ ] T071 [P] Update CLI help text and error messages per contracts/cli-commands.md
- [ ] T072 [P] Add cost reporting to CLI output (display total cost after generation)
- [ ] T073 [P] Update tests/e2e/test_cli_readings.py to cover all new CLI options
- [ ] T074 Verify graceful degradation when --with-reflections used but API key missing

---

## Phase 8: GitHub Actions Scheduled Generation

**Purpose**: Automate daily generation at 6:00 AM CT

- [ ] T075 Update .github/workflows/publish-site.yml schedule to cron: '0 12 * * *' (12:00 PM UTC = 6:00 AM CST)
- [ ] T076 Add ANTHROPIC_API_KEY to GitHub repository secrets
- [ ] T077 Add ANTHROPIC_MAX_COST_PER_REFLECTION to GitHub repository variables (set to 0.04)
- [ ] T078 Update workflow to use secrets.ANTHROPIC_API_KEY and vars.ANTHROPIC_MAX_COST_PER_REFLECTION
- [ ] T079 Add workflow step to generate reflections using catholic-liturgy-tools generate-readings
- [ ] T080 Add error handling in workflow for AI service failures (continue with readings-only on failure)
- [ ] T081 Update workflow to commit and push generated reflections to repository

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements affecting multiple components

### Documentation

- [ ] T082 [P] Update README.md with reflection feature overview and setup instructions
- [ ] T083 [P] Document .env file setup in docs/ or README.md
- [ ] T084 [P] Add CHANGELOG.md entry for version 0.3.0 (new reflection features)
- [ ] T085 [P] Update quickstart.md if any setup steps changed during implementation

### Code Quality

- [ ] T086 Run pytest to verify 90%+ coverage across all modules
- [ ] T087 Run pylint/flake8 and fix any code quality issues
- [ ] T088 Review and refactor any duplicated code across modules
- [ ] T089 Add docstrings to all public functions and classes

### Security & Error Handling

- [ ] T090 [P] Verify .env file is in .gitignore and never committed
- [ ] T091 [P] Add comprehensive logging for all AI API calls and errors
- [ ] T092 [P] Test error scenarios: API timeout, invalid response, rate limiting, network failures
- [ ] T093 [P] Verify cost limit enforcement works correctly (test with mock high-cost scenarios)

### Validation

- [ ] T094 Run through quickstart.md end-to-end to validate all instructions
- [ ] T095 Generate reflections for 5 different dates (ordinary days, feast days, saint days) and manually review for quality
- [ ] T096 Test on-demand historical date generation for dates without existing reflections
- [ ] T097 Verify prayer database has appropriate coverage for all liturgical seasons

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational) ← BLOCKS all user stories
    ↓
├─→ Phase 3 (US1: Synopses) ← MVP
├─→ Phase 4 (US2: Reflection) ← Can start after Phase 2
├─→ Phase 5 (US3: Prayer) ← Can start after Phase 2
└─→ Phase 6 (US4: Feast Days) ← Can start after Phase 2
    ↓
Phase 7 (CLI Integration) ← Needs all desired user stories complete
    ↓
Phase 8 (GitHub Actions) ← Needs Phase 7
    ↓
Phase 9 (Polish) ← Needs all features complete
```

### User Story Dependencies

- **User Story 1 (P1)**: Depends only on Phase 2 (Foundational) - No dependencies on other stories
- **User Story 2 (P2)**: Depends only on Phase 2 (Foundational) - Uses synopses from US1 for context but can work independently
- **User Story 3 (P2)**: Depends only on Phase 2 (Foundational) - Completely independent of US1/US2
- **User Story 4 (P3)**: Depends only on Phase 2 (Foundational) - Independent but integrates with prayer selection from US3

### Within Each User Story

1. **Tests FIRST** - Write all tests for the story, verify they FAIL
2. **Models** - Create data models needed for the story
3. **Core Logic** - Implement business logic (services, algorithms)
4. **Integration** - Wire into existing generator/CLI
5. **HTML/UI** - Update templates to display new content
6. **Verify Tests PASS** - Confirm all tests now pass

### Parallel Opportunities

#### Phase 1 (Setup)
```bash
# Can run simultaneously:
T002 (npm install romcal)
T004 (update .gitignore)
T005 (create data/ directory)
```

#### Phase 2 (Foundational)
```bash
# AI module files (all parallel):
T009, T010, T011, T012, T013

# Liturgy module files (all parallel):
T014, T015, T016, T017

# Model files (all parallel):
T019, T020, T021

# Test infrastructure (all parallel):
T022, T023, T024
```

#### User Story Tests (Within Each Phase)
```bash
# US1 Tests (all parallel after Phase 2):
T025, T026, T027, T028, T029

# US2 Tests (all parallel after Phase 2):
T035, T036, T037, T038, T039

# US3 Tests (all parallel after Phase 2):
T047, T048, T049, T050

# US4 Tests (all parallel after Phase 2):
T057, T058, T059, T060
```

#### Cross-Story Parallelization
```bash
# After Phase 2 completes, ALL user stories can start in parallel:
Phase 3 (US1) || Phase 4 (US2) || Phase 5 (US3) || Phase 6 (US4)
```

#### Phase 7 (CLI Integration) - All parallel
```bash
T069, T070, T071, T072, T073
```

#### Phase 9 (Polish) - Documentation parallel
```bash
T082, T083, T084, T085
```

#### Phase 9 (Polish) - Security parallel
```bash
T090, T091, T092, T093
```

---

## Parallel Example: User Story 1 Implementation

```bash
# Step 1: Write all tests in parallel (should FAIL)
Parallel:
  - T025: Unit test for synopsis generation
  - T026: Unit test for prompt template
  - T027: Unit test for cost tracking
  - T028: Integration test for synopsis workflow
  - T029: E2E test for CLI with reflections

# Step 2: Implement (sequential due to dependencies)
Sequential:
  - T030: Implement generate_synopsis() method
  - T031: Add synopsis generation to readings generator
  - T032: Update HTML template
  - T033: Add error handling
  - T034: Verify all tests pass
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

**Goal**: Ship minimum viable feature quickly

1. ✅ Complete Phase 1: Setup (T001-T008)
2. ✅ Complete Phase 2: Foundational (T009-T024) ← CRITICAL GATE
3. ✅ Complete Phase 3: User Story 1 (T025-T034) ← MVP
4. ✅ Complete Phase 7: CLI Integration (T068-T074)
5. **STOP and VALIDATE**: Generate readings for 3 different dates, verify synopses display correctly
6. Optional: Deploy to staging for user feedback

**Deliverable**: Daily readings with AI-generated synopses - immediate value to users

### Incremental Delivery (Recommended)

**Goal**: Add value progressively, each increment independently testable

1. ✅ Foundation (Phase 1 + Phase 2) → Can generate basic AI content
2. ✅ **MVP** (Phase 3) → Synopses displayed → **DEPLOY/DEMO**
3. ✅ Enhanced (Phase 4) → Add reflections → **DEPLOY/DEMO**
4. ✅ Complete (Phase 5 + Phase 6) → Add prayers + feast days → **DEPLOY/DEMO**
5. ✅ Automated (Phase 7 + Phase 8) → CLI + scheduled generation → **DEPLOY/DEMO**
6. ✅ Polished (Phase 9) → Final quality pass → **DEPLOY/DEMO**

**Benefits**: 
- Each phase delivers working feature
- Early user feedback
- Risk mitigation (can stop at any phase)
- Clear progress milestones

### Parallel Team Strategy (If Multiple Developers)

**Goal**: Maximize throughput with parallel work

1. **Week 1**: Entire team on Phase 1-2 (foundation must be solid)
2. **Week 2+**: Split team after foundation complete:
   - Developer A: User Story 1 (P1) - MVP priority
   - Developer B: User Story 3 (P2) - Independent work on prayers
   - Developer C: User Story 4 (P3) - Independent work on feast days
3. **Week 3**: Developer A completes US1, then picks up US2 (depends on US1 context)
4. **Week 4**: Integration and polish (Phase 7-9)

**Key**: Foundation (Phase 2) is the critical path - must be complete before stories can parallelize

---

## Cost Estimates

### Development Time (Single Developer)

- **Phase 1 (Setup)**: 2-4 hours
- **Phase 2 (Foundational)**: 16-24 hours (most complex: AI client, liturgical calendar)
- **Phase 3 (US1: Synopses)**: 8-12 hours (includes tests)
- **Phase 4 (US2: Reflection)**: 12-16 hours (includes CCC validation, complex prompting)
- **Phase 5 (US3: Prayer)**: 6-8 hours (includes selection algorithm)
- **Phase 6 (US4: Feast Days)**: 8-12 hours (includes romcal integration, saint data)
- **Phase 7 (CLI)**: 4-6 hours
- **Phase 8 (GitHub Actions)**: 2-4 hours
- **Phase 9 (Polish)**: 8-12 hours (testing, documentation, validation)

**Total**: ~66-98 hours for complete implementation

**MVP Only** (Phase 1-3 + Phase 7): ~30-46 hours

### AI API Costs (Anthropic Claude 3.5 Sonnet)

- **Per reflection**: ~$0.016-0.020 (well under $0.04 limit)
- **Daily cost**: $0.016-0.020
- **Monthly cost**: ~$0.48-0.60 (30 days)
- **Annual cost**: ~$5.84-7.30 (365 days)

**Budget**: $0.04 per reflection allows 2x safety margin for feast days and retries

---

## Notes

- **[P] tasks**: Different files, no dependencies - can run in parallel
- **[Story] labels**: Map tasks to specific user stories for traceability
- **Checkbox format**: All tasks use `- [ ]` for tracking completion
- **Test-First**: All user story tests written before implementation
- **Independent Stories**: Each user story can be completed and tested independently
- **Graceful Degradation**: System displays readings without AI content if generation fails
- **Human Review Gate**: Prayer database (T006-T008) requires human approval before proceeding
- **Constitution Compliance**: 90%+ test coverage enforced in Phase 9 (T086)
- **Security**: .env file never committed (T090), API keys in secrets only (T076-T078)

---

## Success Metrics

### Completion Criteria

- [ ] All 97 tasks complete
- [ ] 90%+ test coverage verified (pytest-cov)
- [ ] All user stories independently testable and functional
- [ ] Quickstart.md validation passes (T094)
- [ ] Manual quality review passes for 5+ different dates (T095)
- [ ] GitHub Actions workflow successfully generates and publishes reflections
- [ ] AI API costs remain under $0.04 per reflection for 95% of generations (30-day sample)

### User Story Verification

- [ ] **US1 (Synopses)**: Each reading has one-line synopsis in italics
- [ ] **US2 (Reflection)**: Unified reflection with 2-3 questions and 1-2 CCC citations
- [ ] **US3 (Prayer)**: Prayer at top with attribution and source link
- [ ] **US4 (Feast Days)**: Saint biography or feast synopsis on appropriate days

### Quality Gates

- [ ] All unit tests pass (pytest tests/unit/)
- [ ] All integration tests pass (pytest tests/integration/)
- [ ] All E2E tests pass (pytest tests/e2e/)
- [ ] No theological errors in AI-generated content (manual review)
- [ ] Prayer database includes 20-30 prayers from 5 approved sources
- [ ] Error handling works for all failure scenarios (API timeout, rate limit, network failure, cost exceeded)
