# Feature Specification: GitHub Pages Daily Message

**Feature Branch**: `001-github-pages`  
**Created**: 2025-11-22  
**Status**: Draft  
**Input**: User description: "publish a hello world message using a github action to github site page (using Jekyll) - initially this message will just be the date in YYYY-MM-DD and 'Hello Catholic World' - each day's message should be on it's own page which is linked from the index page - the published message should be in markdown format - provide a CLI to kickoff the runs, both via github actions (i.e. fully end-to-end) and directly via invoking the python scripts."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate Daily Message Locally (Priority: P1)

A developer runs the CLI locally to generate a daily message markdown file containing today's date and "Hello Catholic World". This provides immediate value and can be tested without any GitHub infrastructure.

**Why this priority**: This is the core functionality and can be developed, tested, and demonstrated completely independently. It delivers immediate value as a standalone tool.

**Independent Test**: Can be fully tested by running the CLI command locally, inspecting the generated markdown file content, and verifying it contains the correct date format and message. Requires no external dependencies.

**Acceptance Scenarios**:

1. **Given** the CLI is installed, **When** user runs `catholic-liturgy generate-message`, **Then** a markdown file is created with today's date in YYYY-MM-DD format and the text "Hello Catholic World"
2. **Given** a message already exists for today, **When** user runs `catholic-liturgy generate-message`, **Then** the existing file is updated/overwritten with current timestamp
3. **Given** the CLI is run on 2025-11-22, **When** the file is generated, **Then** the filename includes `2025-11-22` and the content displays the same date

---

### User Story 2 - Generate Index Page with Links (Priority: P2)

The system automatically generates an index page that lists all daily message pages with clickable links, making it easy to browse historical messages.

**Why this priority**: This adds navigation capability and builds upon P1. It can be tested independently by generating multiple messages and verifying the index page correctly links to them.

**Independent Test**: Generate 3-5 daily messages, run the index generation, verify the index.md contains links to all messages in reverse chronological order (newest first).

**Acceptance Scenarios**:

1. **Given** multiple daily message files exist, **When** index generation runs, **Then** an index.md file is created listing all messages with links
2. **Given** messages from different dates exist, **When** index is generated, **Then** messages are sorted in reverse chronological order (newest first)
3. **Given** the index page exists, **When** a new daily message is added, **Then** running index generation updates the index to include the new message

---

### User Story 3 - Deploy to GitHub Pages via GitHub Actions (Priority: P3)

A GitHub Action automatically runs on schedule (or manual trigger) to generate the daily message, update the index, commit changes, and deploy to GitHub Pages using Jekyll.

**Why this priority**: This automates the entire workflow but depends on P1 and P2 being complete. It requires GitHub infrastructure to test end-to-end.

**Independent Test**: Manually trigger the GitHub Action, verify it runs successfully, check the gh-pages branch for new commits, and verify the live site shows the new content.

**Acceptance Scenarios**:

1. **Given** the GitHub Action workflow is configured, **When** manually triggered, **Then** a new daily message is generated, committed, and published to GitHub Pages
2. **Given** the workflow runs successfully, **When** visiting the GitHub Pages site, **Then** the index page displays with links to all daily messages
3. **Given** the action is scheduled to run daily, **When** a new day begins, **Then** the action automatically generates and publishes the new day's message

---

### User Story 4 - Manual GitHub Action Trigger via CLI (Priority: P4)

A developer can trigger the GitHub Action remotely from their local machine using the CLI, providing a convenient way to force a publish without opening the GitHub web interface.

**Why this priority**: This is a convenience feature that enhances the workflow but isn't essential for core functionality.

**Independent Test**: Run the CLI command to trigger the action, verify the GitHub Action starts running, and check that the site updates after completion.

**Acceptance Scenarios**:

1. **Given** the user has GitHub credentials configured, **When** they run `catholic-liturgy trigger-publish`, **Then** the GitHub Action starts execution
2. **Given** the action trigger completes, **When** checking GitHub Actions tab, **Then** a new workflow run appears with status information
3. **Given** authentication fails, **When** trigger command runs, **Then** user receives clear error message about missing/invalid credentials

---

### Edge Cases

- What happens when the script runs multiple times in the same day?
  - Should overwrite/update the existing day's message file
  - Index should not contain duplicate entries for the same date
- How does the system handle missing or corrupted message files when generating the index?
  - Skip corrupted files with a warning
  - Generate index with valid files only
- What if GitHub Pages deployment fails?
  - GitHub Action should fail gracefully with clear error message
  - Local message generation should still work
- What if the CLI is run without proper GitHub credentials for triggering actions?
  - Provide clear error message indicating authentication is required
  - Direct user to GitHub token documentation

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST generate markdown files containing a date in YYYY-MM-DD format and the text "Hello Catholic World"
- **FR-002**: System MUST create separate markdown files for each day, with the date included in the filename (e.g., `2025-11-22-daily-message.md`)
- **FR-003**: System MUST generate an index page (index.md) that links to all daily message pages
- **FR-004**: System MUST sort messages in the index in reverse chronological order (newest first)
- **FR-005**: System MUST provide a CLI command to generate a daily message locally
- **FR-006**: System MUST provide a CLI command to generate/update the index page
- **FR-007**: System MUST provide a GitHub Actions workflow that automatically generates and publishes messages
- **FR-008**: CLI MUST provide a command to manually trigger the GitHub Action workflow
- **FR-009**: Generated markdown files MUST be compatible with Jekyll for GitHub Pages
- **FR-010**: System MUST handle running multiple times in the same day without creating duplicate entries
- **FR-011**: All generated content MUST use UTF-8 encoding
- **FR-012**: System MUST provide clear error messages when operations fail
- **FR-013**: GitHub Action MUST commit generated files to the repository
- **FR-014**: GitHub Action MUST deploy to GitHub Pages after generating content
- **FR-015**: CLI MUST support both local execution and GitHub Action triggering modes

### Key Entities

- **Daily Message**: A markdown document containing a date (YYYY-MM-DD format) and the greeting "Hello Catholic World". Each message is stored as a separate file named with its date.
- **Index Page**: A markdown document that serves as the homepage, containing a chronologically ordered list of links to all daily message pages.
- **GitHub Action Workflow**: An automated workflow configuration that generates messages, updates the index, commits changes, and triggers GitHub Pages deployment.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A developer can generate a daily message locally in under 5 seconds by running a single CLI command
- **SC-002**: The generated markdown file contains correctly formatted content (YYYY-MM-DD date + "Hello Catholic World") 100% of the time
- **SC-003**: The index page correctly links to all existing daily messages with no broken links or duplicates
- **SC-004**: The GitHub Action successfully generates and publishes a daily message within 2 minutes of being triggered
- **SC-005**: The published GitHub Pages site displays the index page with functioning links to all daily messages
- **SC-006**: Running the CLI multiple times in the same day does not create duplicate entries in the index
- **SC-007**: All CLI commands provide clear success/error feedback to the user
- **SC-008**: End-to-end testing confirms a developer can trigger publication from CLI and see updates on the live site within 3 minutes

## Assumptions

- GitHub repository is already set up with appropriate permissions for GitHub Actions
- GitHub Pages is enabled for the repository
- User has Python 3.11 installed for local CLI usage
- User has Git installed and repository cloned locally
- Package is installed locally via `pip install -e .` from repository (not published to PyPI)
- For GitHub Action triggering, user has a GitHub personal access token with appropriate permissions
- Jekyll is the assumed static site generator for GitHub Pages (default for GitHub)
- Message content is intentionally simple (date + greeting) per requirements; extensibility for richer content is out of scope for this feature
- All dates use the system's local timezone (no timezone conversion needed at this stage)

## Out of Scope

- Custom styling or theming for the GitHub Pages site (using Jekyll defaults)
- Multilingual support (English only per constitution)
- Historical data import or backfilling of past dates
- Message editing or deletion through the CLI
- Authentication UI (tokens must be configured manually)
- Analytics or visitor tracking on the published site
- RSS feed or subscription features
- Mobile-specific optimizations
- Accessibility features (per constitution scope constraints)

## Technical Constraints

- Must use Python 3.11 as specified in project constitution
- Must maintain 90% test coverage including E2E tests for all CLI commands
- Must follow semantic versioning
- Generated content must derive from code (the greeting is fixed, not from external sources)
- Must work with GitHub's Jekyll integration for Pages (no custom Jekyll server required)

## Dependencies

- GitHub Actions environment (for automated publishing)
- GitHub Pages service
- GitHub API (for remote workflow triggering via CLI)
- Jekyll (provided by GitHub Pages, no separate installation needed)
- Python packages: argparse (stdlib), requests (for GitHub API), pytest and pytest-cov (for testing)

## Constitution Compliance

This feature adheres to the project constitution:
- ✅ Python 3.11 as primary language
- ✅ Includes CLI for manual verification and experimentation
- ✅ Will include E2E tests for all CLI options
- ✅ Uses thin slices of functionality (P1-P4 priorities allow incremental development)
- ✅ Keeps implementation minimal and simple
- ✅ English-only content
- ✅ No performance optimizations needed at this stage
- ✅ Fixed greeting content (not liturgical content requiring authoritative sources)
