# Implementation Tasks

**Feature**: Daily Readings from Catholic Lectionary  
**Branch**: 002-daily-readings  
**Date**: 2025-11-22

## Purpose

This document breaks down the implementation into specific, actionable tasks with clear acceptance criteria. Tasks are organized by phase and priority level from [plan.md](./plan.md).

---

## Phase 0: Research & Technical Decisions ✅

**Status**: COMPLETE (research.md created)

- [x] Study USCCB HTML structure for regular weekdays
- [x] Study USCCB HTML structure for Sundays
- [x] Study USCCB HTML structure for major feast days
- [x] Review try1 repo scraper code for patterns
- [x] Design HTML template for readings pages
- [x] Design retry/backoff strategy
- [x] Document all decisions in research.md

---

## Phase 1: Design & Contracts ✅

**Status**: COMPLETE (spec.md, data-model.md, contracts/ created)

- [x] Create spec.md with user stories and requirements
- [x] Create data-model.md with entities and relationships
- [x] Create plan.md with implementation roadmap
- [x] Create research.md with technical decisions
- [x] Create contracts/cli-commands.md
- [x] Create contracts/html-format.md
- [x] Review all specs for completeness

---

## Phase 2: Core Implementation - Priority 1 (Scraper)

**Goal**: Implement reliable USCCB scraper with comprehensive testing

**Estimated Duration**: 3-4 days

### Task 2.1: Create Scraper Module Structure ✅
**Assignee**: Developer  
**Estimated Time**: 30 minutes  
**Completed**: 2025-11-24

- [x] Create `src/catholic_liturgy_tools/scraper/` directory
- [x] Create `src/catholic_liturgy_tools/scraper/__init__.py`
- [x] Create `src/catholic_liturgy_tools/scraper/usccb.py` (stub)
- [x] Create `src/catholic_liturgy_tools/scraper/models.py` (stub)

**Acceptance Criteria**: ✅
- ✅ Directory structure created
- ✅ All `__init__.py` files present
- ✅ Stub files import without errors

---

### Task 2.2: Implement Data Models ✅
**Assignee**: Developer  
**Estimated Time**: 2 hours  
**Completed**: 2025-11-24

- [x] Implement `ReadingEntry` dataclass in `models.py`
  - [x] Add attributes (title, citation, text)
  - [x] Add `validate()` method
  - [x] Add `title_with_citation` property
  - [x] Add docstrings with type hints
- [x] Implement `DailyReading` dataclass in `models.py`
  - [x] Add attributes (date, date_display, liturgical_day, readings, source_url)
  - [x] Add `validate()` method
  - [x] Add `filename` property
  - [x] Add `file_path` property
  - [x] Add docstrings with type hints

**Acceptance Criteria**: ✅
- ✅ Both dataclasses implemented with all attributes
- ✅ Validation methods work correctly
- ✅ Properties return expected values
- ✅ Type hints complete
- ✅ Docstrings comprehensive

**Test Coverage**: ✅ 98% coverage
- [x] Unit tests for `ReadingEntry` validation
- [x] Unit tests for `DailyReading` validation
- [x] Unit tests for derived properties
- [x] Unit tests for edge cases (empty strings, etc.)

---

### Task 2.3: Implement Exception Hierarchy ✅
**Assignee**: Developer  
**Estimated Time**: 1 hour  
**Completed**: 2025-11-24

- [x] Create `src/catholic_liturgy_tools/scraper/exceptions.py`
- [x] Implement exception classes:
  - [x] `LiturgyToolsError` (base)
  - [x] `ScraperError` (base for scraping)
  - [x] `NetworkError` (network issues)
  - [x] `ParseError` (HTML parsing issues)
  - [x] `ValidationError` (data validation)
  - [x] `DateError` (invalid dates)
- [x] Add docstrings explaining when each is raised

**Acceptance Criteria**: ✅
- ✅ All exception classes defined
- ✅ Proper inheritance hierarchy
- ✅ Docstrings complete

---

### Task 2.4: Implement Retry Decorator ✅
**Assignee**: Developer  
**Estimated Time**: 1 hour  
**Completed**: 2025-11-24

- [x] Create `src/catholic_liturgy_tools/utils/retry.py`
- [x] Implement `retry_with_backoff` decorator
- [x] Add parameters: max_attempts, backoff_factor
- [x] Add exponential backoff logic
- [x] Add logging for retry attempts

**Acceptance Criteria**: ✅
- ✅ Decorator works with functions
- ✅ Retries on specified exceptions only
- ✅ Exponential backoff implemented correctly
- ✅ Logging shows retry attempts

**Test Coverage**: ✅ 100% coverage
- [x] Test successful first attempt
- [x] Test retry after failure
- [x] Test max attempts reached
- [x] Test non-retryable exceptions pass through

---

### Task 2.5: Implement USCCBReadingsScraper Class ✅
**Assignee**: Developer  
**Estimated Time**: 4 hours  
**Completed**: 2025-11-24

- [x] Implement `USCCBReadingsScraper` class in `usccb.py`
- [x] Implement `__init__` with configuration
- [x] Implement `_build_url(date) -> str`
- [x] Implement `_fetch_page(url) -> BeautifulSoup`
- [x] Implement `_extract_liturgical_day(soup) -> str`
  - [x] Strategy 1: Extract from `<title>`
  - [x] Strategy 2: Extract from H1 with class
  - [x] Strategy 3: Any H1 tag
- [x] Implement `_extract_readings(soup) -> List[ReadingEntry]`
- [x] Implement `_check_for_multiple_masses(soup, date_str) -> Optional[str]`
- [x] Implement `get_readings_for_date(date) -> DailyReading`
- [x] Add comprehensive docstrings and type hints

**Acceptance Criteria**:
- ✅ All methods implemented
- ✅ User-Agent header set correctly
- ✅ Timeout configured
- ✅ Retry decorator applied to fetch method
- ✅ Error handling comprehensive
- ✅ Logging at appropriate levels

**Status**: ✅ COMPLETED (2025-01-24)
- All methods implemented and verified with fixture HTML
- Successfully extracts 4 readings from test fixtures
- Proper error handling and validation in place

---

### Task 2.6: Create HTML Fixtures for Testing
**Assignee**: Developer  
**Estimated Time**: 2 hours

- [x] Create `tests/fixtures/usccb_html/` directory
- [x] Fetch and save sample HTML files:
  - [x] `weekday_memorial_112225.html` (Memorial of St. Cecilia - 4 readings)
  - [x] `sunday_113024.html` (First Sunday of Advent - 4 readings)
  - [x] `christmas_hub_122524.html` (Christmas Day hub with multiple Mass options)
  - [x] `christmas_day_mass_122524.html` (Christmas Day Mass specific readings)
- [x] Document each fixture's purpose

**Acceptance Criteria**:
- ✅ At least 4 fixture files created
- ✅ Files are real USCCB HTML (not synthetic)
- ✅ Files saved with UTF-8 encoding
- ✅ README in fixtures directory explaining each file

**Status**: ✅ COMPLETED (2025-01-24)
- Created 4 fixture files (total ~244KB)
- Fetched from live USCCB site with proper rate limiting
- README.md documents structure, usage, and HTML patterns

---

### Task 2.7: Write Unit Tests for Scraper
**Assignee**: Developer  
**Estimated Time**: 4 hours

- [x] Create `tests/unit/test_usccb_scraper.py`
- [x] Test `_build_url` with various dates
- [x] Test `_extract_liturgical_day` with fixtures
- [x] Test `_extract_readings` with fixtures
- [x] Test `_check_for_multiple_masses` with fixtures
- [x] Test `get_readings_for_date` with mocked HTTP
- [x] Test error handling (network errors, parse errors)
- [x] Test retry logic (mocked failures)
- [x] Achieve 90%+ coverage on scraper module

**Acceptance Criteria**:
- ✅ All scraper functions tested
- ✅ Mocking used for HTTP requests
- ✅ Fixtures used for HTML parsing
- ✅ Coverage at 92.42% for scraper module (exceeds 90% requirement)
- ✅ All tests pass (44 tests passed)

**Status**: ✅ COMPLETED (2025-11-24)
- Created comprehensive test suite with 44 tests across 7 test classes
- Test coverage: 92.42% (132 statements, 10 uncovered)
- Tests cover initialization, URL building, HTML extraction, error handling, retry logic, and edge cases
- All HTTP requests properly mocked to avoid live network calls
- All 4 HTML fixtures used for realistic parsing tests
- Test execution time: 18.81s

---

### Task 2.8: Write Integration Tests for Scraper
**Assignee**: Developer  
**Estimated Time**: 2 hours

- [x] Create `tests/integration/test_usccb_integration.py`
- [x] Mark tests as `@pytest.mark.slow` and `@pytest.mark.integration`
- [x] Test 3-5 sample dates against live USCCB site
  - [x] Weekday (3-4 readings) - tested Nov 22 and Nov 25
  - [x] Sunday (4-5 readings) - tested Nov 30 and Dec 7 (Advent Sundays)
  - [x] Major feast day - tested Immaculate Conception, Christmas (hub detection)
- [x] Add rate limiting (1 second between requests)
- [x] Allow skipping with `-m "not integration"` flag

**Acceptance Criteria**:
- ✅ Integration tests pass against live site (9 passed, 1 skipped)
- ✅ Tests are appropriately marked with @pytest.mark.slow and @pytest.mark.integration
- ✅ Rate limiting implemented (1 second delay between tests via autouse fixture)
- ✅ Tests can be skipped with `-m "not integration"` (10 tests deselected when skipped)
- ✅ Clear failure messages if USCCB structure changed

**Status**: ✅ COMPLETED (2025-11-24)
- Created comprehensive integration test suite with 10 tests across 5 test classes
- Test results: 9 passed, 1 skipped (Christmas hub detection - expected)
- Tests verified against live USCCB site on Nov 24, 2025
- Rate limiting: 1 second between tests (total runtime: 17 seconds)
- Registered custom pytest markers in pyproject.toml to avoid warnings
- Tests cover weekdays, Sundays, feast days, error handling, and data quality
- Can be skipped with: `pytest -m "not integration"`

---

## Phase 3: Core Implementation - Priority 2 (HTML Generation)

**Goal**: Generate well-formatted HTML pages from scraped data

**Estimated Duration**: 2-3 days

### Task 3.1: Create HTML Utilities Module
**Assignee**: Developer  
**Estimated Time**: 1 hour

- [ ] Create `src/catholic_liturgy_tools/utils/html_utils.py`
- [ ] Implement `sanitize_text(text: str) -> str`
- [ ] Implement `format_paragraph(text: str) -> str`
- [ ] Add docstrings and type hints

**Acceptance Criteria**:
- HTML escaping works correctly
- Special characters handled
- Type hints complete

**Test Coverage**:
- [ ] Test sanitization with special characters
- [ ] Test paragraph formatting
- [ ] Test edge cases (empty strings, None)

---

### Task 3.2: Implement HTML Template Generation
**Assignee**: Developer  
**Estimated Time**: 3 hours

- [ ] Create `src/catholic_liturgy_tools/generator/readings.py`
- [ ] Implement `generate_readings_html(reading: DailyReading) -> str`
  - [ ] Generate HTML structure per contract
  - [ ] Embed CSS styles
  - [ ] Include all readings
  - [ ] Add navigation link
  - [ ] Add attribution section
- [ ] Implement `generate_readings_page(reading: DailyReading, output_dir: str) -> Path`
  - [ ] Create output directory if needed
  - [ ] Write HTML to file
  - [ ] Return file path
- [ ] Add comprehensive docstrings

**Acceptance Criteria**:
- HTML matches contract specification
- All template variables replaced
- File writing works correctly
- UTF-8 encoding used
- Idempotent (overwrite existing files)

---

### Task 3.3: Write Unit Tests for HTML Generation
**Assignee**: Developer  
**Estimated Time**: 3 hours

- [ ] Create `tests/unit/test_readings_generator.py`
- [ ] Test `generate_readings_html` with sample data
- [ ] Verify HTML structure (doctype, head, body)
- [ ] Verify all required elements present
- [ ] Verify CSS embedded correctly
- [ ] Verify special characters sanitized
- [ ] Test `generate_readings_page` with temp directory
- [ ] Test file creation and content
- [ ] Achieve 90%+ coverage on generator module

**Acceptance Criteria**:
- All generator functions tested
- BeautifulSoup used to parse generated HTML
- Structure validated programmatically
- Coverage at 90%+ for generator module
- All tests pass

---

### Task 3.4: Validate Generated HTML
**Assignee**: Developer  
**Estimated Time**: 2 hours

- [ ] Generate sample HTML files manually
- [ ] Validate with W3C HTML5 validator
- [ ] Test rendering in Chrome
- [ ] Test rendering in Firefox
- [ ] Test rendering in Safari (if on macOS)
- [ ] Test responsive design (resize window)
- [ ] Fix any validation or rendering issues

**Acceptance Criteria**:
- HTML validates as HTML5
- Renders correctly in all target browsers
- Responsive design works on mobile sizes
- Navigation links work
- Attribution link works (opens in new tab)

---

## Phase 4: Core Implementation - Priority 3 (Index Updates)

**Goal**: Update index page to include readings

**Estimated Duration**: 1-2 days

### Task 4.1: Implement Readings Scanning
**Assignee**: Developer  
**Estimated Time**: 2 hours

- [ ] Modify `src/catholic_liturgy_tools/generator/index.py`
- [ ] Implement `scan_readings_files(readings_dir: str) -> List[ReadingsEntry]`
  - [ ] Scan directory for `*.html` files
  - [ ] Parse HTML to extract liturgical day name
  - [ ] Extract date from filename
  - [ ] Create ReadingsEntry objects
  - [ ] Sort by date (newest first)
- [ ] Add docstrings and type hints

**Acceptance Criteria**:
- Function scans directory correctly
- Parses HTML files to get liturgical day
- Returns sorted list
- Handles empty directory gracefully

---

### Task 4.2: Update Index Generation
**Assignee**: Developer  
**Estimated Time**: 2 hours

- [ ] Modify `generate_index()` function
- [ ] Add `readings_dir` parameter (default: "readings")
- [ ] Call `scan_readings_files()` in addition to `scan_message_files()`
- [ ] Generate two-section markdown:
  - [ ] "Daily Messages" section
  - [ ] "Daily Readings" section
- [ ] Handle cases where one or both sections are empty
- [ ] Ensure output file is `index.md` (not `index.html`)

**Acceptance Criteria**:
- Index includes both sections
- Both sections sorted correctly
- Links point to correct files
- Works when readings directory is empty
- Works when messages directory is empty
- Output file is `index.md`

---

### Task 4.3: Update Index Tests
**Assignee**: Developer  
**Estimated Time**: 2 hours

- [ ] Modify `tests/unit/test_index.py`
- [ ] Add tests for `scan_readings_files()`
- [ ] Update tests for `generate_index()` to include readings
- [ ] Test with both messages and readings present
- [ ] Test with only messages present
- [ ] Test with only readings present
- [ ] Test with neither present (empty index)
- [ ] Update integration test if needed

**Acceptance Criteria**:
- All new functionality tested
- Edge cases covered
- Coverage maintained at 90%+
- All tests pass

---

## Phase 5: CLI Integration - Priority 4

**Goal**: Provide CLI command for generating readings

**Estimated Duration**: 1-2 days

### Task 5.1: Implement generate-readings Command
**Assignee**: Developer  
**Estimated Time**: 2 hours

- [ ] Modify `src/catholic_liturgy_tools/cli.py`
- [ ] Implement `generate_readings_command(args)` function
  - [ ] Parse date from args (default: today)
  - [ ] Validate date format
  - [ ] Call scraper to fetch readings
  - [ ] Call generator to create HTML
  - [ ] Display progress messages
  - [ ] Handle all error types with user-friendly messages
- [ ] Add command to main parser
- [ ] Add `--date` and `--output-dir` options
- [ ] Add help text following contract

**Acceptance Criteria**:
- Command works with no arguments (today)
- Command works with `--date` parameter
- Command works with `--output-dir` parameter
- Error messages match contract specification
- Exit codes match contract
- Progress messages informative

---

### Task 5.2: Update generate-index Command
**Assignee**: Developer  
**Estimated Time**: 1 hour

- [ ] Modify `generate_index_command()` in `cli.py`
- [ ] Add `--readings-dir` option (default: "readings")
- [ ] Pass readings_dir to `generate_index()`
- [ ] Update output message to show readings count
- [ ] Update help text

**Acceptance Criteria**:
- New option works correctly
- Output message shows both message and reading counts
- Help text updated
- Backward compatible (old usage still works)

---

### Task 5.3: Write E2E Tests for CLI
**Assignee**: Developer  
**Estimated Time**: 3 hours

- [ ] Create `tests/e2e/test_cli_readings.py`
- [ ] Test `generate-readings` with no args
- [ ] Test `generate-readings --date YYYY-MM-DD`
- [ ] Test `generate-readings --output-dir custom/`
- [ ] Test error handling (invalid date, network failure)
- [ ] Test output messages
- [ ] Test file creation
- [ ] Update `tests/e2e/test_cli_index.py` to test readings scanning

**Acceptance Criteria**:
- All CLI workflows tested end-to-end
- Uses real file system (temp directories)
- Mocks network requests for reliability
- All tests pass
- Coverage maintained

---

### Task 5.4: Update README
**Assignee**: Developer  
**Estimated Time**: 1 hour

- [ ] Update `README.md` with new features
- [ ] Document `generate-readings` command
- [ ] Update `generate-index` command documentation
- [ ] Add examples for both commands
- [ ] Add troubleshooting section for scraping issues
- [ ] Add USCCB attribution and source information

**Acceptance Criteria**:
- README comprehensive and accurate
- Examples work as shown
- Clear and well-formatted
- Attribution included

---

## Phase 6: GitHub Actions Automation - Priority 5

**Goal**: Automate readings generation in GitHub Actions

**Estimated Duration**: 1-2 days

### Task 6.1: Update pyproject.toml
**Assignee**: Developer  
**Estimated Time**: 30 minutes

- [ ] Update version to `0.2.0`
- [ ] Add `beautifulsoup4>=4.12.0` dependency
- [ ] Add `lxml>=5.0.0` dependency
- [ ] Update description if needed

**Acceptance Criteria**:
- Version bumped correctly
- New dependencies added
- File still valid TOML

---

### Task 6.2: Update Version in Code
**Assignee**: Developer  
**Estimated Time**: 15 minutes

- [ ] Update `src/catholic_liturgy_tools/__init__.py`
- [ ] Set `__version__ = "0.2.0"`

**Acceptance Criteria**:
- Version matches pyproject.toml
- Imports still work

---

### Task 6.3: Rename and Update GitHub Actions Workflow
**Assignee**: Developer  
**Estimated Time**: 1 hour

- [ ] Rename `.github/workflows/publish-daily-message.yml` to `publish-content.yml`
- [ ] Update workflow name to "Publish Daily Content"
- [ ] Update description
- [ ] Add step to generate readings:
  ```yaml
  - name: Generate daily readings
    run: catholic-liturgy generate-readings
  ```
- [ ] Ensure index generation step still works
- [ ] Update git add to include `readings/` directory:
  ```yaml
  git add _posts/ readings/ index.md
  ```
- [ ] Update commit message to reflect both content types

**Acceptance Criteria**:
- Workflow renamed successfully
- Generates both messages and readings
- Commits all files correctly
- Deploys to GitHub Pages
- Still works with manual trigger

---

### Task 6.4: Update GitHub Actions Trigger Command
**Assignee**: Developer  
**Estimated Time**: 30 minutes

- [ ] Modify `src/catholic_liturgy_tools/github/actions.py` if needed
- [ ] Update default workflow file name to `publish-content.yml`
- [ ] Update tests in `tests/e2e/test_cli_trigger.py`

**Acceptance Criteria**:
- Trigger command uses new workflow name
- Tests updated and passing
- Backward compatible if possible

---

### Task 6.5: Test GitHub Actions Workflow
**Assignee**: Developer  
**Estimated Time**: 1 hour

- [ ] Push changes to feature branch
- [ ] Manually trigger workflow via GitHub UI
- [ ] Monitor workflow execution
- [ ] Verify readings generated and committed
- [ ] Verify index updated correctly
- [ ] Verify site deploys successfully
- [ ] Check live site for new content
- [ ] Fix any issues found

**Acceptance Criteria**:
- Workflow runs successfully
- All files committed to repository
- Site deploys to GitHub Pages
- Live site shows both messages and readings
- Links work correctly

---

## Final Tasks

### Task 7.1: Update All Documentation
**Assignee**: Developer  
**Estimated Time**: 2 hours

- [ ] Review and update README.md
- [ ] Update CHANGELOG.md (if exists) or create it
- [ ] Review all spec documents for accuracy
- [ ] Add any missing documentation
- [ ] Check all links work

**Acceptance Criteria**:
- All documentation accurate and complete
- No broken links
- Clear and well-formatted
- Examples tested and working

---

### Task 7.2: Create Feature Completion Report
**Assignee**: Developer  
**Estimated Time**: 1 hour

- [ ] Create `specs/002-daily-readings/COMPLETION.md`
- [ ] Document what was implemented
- [ ] Document any deviations from plan
- [ ] Document lessons learned
- [ ] Document any technical debt
- [ ] Note any future enhancements

**Acceptance Criteria**:
- Completion report comprehensive
- Honest assessment of implementation
- Lessons learned documented
- Future work identified

---

### Task 7.3: Final Testing and Validation
**Assignee**: Developer  
**Estimated Time**: 2 hours

- [ ] Run full test suite locally
- [ ] Verify 90%+ coverage
- [ ] Test all CLI commands manually
- [ ] Verify HTML validation
- [ ] Test cross-browser
- [ ] Test GitHub Actions workflow
- [ ] Verify live site works
- [ ] Check all links on live site

**Acceptance Criteria**:
- All tests pass
- Coverage at 90%+
- Manual testing successful
- Live site fully functional

---

### Task 7.4: Merge to Main
**Assignee**: Developer  
**Estimated Time**: 30 minutes

- [ ] Create pull request from feature branch
- [ ] Review all changes
- [ ] Ensure CI/CD passes
- [ ] Merge to main branch
- [ ] Tag release: `git tag v0.2.0`
- [ ] Push tag: `git push --tags`
- [ ] Monitor first scheduled run

**Acceptance Criteria**:
- PR created and reviewed
- All checks passing
- Merged without conflicts
- Tagged correctly
- First scheduled run successful

---

## Task Summary by Phase

| Phase | Tasks | Est. Time | Priority |
|-------|-------|-----------|----------|
| Phase 0: Research | 7 tasks | 1-2 days | P0 |
| Phase 1: Design & Contracts | 7 tasks | 1-2 days | P0 |
| Phase 2: Scraper | 8 tasks | 3-4 days | P1 |
| Phase 3: HTML Generation | 4 tasks | 2-3 days | P2 |
| Phase 4: Index Updates | 3 tasks | 1-2 days | P3 |
| Phase 5: CLI Integration | 4 tasks | 1-2 days | P4 |
| Phase 6: GitHub Actions | 5 tasks | 1-2 days | P5 |
| Final Tasks | 4 tasks | 1 day | P5 |
| **Total** | **42 tasks** | **10-15 days** | - |

---

## Progress Tracking

Use this section to track overall progress:

**Phases Complete**: 2/8 (Phase 0, Phase 1)

**Tasks Complete**: 14/42 (33%)

**Current Phase**: Phase 2 (Scraper Implementation)

**Blockers**: None

**Notes**: Specification phase complete and ready for implementation.

---

**Document Status**: Complete - ready for implementation tracking
