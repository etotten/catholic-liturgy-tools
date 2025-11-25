# Feature Specification: Daily Readings from Catholic Lectionary

**Feature Branch**: `002-daily-readings`  
**Created**: 2025-11-22  
**Status**: Draft  
**Input**: User description: "add a new feature to publish the 'Daily Readings' from the Catholic Lectionary - this 'Daily Readings' feature will create a separate page for each day in a basic html format which is linked from the index page; these pages are also separate from the daily message - The readings are fetched from the USCCB.org readings site; there are existing python files found in this dir 'https://github.com/etotten/catholic-liturgy-tools--try1/tree/001-liturgy-content-generator/src/scrapers' which can be used as the inspiration for this fetching, but the resulting .py files in this repo should have tests and be refactored if necessary - the existing github action should be renamed to reflect that it will publish multiple things to the site; it will likely be used for even more features later, so we can keep the name generic - the index page has been changed; it should be generated such that the '/index.html' is not required on the end of the url for the page to render (e.g. https://etotten.github.io/catholic-liturgy-tools/ should render the index page)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Fetch Daily Readings from USCCB (Priority: P1)

A developer runs the CLI locally to fetch readings from USCCB.org for a specific date. The scraper retrieves the liturgical day name, all Scripture readings (First Reading, Responsorial Psalm, Second Reading if present, Gospel), and handles special cases like multiple Mass options for major feast days.

**Why this priority**: This is the foundational functionality. It must work reliably before any generation or publishing features can be built. The scraper can be developed and tested completely independently with unit tests and integration tests against the live USCCB site.

**Independent Test**: Run the scraper for various dates (regular weekdays, Sundays, major feast days like Christmas with multiple Masses), verify the returned data structure contains all expected readings with proper titles, citations, and text content.

**Acceptance Scenarios**:

1. **Given** a regular weekday date (e.g., 2025-11-22), **When** the scraper fetches readings, **Then** it returns First Reading, Responsorial Psalm, Gospel with liturgical day name
2. **Given** a Sunday date with Second Reading, **When** the scraper fetches readings, **Then** it returns all four readings (First, Psalm, Second, Gospel)
3. **Given** a major feast day with multiple Masses (e.g., Christmas Day, Vigil, Dawn), **When** the scraper fetches readings, **Then** it detects multiple options and fetches the primary/most solemn Mass readings
4. **Given** the USCCB site is unreachable, **When** the scraper runs, **Then** it retries with exponential backoff and raises a clear error after max attempts
5. **Given** an invalid date, **When** the scraper is called, **Then** it raises a validation error with clear message

---

### User Story 2 - Generate HTML Daily Readings Page (Priority: P2)

The system generates a standalone HTML page for a specific date's readings, formatted with proper structure (headings, paragraphs) and linked from the index page. This page is separate from the daily message markdown file.

**Why this priority**: Builds on P1 scraper functionality. Can be tested independently by verifying the HTML output structure, content accuracy, and proper formatting without requiring GitHub Pages deployment.

**Independent Test**: Generate readings HTML for multiple dates, verify file paths follow convention (e.g., `readings/2025-11-22.html`), validate HTML structure and content match scraped data, check that links work locally.

**Acceptance Scenarios**:

1. **Given** scraped readings data for a date, **When** HTML generation runs, **Then** an HTML file is created in `readings/{YYYY-MM-DD}.html` with proper structure
2. **Given** readings with multiple paragraphs in text, **When** HTML is generated, **Then** each paragraph is wrapped in `<p>` tags with proper formatting
3. **Given** readings include citations, **When** HTML is generated, **Then** citations are displayed prominently below reading titles
4. **Given** a liturgical day name exists, **When** HTML is generated, **Then** it's displayed as the page title/heading
5. **Given** an existing readings HTML file for a date, **When** generation runs again, **Then** the existing file is overwritten with updated content

---

### User Story 3 - Update Index Page with Readings Links (Priority: P3)

The index page generator is enhanced to include links to both daily messages AND daily readings pages, displayed in a clear, organized manner. The index page is generated as `index.md` so that GitHub Pages renders it at the root URL without requiring `/index.html`.

**Why this priority**: Depends on P1 and P2. Provides navigation to all content types. Can be tested independently by generating index with various combinations of messages and readings files.

**Independent Test**: Create sample message and readings files, generate index, verify it contains separate sections for messages and readings, check that links point to correct files, test that `index.md` (not `index.html`) is generated.

**Acceptance Scenarios**:

1. **Given** multiple daily messages and readings files exist, **When** index generation runs, **Then** index.md contains two sections: "Daily Messages" and "Daily Readings"
2. **Given** readings files in `readings/` directory, **When** index is generated, **Then** readings are listed in reverse chronological order with links
3. **Given** both message and readings exist for the same date, **When** index is generated, **Then** both are displayed with clear distinction
4. **Given** only messages exist (no readings), **When** index is generated, **Then** only the messages section is shown
5. **Given** the index.md file is generated, **When** deployed to GitHub Pages, **Then** the site root URL (without /index.html) renders the page correctly

---

### User Story 4 - CLI Command to Generate Readings Page (Priority: P4)

A CLI command `catholic-liturgy generate-readings` fetches readings from USCCB and generates the HTML page for today (or a specified date), providing a complete end-to-end workflow in a single command.

**Why this priority**: Convenience feature that combines P1 and P2. Essential for local testing and manual operation.

**Independent Test**: Run CLI command, verify it fetches data and creates HTML file, test with date parameter, verify error handling for network failures.

**Acceptance Scenarios**:

1. **Given** the CLI is installed, **When** user runs `catholic-liturgy generate-readings`, **Then** readings for today are fetched and HTML page is generated
2. **Given** user specifies a date, **When** running `catholic-liturgy generate-readings --date 2025-12-25`, **Then** readings for that specific date are generated
3. **Given** the command succeeds, **When** checking output, **Then** user sees confirmation with file path and liturgical day name
4. **Given** network failure occurs, **When** command runs, **Then** clear error message is displayed with troubleshooting hints
5. **Given** readings already exist for a date, **When** command runs again, **Then** existing file is updated without warning (idempotent operation)

---

### User Story 5 - Automated GitHub Action Publishing (Priority: P5)

The GitHub Action workflow (renamed to generic name like `publish-content.yml`) automatically fetches readings, generates HTML pages, updates the index, commits changes, and deploys to GitHub Pages. Runs on schedule and manual trigger.

**Why this priority**: Full automation depends on all previous priorities being complete and tested. Requires GitHub infrastructure for end-to-end testing.

**Independent Test**: Manually trigger GitHub Action, verify workflow runs successfully, check that readings HTML files are committed, verify live site shows new readings pages with proper links from index.

**Acceptance Scenarios**:

1. **Given** the GitHub Action is configured, **When** manually triggered, **Then** it fetches readings, generates HTML, updates index, and publishes to GitHub Pages
2. **Given** the workflow runs, **When** checking commits, **Then** both readings HTML files and updated index.md are committed
3. **Given** the action is scheduled daily, **When** a new day begins, **Then** the action automatically generates both daily message and readings
4. **Given** the action completes successfully, **When** visiting the live site, **Then** the index page shows links to both messages and readings
5. **Given** the workflow file is renamed, **When** existing manual triggers reference it, **Then** they continue to work with the new name

---

### Edge Cases

- **What happens when USCCB site structure changes?**
  - Scraper should fail gracefully with detailed error message
  - Consider HTML snapshot tests to detect structure changes early
  - Document the expected HTML structure in research.md for maintainability

- **How to handle missing readings for future dates?**
  - USCCB typically has readings available weeks in advance
  - If readings not available, scraper should return clear error (not empty data)
  - CLI should display helpful message indicating date may be too far in future

- **What if scraper is rate-limited or blocked by USCCB?**
  - Implement polite scraping with User-Agent header identifying the tool
  - Add exponential backoff retry logic (already present in try1 code)
  - Consider caching mechanism to avoid repeated requests for same date
  - Document rate limiting behavior and respectful usage policy

- **How to handle readings with special formatting (poetry, verse numbers)?**
  - For initial version, treat all text as prose paragraphs
  - Future enhancement: detect and preserve special formatting
  - Document limitations in README

- **What if readings file conflicts with message file naming?**
  - Use separate directories: `_posts/` for messages, `readings/` for readings HTML
  - Clear separation prevents conflicts
  - Both can coexist for same date

- **How to handle timezone differences for "today"?**
  - Use system local time for "today" when no date specified
  - Document timezone behavior in CLI help text
  - GitHub Action runs on UTC schedule, document this

- **What if HTML generation fails but scraping succeeds?**
  - Log detailed error information for debugging
  - Don't cache incomplete/failed generation
  - Allow retry without re-fetching (if data is preserved)

---

## Requirements *(mandatory)*

### Functional Requirements

**Scraping & Data Fetching:**
- **FR-001**: System MUST fetch daily Mass readings from bible.usccb.org
- **FR-002**: System MUST extract liturgical day name from USCCB page
- **FR-003**: System MUST extract all reading components: title, Scripture citation, and full text
- **FR-004**: System MUST handle regular weekdays (3 readings: First, Psalm, Gospel)
- **FR-005**: System MUST handle Sundays and feast days (4 readings: First, Psalm, Second, Gospel)
- **FR-006**: System MUST detect and handle multiple Mass options (Vigil, Day, Night, Dawn) for major feasts
- **FR-007**: System MUST select the primary/most solemn Mass when multiple options exist
- **FR-008**: System MUST retry failed requests with exponential backoff (max 3 attempts)
- **FR-009**: System MUST raise clear errors when readings cannot be fetched or parsed

**HTML Generation:**
- **FR-010**: System MUST generate standalone HTML files for daily readings
- **FR-011**: HTML files MUST be stored in `readings/{YYYY-MM-DD}.html` format
- **FR-012**: HTML pages MUST include liturgical day name as main heading
- **FR-013**: HTML pages MUST display each reading with title, citation, and text
- **FR-014**: HTML pages MUST format reading text with proper paragraph tags
- **FR-015**: HTML pages MUST be valid HTML5 with proper structure (doctype, head, body)
- **FR-016**: HTML pages MUST include basic CSS styling for readability
- **FR-017**: HTML pages MUST include navigation link back to index page

**Index Page Updates:**
- **FR-018**: System MUST generate index page as `index.md` (not `index.html`)
- **FR-019**: Index page MUST include separate sections for "Daily Messages" and "Daily Readings"
- **FR-020**: Index page MUST list readings in reverse chronological order (newest first)
- **FR-021**: Index page MUST link to both message markdown files and readings HTML files
- **FR-022**: Index page MUST handle cases where only messages or only readings exist
- **FR-023**: Index page MUST scan both `_posts/` and `readings/` directories for content

**CLI Commands:**
- **FR-024**: System MUST provide `catholic-liturgy generate-readings` command
- **FR-025**: CLI MUST support optional `--date` parameter for specific dates
- **FR-026**: CLI MUST default to today's date when no date specified
- **FR-027**: CLI MUST validate date format (YYYY-MM-DD)
- **FR-028**: CLI MUST display confirmation message with liturgical day name and file path
- **FR-029**: CLI MUST provide clear error messages for network, parsing, or validation failures
- **FR-030**: Existing `generate-index` command MUST be updated to scan readings files

**GitHub Actions:**
- **FR-031**: GitHub Action workflow MUST be renamed to generic name (e.g., `publish-content.yml`)
- **FR-032**: Workflow MUST generate both daily message and daily readings
- **FR-033**: Workflow MUST update index page to include both content types
- **FR-034**: Workflow MUST commit and push all generated files
- **FR-035**: Workflow MUST trigger on schedule (daily) and manual dispatch
- **FR-036**: Workflow MUST deploy to GitHub Pages after successful generation

---

### Non-Functional Requirements

**Code Quality:**
- **NFR-001**: All scraper code MUST have unit tests with 90% coverage minimum
- **NFR-002**: Scraper MUST be refactored from try1 repo code with improved error handling
- **NFR-003**: Code MUST follow PEP 8 style guidelines
- **NFR-004**: All functions MUST have docstrings with type hints
- **NFR-005**: Complex scraping logic MUST have inline comments explaining HTML structure

**Performance:**
- **NFR-006**: Scraper MUST complete fetch and parse within 30 seconds for normal operation
- **NFR-007**: HTML generation MUST complete within 5 seconds for single date
- **NFR-008**: Full workflow (fetch + generate + update index) MUST complete within 2 minutes

**Reliability:**
- **NFR-009**: Scraper MUST implement retry logic with exponential backoff
- **NFR-010**: Scraper MUST use descriptive User-Agent header
- **NFR-011**: System MUST handle network timeouts gracefully
- **NFR-012**: System MUST provide detailed error logging for debugging

**Maintainability:**
- **NFR-013**: HTML structure expectations MUST be documented in research.md
- **NFR-014**: Scraper MUST separate URL building, fetching, and parsing into distinct functions
- **NFR-015**: HTML templates MUST be easily modifiable (consider template string or file)

**Security:**
- **NFR-016**: Scraper MUST validate and sanitize all extracted HTML content
- **NFR-017**: Generated HTML MUST escape user-generated content (though source is USCCB, not user input)
- **NFR-018**: System MUST NOT expose sensitive credentials or tokens in logs

**Compatibility:**
- **NFR-019**: Generated HTML MUST render correctly in modern browsers (Chrome, Firefox, Safari, Edge)
- **NFR-020**: System MUST work with Python 3.11+
- **NFR-021**: System MUST work on macOS, Linux, and Windows (for local CLI usage)
- **NFR-022**: Generated index.md MUST render correctly with GitHub Pages Jekyll

**Testing:**
- **NFR-023**: Unit tests MUST cover scraper functions in isolation
- **NFR-024**: Integration tests MUST verify scraper against live USCCB site (with caution/rate limiting)
- **NFR-025**: E2E tests MUST verify complete CLI workflow (fetch + generate)
- **NFR-026**: Tests MUST use pytest framework matching existing project setup

---

## Dependencies & Constraints

**New Dependencies:**
- `beautifulsoup4`: HTML parsing (required for scraping)
- `lxml`: Fast HTML parser backend for BeautifulSoup
- `requests`: HTTP client (may already be in project)

**Constraints:**
- Must respect USCCB's robots.txt and terms of service
- Scraper must include polite User-Agent identifying educational/personal use
- Cannot modify USCCB site structure (must adapt to their HTML)
- GitHub Pages free tier limitations (bandwidth, storage)
- No server-side processing (static HTML only)

---

## Success Criteria

This feature is considered complete when:

1. ✅ Scraper reliably fetches readings from USCCB.org for any date
2. ✅ Scraper has 90%+ unit test coverage and passes integration tests
3. ✅ HTML pages are generated with proper structure and styling
4. ✅ Index page includes both messages and readings in separate sections
5. ✅ CLI command works for generating readings (with and without date parameter)
6. ✅ GitHub Action workflow renamed and generates both content types
7. ✅ Live site displays readings pages accessible from index
8. ✅ All tests pass in CI/CD pipeline
9. ✅ Documentation updated (README, research.md, this spec)
10. ✅ Feature can run daily without manual intervention

---

## Future Enhancements (Out of Scope)

- Search functionality for readings by date or liturgical day
- Calendar view of available readings
- Print-friendly CSS styling
- Liturgical color indicators (green, purple, white, red)
- Saint of the day integration
- Responsive design for mobile devices
- RSS feed of daily readings
- Audio readings (text-to-speech)
- Multiple language support (Spanish, Latin)
- Advanced formatting for psalms and poetry
- User customization options (font size, colors)

These enhancements may be considered for future specifications (003, 004, etc.)
