# Implementation Plan: Daily Readings from Catholic Lectionary

**Branch**: `002-daily-readings` | **Date**: 2025-11-22 | **Spec**: [spec.md](./spec.md)

## Summary

Add a complete Daily Readings feature that fetches Catholic liturgical readings from USCCB.org, generates standalone HTML pages for each day, updates the index page to include both messages and readings, and integrates with the existing GitHub Actions workflow for automated publishing. The implementation follows a thin-slice approach with 5 priority levels (P1-P5), starting with scraper development, then HTML generation, index updates, CLI integration, and finally GitHub Actions automation.

---

## Technical Context

**Language/Version**: Python 3.11  

**Primary Dependencies**: 
- `beautifulsoup4` (NEW): HTML parsing for scraping USCCB site
- `lxml` (NEW): Fast HTML parser backend for BeautifulSoup
- `requests` (EXISTING): HTTP client for fetching USCCB pages
- `python-dotenv` (EXISTING): Environment variable management
- `pytest`, `pytest-cov` (EXISTING): Testing framework

**Storage**: 
- File system: HTML files in `readings/` directory
- Markdown files in `_posts/` directory (existing)
- Index page at root: `index.md`

**Testing**: 
- pytest with 90% coverage requirement
- Unit tests for scraper functions
- Integration tests against live USCCB site (with rate limiting)
- E2E tests for complete CLI workflows

**Target Platform**: 
- Local: macOS/Linux/Windows with Python 3.11+
- CI/CD: GitHub Actions Ubuntu runner
- Deployment: GitHub Pages with Jekyll (static HTML)

**Project Type**: Single project (CLI + library)  

**Performance Goals**: 
- Scraper fetch + parse: < 30 seconds per date
- HTML generation: < 5 seconds per page
- Index generation: < 3 seconds with hundreds of files
- Full GitHub Action workflow: < 3 minutes (fetch + generate + deploy)

**Constraints**: 
- Must respect USCCB's robots.txt and be a polite scraper
- No custom Jekyll plugins (GitHub Pages limitations)
- Static HTML only (no server-side processing)
- Must handle USCCB HTML structure changes gracefully
- Rate limiting: No more than 1 request per second to USCCB
- Generated HTML must be accessible and valid HTML5
- No external databases or services (except USCCB scraping)

**Scale/Scope**: 
- Small scale: ~365 readings per year
- HTML files: ~10-30 KB each, ~11 MB/year
- Single user/developer workflow initially
- Minimal dependencies for maintainability

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**✅ Principle 1: Liturgical Authenticity**
- Status: CRITICAL - readings are official liturgical content
- Source: USCCB.org (United States Conference of Catholic Bishops) - authoritative source
- Commitment: Fetch readings verbatim from USCCB without modification
- Attribution: Include source URL in HTML pages
- Verification: Integration tests verify content matches USCCB site
- Note: This is a significant liturgical content addition, must be accurate

**✅ Principle 2: Simplicity and Minimalism**
- Simple file-based storage (HTML files in `readings/` directory)
- Minimal new dependencies (beautifulsoup4, lxml only)
- Reuse existing CLI structure and patterns from spec 001
- Thin-slice approach with P1-P5 priorities
- No premature abstractions or over-engineering
- Start with basic HTML formatting (enhance later if needed)

**✅ Principle 3: Correctness Over Performance**
- Clear, readable scraping code with extensive error handling
- Validate all extracted data before generating HTML
- Retry logic with exponential backoff for reliability
- Comprehensive test coverage (unit + integration + E2E)
- Performance goals are reasonable, no premature optimization needed

**✅ Principle 4: Testing Discipline**
- 90% unit test coverage enforced via pytest-cov
- Unit tests for all scraper functions in isolation
- Integration tests against live USCCB site (carefully rate-limited)
- E2E tests for complete CLI workflows
- Mock USCCB responses for fast unit tests
- Real USCCB tests for integration validation

**✅ Principle 5: CLI-First Development**
- New command: `catholic-liturgy generate-readings`
- Existing commands updated: `generate-index` scans readings
- Clear error messages with helpful guidance
- Support for both interactive use and automation
- Optional date parameter for flexibility

**✅ Principle 6: Semantic Versioning**
- This is a MINOR version bump (0.1.0 → 0.2.0)
- New feature, backward compatible with existing functionality
- Existing commands and workflows continue to work unchanged
- Version will be updated in pyproject.toml and __init__.py

**✅ Principle 7: Python 3.11 Standard**
- Using Python 3.11 exclusively
- Type hints throughout (PEP 484)
- Dataclasses for entity definitions (PEP 557)
- No alternative languages needed

**✅ Principle 8: Scope Constraints for Early Development**
- English-only content (USCCB default)
- Basic HTML formatting (no fancy CSS frameworks)
- No accessibility enhancements at this stage (future improvement)
- No performance optimizations (current goals easily achievable)
- No search or advanced features
- Focused on core scraping + generation functionality

**GATE STATUS: ✅ PASSED** - All constitutional principles satisfied

**Special Note on Principle 1**: This feature adds official liturgical content for the first time. We must ensure accuracy and proper attribution. The USCCB is the authoritative source for U.S. Catholic liturgical readings, making this appropriate.

---

## Project Structure

### New Files (this feature)

```text
src/catholic_liturgy_tools/
├── scraper/                    # NEW: Scraping module
│   ├── __init__.py
│   ├── usccb.py               # USCCB readings scraper
│   └── models.py              # Data models (DailyReading, ReadingEntry)
│
├── generator/
│   ├── readings.py            # NEW: HTML generation for readings
│   └── index.py               # MODIFIED: Update to scan readings/
│
├── utils/
│   └── html_utils.py          # NEW: HTML utilities (sanitization, formatting)
│
└── cli.py                     # MODIFIED: Add generate-readings command

tests/
├── unit/
│   ├── test_usccb_scraper.py  # NEW: Scraper unit tests (mocked)
│   ├── test_readings_models.py # NEW: Data model validation tests
│   ├── test_readings_generator.py # NEW: HTML generation tests
│   └── test_html_utils.py     # NEW: HTML utility tests
│
├── integration/
│   ├── test_usccb_integration.py # NEW: Live USCCB scraping tests
│   └── test_readings_workflow.py # NEW: End-to-end readings workflow
│
└── e2e/
    └── test_cli_readings.py   # NEW: CLI command E2E tests

readings/                       # NEW: Output directory for HTML files
└── .gitkeep

specs/002-daily-readings/       # NEW: This specification
├── spec.md
├── data-model.md
├── plan.md                     # This file
├── research.md
├── tasks.md
└── contracts/
    └── cli-commands.md

.github/workflows/
└── publish-content.yml         # RENAMED: from publish-daily-message.yml
```

### Modified Files

1. `src/catholic_liturgy_tools/cli.py`: Add `generate-readings` command
2. `src/catholic_liturgy_tools/generator/index.py`: Scan `readings/` directory
3. `.github/workflows/publish-content.yml`: Renamed, add readings generation step
4. `pyproject.toml`: Add beautifulsoup4 and lxml dependencies, bump version to 0.2.0
5. `src/catholic_liturgy_tools/__init__.py`: Update version to 0.2.0
6. `README.md`: Document new commands and features
7. `index.md`: Regenerated with new structure (messages + readings sections)

---

## Phased Implementation

### Phase 0: Research & Technical Decisions (1-2 days)

**Goal**: Make informed decisions about scraping approach, HTML generation, error handling, and testing strategy.

**Tasks**:
1. Study USCCB HTML structure for regular weekdays, Sundays, and major feasts
2. Research BeautifulSoup best practices for robust parsing
3. Design HTML template for readings pages (structure, CSS, accessibility)
4. Review try1 repo scraper code for inspiration and lessons learned
5. Design retry/backoff strategy for reliability
6. Create HTML snapshots for test fixtures
7. Document decisions in `research.md`

**Deliverables**:
- `specs/002-daily-readings/research.md` with technical decisions
- HTML structure documentation with example USCCB pages analyzed
- Test strategy document (unit vs integration balance)
- Error handling strategy documented

---

### Phase 1: Design & Contracts (1-2 days)

**Goal**: Define all interfaces, data structures, and contracts before writing implementation code.

**Tasks**:
1. Define `DailyReading` and `ReadingEntry` data models (already in data-model.md)
2. Create `ScraperConfig` configuration class
3. Define CLI command interface for `generate-readings`
4. Document HTML output format and structure
5. Define exception hierarchy (NetworkError, ParseError, ValidationError, etc.)
6. Create test data fixtures and mock responses
7. Document all function signatures with type hints

**Deliverables**:
- `specs/002-daily-readings/contracts/cli-commands.md`
- `specs/002-daily-readings/contracts/data-models.md` (or reference data-model.md)
- `specs/002-daily-readings/contracts/html-format.md`
- Python stub files with type hints and docstrings (no implementation)

---

### Phase 2: Core Implementation - Priority 1 (Scraper) (3-4 days)

**Goal**: Implement reliable USCCB scraper with comprehensive error handling and testing.

**Priority**: P1 (Foundation - everything else depends on this)

**Tasks**:
1. Create `src/catholic_liturgy_tools/scraper/` module
2. Implement `USCCBReadingsScraper` class:
   - `get_readings_for_date(date) -> DailyReading`
   - `_build_url(date) -> str`
   - `_fetch_page(url) -> BeautifulSoup`
   - `_extract_liturgical_day(soup) -> str`
   - `_extract_readings(soup) -> List[ReadingEntry]`
   - `_check_for_multiple_masses(soup) -> Optional[str]`
3. Implement retry logic with exponential backoff
4. Implement data models: `DailyReading`, `ReadingEntry`
5. Write unit tests with mocked HTML responses (90% coverage target)
6. Write integration tests against live USCCB site (3-5 sample dates)
7. Add comprehensive error handling and logging

**Acceptance Criteria**:
- ✅ Scraper successfully fetches weekday, Sunday, and feast day readings
- ✅ Unit tests achieve 90%+ coverage
- ✅ Integration tests pass against live USCCB site
- ✅ Handles multiple Mass options (Christmas, Easter Vigil, etc.)
- ✅ Retry logic works with exponential backoff
- ✅ Clear error messages for all failure modes
- ✅ All extracted data passes validation

**Files**:
- `src/catholic_liturgy_tools/scraper/__init__.py`
- `src/catholic_liturgy_tools/scraper/usccb.py`
- `src/catholic_liturgy_tools/scraper/models.py`
- `tests/unit/test_usccb_scraper.py`
- `tests/unit/test_readings_models.py`
- `tests/integration/test_usccb_integration.py`
- `tests/fixtures/usccb_sample_pages/` (HTML snapshots)

---

### Phase 3: Core Implementation - Priority 2 (HTML Generation) (2-3 days)

**Goal**: Generate well-formatted HTML pages from scraped readings data.

**Priority**: P2 (Builds on P1)

**Tasks**:
1. Create `src/catholic_liturgy_tools/generator/readings.py`
2. Implement HTML generation functions:
   - `generate_readings_html(reading: DailyReading) -> str`
   - `generate_readings_page(reading: DailyReading, output_dir: str) -> Path`
3. Create HTML template with:
   - Semantic HTML5 structure
   - Basic CSS styling (embedded or external stylesheet)
   - Navigation link back to index
   - Responsive meta tags
4. Implement HTML utilities:
   - `sanitize_text(text: str) -> str`
   - `format_paragraph(text: str) -> str`
5. Write unit tests for HTML generation (90% coverage)
6. Validate generated HTML (HTML5 validator)
7. Test cross-browser rendering (Chrome, Firefox, Safari)

**Acceptance Criteria**:
- ✅ HTML pages generated with proper structure (doctype, head, body)
- ✅ All readings displayed with titles, citations, and text
- ✅ Liturgical day name prominently displayed
- ✅ Navigation link to index page works
- ✅ HTML validates as HTML5
- ✅ Renders correctly in modern browsers
- ✅ Unit tests achieve 90%+ coverage
- ✅ Files saved to `readings/{date}.html`

**Files**:
- `src/catholic_liturgy_tools/generator/readings.py`
- `src/catholic_liturgy_tools/utils/html_utils.py`
- `tests/unit/test_readings_generator.py`
- `tests/unit/test_html_utils.py`
- `readings/.gitkeep` (directory created)

---

### Phase 4: Core Implementation - Priority 3 (Index Updates) (1-2 days)

**Goal**: Update index page generator to include readings alongside messages.

**Priority**: P3 (Builds on P1 and P2)

**Tasks**:
1. Modify `src/catholic_liturgy_tools/generator/index.py`:
   - Add `scan_readings_files(readings_dir: str) -> List[ReadingsEntry]`
   - Update `generate_index()` to scan both `_posts/` and `readings/`
   - Generate two-section markdown (messages + readings)
2. Parse HTML files to extract liturgical day name for display
3. Sort both lists by date (newest first)
4. Handle edge cases (empty directories, one section only)
5. Ensure `index.md` is generated (not `index.html`)
6. Update tests for index generation
7. Test that GitHub Pages renders index at root URL

**Acceptance Criteria**:
- ✅ Index page includes "Daily Messages" section
- ✅ Index page includes "Daily Readings" section
- ✅ Both sections sorted newest first
- ✅ Links point to correct files
- ✅ Works when only messages exist (no readings yet)
- ✅ Works when both messages and readings exist
- ✅ Generated as `index.md` (not `index.html`)
- ✅ Unit tests updated and passing

**Files Modified**:
- `src/catholic_liturgy_tools/generator/index.py`
- `tests/unit/test_index.py`
- `tests/integration/test_index_workflow.py`

---

### Phase 5: CLI Integration - Priority 4 (1-2 days)

**Goal**: Provide CLI command for generating readings pages.

**Priority**: P4 (User interface for P1-P3 functionality)

**Tasks**:
1. Modify `src/catholic_liturgy_tools/cli.py`:
   - Add `generate_readings_command(args)` function
   - Add command parser with optional `--date` parameter
   - Add help text and examples
2. Integrate scraper + HTML generation in single command
3. Add progress indicators and status messages
4. Implement error handling with user-friendly messages
5. Update main parser to include new command
6. Write E2E tests for CLI command
7. Update README with command documentation

**Acceptance Criteria**:
- ✅ `catholic-liturgy generate-readings` command works
- ✅ Optional `--date YYYY-MM-DD` parameter works
- ✅ Defaults to today's date when no date specified
- ✅ Displays liturgical day name and file path on success
- ✅ Clear error messages for network, parsing, validation failures
- ✅ E2E tests pass for all scenarios
- ✅ Help text is clear and informative

**Files**:
- `src/catholic_liturgy_tools/cli.py` (modified)
- `tests/e2e/test_cli_readings.py` (new)
- `README.md` (modified)

---

### Phase 6: GitHub Actions Automation - Priority 5 (1-2 days)

**Goal**: Automate readings generation and publishing in GitHub Actions workflow.

**Priority**: P5 (Full automation, depends on P1-P4)

**Tasks**:
1. Rename `.github/workflows/publish-daily-message.yml` to `publish-content.yml`
2. Update workflow to:
   - Generate daily message (existing)
   - Generate daily readings (new)
   - Generate index with both sections
   - Commit and push all changes
   - Deploy to GitHub Pages
3. Update workflow name and description
4. Test manual trigger via GitHub UI
5. Test scheduled trigger (wait for next scheduled run or adjust cron temporarily)
6. Update README with new workflow name and behavior
7. Update trigger-publish CLI command to use new workflow name

**Acceptance Criteria**:
- ✅ Workflow renamed to `publish-content.yml`
- ✅ Workflow generates both messages and readings
- ✅ Workflow updates index with both sections
- ✅ Workflow commits and pushes successfully
- ✅ Workflow deploys to GitHub Pages
- ✅ Manual trigger works via GitHub UI
- ✅ CLI `trigger-publish` command works with new name
- ✅ Scheduled trigger works (daily execution)
- ✅ Live site displays both messages and readings

**Files**:
- `.github/workflows/publish-content.yml` (renamed and modified)
- `src/catholic_liturgy_tools/github/actions.py` (modify if needed for new workflow name)
- `tests/e2e/test_cli_trigger.py` (update for new workflow name)
- `README.md` (modified)

---

## Testing Strategy

### Unit Tests (90% coverage required)

**Scraper Tests** (`tests/unit/test_usccb_scraper.py`):
- Test URL building for various dates
- Test parsing with mocked HTML responses (weekday, Sunday, feast day)
- Test multiple Mass detection logic
- Test liturgical day extraction
- Test readings extraction with various structures
- Test error handling (network errors, parse errors)
- Test retry logic with mocked failures
- Test validation of extracted data

**Data Model Tests** (`tests/unit/test_readings_models.py`):
- Test `DailyReading.validate()` with valid/invalid data
- Test `ReadingEntry.validate()` with valid/invalid data
- Test derived attributes (filename, file_path, title_with_citation)
- Test edge cases (empty strings, whitespace, special characters)

**HTML Generation Tests** (`tests/unit/test_readings_generator.py`):
- Test HTML generation with various reading counts (3-4 readings)
- Test paragraph formatting
- Test special character handling
- Test output file path generation
- Test file writing (with temp directories)
- Test HTML structure (presence of key elements)

**HTML Utilities Tests** (`tests/unit/test_html_utils.py`):
- Test text sanitization
- Test paragraph formatting
- Test HTML escaping

**Index Generation Tests** (`tests/unit/test_index.py` - modified):
- Test scanning readings directory
- Test parsing HTML files for liturgical day names
- Test generating two-section markdown
- Test sorting (newest first)
- Test edge cases (empty dirs, only messages, only readings)
- Test filename is `index.md`

---

### Integration Tests

**USCCB Integration Tests** (`tests/integration/test_usccb_integration.py`):
- Test fetching real pages from USCCB.org (with rate limiting!)
- Test 3-5 sample dates:
  - Regular weekday
  - Sunday with 4 readings
  - Major feast day (e.g., Christmas Day)
- Verify structure of returned data
- Mark as slow tests (`@pytest.mark.slow`)
- Skip if `--skip-integration` flag used

**Readings Workflow Tests** (`tests/integration/test_readings_workflow.py`):
- Test complete workflow: fetch -> validate -> generate HTML
- Test with various dates
- Test file system operations (temp directories)
- Verify generated HTML can be parsed and validated

**Index Workflow Tests** (`tests/integration/test_index_workflow.py` - modified):
- Test generating index with both messages and readings
- Test with real file system (temp directories)
- Verify markdown structure and links

---

### End-to-End Tests

**CLI Readings Tests** (`tests/e2e/test_cli_readings.py`):
- Test `generate-readings` command without date (today)
- Test `generate-readings --date YYYY-MM-DD`
- Test error handling (invalid date, network failure)
- Test output messages and file paths
- Test idempotency (running twice)

**CLI Index Tests** (`tests/e2e/test_cli_index.py` - modified):
- Test `generate-index` with readings present
- Test `generate-index` with messages and readings

**CLI Trigger Tests** (`tests/e2e/test_cli_trigger.py` - modified):
- Update for new workflow name `publish-content.yml`

---

## Dependencies

### New Dependencies (add to pyproject.toml)

```toml
dependencies = [
    "requests>=2.31.0",            # EXISTING
    "python-dotenv>=1.0.0",        # EXISTING
    "beautifulsoup4>=4.12.0",      # NEW: HTML parsing
    "lxml>=5.0.0",                 # NEW: Fast parser for BeautifulSoup
]
```

### Justification for New Dependencies

**beautifulsoup4**: Industry-standard HTML parsing library, well-maintained, excellent documentation, handles malformed HTML gracefully. Alternatives considered: lxml alone (less convenient API), html.parser (stdlib, but less robust). BeautifulSoup is the right choice for this use case.

**lxml**: Fast C-based XML/HTML parser. BeautifulSoup can use different backends; lxml is fastest and most robust. Alternative: html.parser (stdlib, slower). We choose lxml for reliability and speed.

---

## Risk Assessment & Mitigation

### Risk 1: USCCB HTML Structure Changes
**Probability**: Medium (sites change over time)  
**Impact**: High (scraper breaks)  
**Mitigation**:
- Extensive unit tests with HTML snapshots
- Integration tests that fail when structure changes
- Detailed documentation of HTML structure in research.md
- Graceful error handling with clear messages
- Consider HTML structure versioning/detection

### Risk 2: Rate Limiting or Blocking by USCCB
**Probability**: Low (polite scraping)  
**Impact**: Medium (fetch failures)  
**Mitigation**:
- Use descriptive User-Agent header
- Implement rate limiting (no more than 1 req/sec)
- Exponential backoff on errors
- Document respectful usage policy
- Consider caching to minimize requests

### Risk 3: Network Reliability
**Probability**: Medium (internet issues happen)  
**Impact**: Medium (workflow failures)  
**Mitigation**:
- Retry logic with exponential backoff (3 attempts)
- Clear error messages for debugging
- Timeout configuration (30 seconds)
- Workflow continues even if readings fetch fails (optional)

### Risk 4: Invalid or Missing Readings Data
**Probability**: Low (USCCB data is reliable)  
**Impact**: Medium (empty pages)  
**Mitigation**:
- Comprehensive data validation
- Clear error messages when readings missing
- Integration tests verify data completeness
- Handle edge cases (future dates, special days)

### Risk 5: HTML Generation Bugs
**Probability**: Low (simple generation logic)  
**Impact**: Medium (broken pages)  
**Mitigation**:
- Unit tests with 90%+ coverage
- HTML validation in tests
- Cross-browser testing
- Visual inspection of generated pages

---

## Performance Benchmarks

**Target Performance** (measured on MacBook Pro M1, or GitHub Actions runner):

| Operation | Target | Acceptable | Notes |
|-----------|--------|------------|-------|
| Fetch USCCB page | < 3s | < 10s | Network dependent |
| Parse HTML | < 1s | < 3s | BeautifulSoup performance |
| Generate HTML | < 1s | < 5s | Template rendering |
| Write file | < 0.5s | < 2s | File I/O |
| Scan directory (100 files) | < 0.5s | < 2s | Index generation |
| Full workflow (single day) | < 5s | < 15s | End-to-end |
| GitHub Action (complete) | < 2min | < 5min | Including deploy |

**Measurement**: Add timing logs to key functions, include in test output.

---

## Documentation Requirements

**User Documentation** (README.md updates):
- New `generate-readings` command with examples
- Updated `generate-index` behavior
- Updated workflow description
- Troubleshooting section for scraping issues

**Developer Documentation** (research.md):
- USCCB HTML structure analysis
- BeautifulSoup usage patterns
- Error handling strategy
- Test strategy details
- HTML template structure

**API Documentation** (docstrings):
- All public functions with type hints
- All classes with class docstrings
- All modules with module docstrings
- Example usage in docstrings

**Contract Documentation** (contracts/):
- CLI command interfaces
- Data model contracts
- HTML format specification

---

## Deployment Plan

### Pre-Deployment Checklist
- [ ] All tests pass (unit + integration + E2E)
- [ ] Coverage at 90%+ for new code
- [ ] Manual testing of CLI commands
- [ ] Manual testing of GitHub Actions workflow (dev branch)
- [ ] HTML validation of generated pages
- [ ] Cross-browser testing (Chrome, Firefox, Safari)
- [ ] Documentation complete and accurate
- [ ] README updated with new features
- [ ] CHANGELOG.md updated (if exists)
- [ ] Version bumped to 0.2.0 in pyproject.toml and __init__.py

### Deployment Steps
1. **Create Feature Branch**: `git checkout -b 002-daily-readings`
2. **Develop in Phases**: Follow P1-P5 with testing at each phase
3. **Merge to Main**: After all tests pass and documentation complete
4. **Tag Release**: `git tag v0.2.0` and push tag
5. **Trigger Workflow**: Manually trigger `publish-content.yml` to test
6. **Monitor First Run**: Check GitHub Actions logs and live site
7. **Verify Live Site**: Ensure index and readings pages render correctly
8. **Schedule Next Run**: Confirm daily scheduled trigger works

### Rollback Plan
If critical issues discovered after deployment:
1. Revert to previous commit on main branch
2. Redeploy previous version to GitHub Pages
3. Fix issues in feature branch
4. Re-test and redeploy

---

## Success Metrics

This implementation is successful when:

1. ✅ **Functionality**: All P1-P5 features working as specified
2. ✅ **Quality**: 90%+ test coverage on all new code
3. ✅ **Reliability**: Scraper handles USCCB structure and errors gracefully
4. ✅ **Usability**: CLI commands are intuitive with clear error messages
5. ✅ **Automation**: GitHub Actions workflow runs daily without issues
6. ✅ **Documentation**: README and research.md are comprehensive
7. ✅ **Performance**: All operations meet performance targets
8. ✅ **Compatibility**: Works on macOS, Linux, Windows locally
9. ✅ **Validation**: HTML pages are valid HTML5 and render correctly
10. ✅ **Maintainability**: Code is clean, well-commented, and follows project conventions

---

## Post-Implementation Review

After completing implementation, conduct review to assess:
- What worked well in the implementation process?
- What challenges were encountered and how were they resolved?
- Are there any technical debt items to address?
- Are there any immediate improvements or enhancements to consider?
- Update this document with lessons learned for future features

---

## Timeline Estimate

**Total Estimated Time**: 10-15 days (2-3 weeks)

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 0: Research | 1-2 days | None |
| Phase 1: Design & Contracts | 1-2 days | Phase 0 |
| Phase 2: Scraper (P1) | 3-4 days | Phase 1 |
| Phase 3: HTML Gen (P2) | 2-3 days | Phase 2 |
| Phase 4: Index (P3) | 1-2 days | Phase 2, 3 |
| Phase 5: CLI (P4) | 1-2 days | Phase 2, 3, 4 |
| Phase 6: Actions (P5) | 1-2 days | Phase 2, 3, 4, 5 |
| Testing & Documentation | Ongoing | All phases |
| Buffer for Issues | 2-3 days | N/A |

**Note**: This is a one-person project estimate. With multiple contributors, phases 2-5 could be parallelized after phase 1 completes, reducing total calendar time to ~1-2 weeks.

---

## Next Steps

1. **Complete Research Phase**: Create `research.md` with HTML structure analysis
2. **Create Contracts**: Document CLI commands and data formats in `contracts/`
3. **Begin Phase 2**: Start scraper implementation with TDD approach
4. **Iterate**: Complete each phase with full testing before moving to next
5. **Review**: Conduct review after each phase to catch issues early
6. **Deploy**: Follow deployment checklist when all phases complete

---

**Document Status**: Draft - to be reviewed and refined during Phase 0 research
