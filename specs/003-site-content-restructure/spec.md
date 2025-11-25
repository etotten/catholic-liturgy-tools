# Feature Specification: Site Content Restructuring

**Feature Branch**: `003-site-content-restructure`  
**Created**: 2025-11-25  
**Status**: Draft  
**Input**: User description: "Separate site content from the rest of the codebase and make more user-friendly: all generated site content should go into a _site directory in order to help separate it from the code; under _site, we should use subdirectories to distinguish the generated files for different features (e.g. daily messages vs daily readings vs other future features); make it so users can go to https://etotten.github.io/catholic-liturgy-tools for the index page and not have to go to https://etotten.github.io/catholic-liturgy-tools/_site/; this may require changes to the github pages settings or the repo structure; change the index page to be index.html and generate html instead of markdown; this will allow any user to click links regardless of whether they know how to read markdown or their client can render markdown"

## Clarifications

### Session 2025-11-25

- Q: How should GitHub Pages be configured to serve the `_site/` directory as the site root? → A: Change GitHub Pages settings to publish from a branch that only contains `_site/` contents (e.g., `gh-pages` branch)
- Q: What should be the main heading/title text displayed at the top of the index page? → A: Catholic Liturgy Tools
- Q: Should the migration of existing content from old locations to `_site/` structure happen automatically during the first generation run, or should it be a separate manual step? → A: One-time development task during implementation, not built into CLI - keeps generation simple
- Q: Should old content files in their original locations be deleted after migration, or kept as a backup? → A: Delete old files after successful migration to `_site/`
- Q: Should the index page HTML include any inline CSS styling, or just semantic HTML with no styling? → A: Basic inline CSS for readability (fonts, spacing, colors)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Reorganize Generated Content into _site Directory (Priority: P1)

The system moves all generated content (daily messages, readings pages, index page) into a `_site` directory structure with feature-specific subdirectories. Generated files are organized as `_site/messages/`, `_site/readings/`, and `_site/index.html`. This provides clear separation between source code and published content.

**Why this priority**: This is the foundational restructuring that must happen first. It establishes the new directory structure that all other features depend on. Can be tested independently by verifying file paths and directory structure without requiring deployment.

**Independent Test**: Run content generation commands, verify all generated files land in `_site/` subdirectories with proper organization (`_site/messages/YYYY-MM-DD-daily-message.md`, `_site/readings/YYYY-MM-DD.html`, `_site/index.html`), check that no generated files remain in root directory.

**Acceptance Scenarios**:

1. **Given** the content generation CLI is updated, **When** generating a daily message, **Then** the file is created in `_site/messages/YYYY-MM-DD-daily-message.md`
2. **Given** the readings generation CLI is updated, **When** generating readings, **Then** the file is created in `_site/readings/YYYY-MM-DD.html`
3. **Given** the index generation CLI is updated, **When** generating the index, **Then** the file is created as `_site/index.html`
4. **Given** existing content files in old locations (root, `_posts/`, `readings/`) exist, **When** one-time migration is performed during implementation, **Then** files are moved to appropriate `_site/` subdirectories and old files are deleted
5. **Given** the `_site` directory doesn't exist, **When** generation runs, **Then** the directory structure is automatically created

---

### User Story 2 - Convert Index Page from Markdown to HTML (Priority: P2)

The index page is generated as HTML instead of Markdown, with "Catholic Liturgy Tools" as the main heading. The page includes basic inline CSS for readability (fonts, spacing, colors) and proper structure with headings, lists, and clickable links to daily messages and readings. This provides universal accessibility without requiring Markdown rendering capabilities.

**Why this priority**: Depends on P1's directory structure but can be tested independently. Makes the site accessible to all users regardless of their client's Markdown support. Critical for user experience.

**Independent Test**: Generate the index page, verify it's an `.html` file (not `.md`) with "Catholic Liturgy Tools" as heading, validate HTML structure is well-formed with inline CSS in `<head>`, check that links work when opened directly in a browser, verify basic styling improves readability.

**Acceptance Scenarios**:

1. **Given** multiple daily messages and readings exist, **When** index generation runs, **Then** `_site/index.html` is created with HTML structure (not Markdown) and displays "Catholic Liturgy Tools" as the main heading
2. **Given** the index HTML is generated, **When** opened in any web browser, **Then** the page displays with basic inline CSS styling for improved readability and clickable links
3. **Given** messages and readings for multiple dates exist, **When** index is generated, **Then** HTML lists are properly formatted with reverse chronological ordering
4. **Given** the index includes sections for different content types, **When** viewing the HTML, **Then** headings and structure clearly distinguish messages from readings with appropriate styling
5. **Given** a link is clicked in the index, **When** navigation occurs, **Then** the linked content page loads correctly

---

### User Story 3 - Configure Root URL to Serve Index Page (Priority: P3)

GitHub Pages is configured to publish from a dedicated branch (e.g., `gh-pages`) that contains only the `_site/` directory contents. The GitHub Actions workflow deploys generated content to this branch. Visiting `https://etotten.github.io/catholic-liturgy-tools/` automatically serves the index page without requiring `/index.html` in the URL.

**Why this priority**: Depends on P1 and P2 being complete. Provides the user-friendly URL experience and clean separation between source and published content. Requires GitHub Pages configuration and GitHub Actions workflow updates which can be tested independently.

**Independent Test**: Deploy the restructured site to GitHub Pages via the dedicated branch, visit the root URL (without `/index.html`), verify the index page loads correctly, test that both `/` and `/index.html` routes work and serve the same content, verify GitHub Actions successfully deploys to the branch.

**Acceptance Scenarios**:

1. **Given** GitHub Pages is configured to publish from `gh-pages` branch, **When** user visits `https://etotten.github.io/catholic-liturgy-tools/`, **Then** the index page is displayed without requiring `/index.html` in URL
2. **Given** the GitHub Actions workflow runs, **When** content is generated, **Then** it deploys only `_site/` directory contents to the `gh-pages` branch
3. **Given** both routes are tested, **When** visiting either `/` or `/index.html`, **Then** the same index page content is displayed
4. **Given** links within the site reference content, **When** navigating between pages, **Then** all relative paths resolve correctly from the published structure
5. **Given** the configuration is saved, **When** future deployments occur, **Then** the root URL behavior and branch deployment persist automatically

---

### User Story 4 - Update All Internal Links for New Structure (Priority: P4)

All links in generated content are updated to reflect the new `_site/` directory structure. Index page links correctly reference `messages/` and `readings/` subdirectories. Navigation works seamlessly throughout the site.

**Why this priority**: Depends on P1-P3 being complete. Ensures site navigation works correctly. Can be tested by clicking through all links and verifying they load correctly.

**Independent Test**: Generate full site content, verify all links in index page point to correct paths (`messages/...`, `readings/...`), click through each link to verify pages load, check for any broken links or 404 errors.

**Acceptance Scenarios**:

1. **Given** the index page contains links to messages, **When** a message link is clicked, **Then** the path correctly resolves to `messages/YYYY-MM-DD-daily-message.md`
2. **Given** the index page contains links to readings, **When** a readings link is clicked, **Then** the path correctly resolves to `readings/YYYY-MM-DD.html`
3. **Given** content pages exist in subdirectories, **When** navigating back to index, **Then** relative paths correctly resolve to `../index.html` or `/`
4. **Given** the site is fully generated, **When** running a link checker, **Then** zero broken links are reported
5. **Given** future content is added, **When** index regenerates, **Then** new links automatically use correct paths based on subdirectory structure

---

### Edge Cases

- What happens when the `_site` directory already exists with old structure content?
  - System should clean or migrate existing content to new subdirectory structure
  - Provide clear warnings if manual intervention needed for conflicting files
- How does system handle partial migration (some files in old locations, some in new)?
  - Migration utility should identify all content files regardless of current location
  - Move all content to appropriate new locations atomically
- What if GitHub Pages is configured to publish from wrong directory after restructuring?
  - Configuration validation should detect mismatch
  - Provide clear error messages with instructions to update GitHub Pages settings
- What happens when generating content if subdirectories don't exist yet?
  - System should automatically create missing subdirectories (`_site/messages/`, `_site/readings/`)
  - No manual directory creation should be required
- How are existing external links to old structure (e.g., bookmarks) handled?
  - Consider implementing redirects or placeholder files at old locations
  - Document breaking changes in migration guide

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST generate all site content files into a `_site` directory at the repository root
- **FR-002**: System MUST organize generated content into feature-specific subdirectories within `_site` (e.g., `_site/messages/`, `_site/readings/`)
- **FR-003**: System MUST generate daily message files in `_site/messages/` directory with filename pattern `YYYY-MM-DD-daily-message.md`
- **FR-004**: System MUST generate daily readings files in `_site/readings/` directory with filename pattern `YYYY-MM-DD.html`
- **FR-005**: System MUST generate the index page as `_site/index.html` (HTML format, not Markdown)
- **FR-006**: System MUST create necessary subdirectories automatically if they don't exist when generating content
- **FR-007**: Index page MUST include properly formatted HTML with semantic structure (headings, lists, links) and basic inline CSS for readability (fonts, spacing, colors)
- **FR-008**: Index page MUST display "Catholic Liturgy Tools" as the main heading/title
- **FR-009**: Index page MUST display two distinct sections: one for daily messages and one for daily readings
- **FR-010**: Index page MUST list content items in reverse chronological order (newest first) within each section
- **FR-011**: All links in the index page MUST use relative paths that resolve correctly from the `_site/` root
- **FR-012**: Links to messages MUST use path format `messages/YYYY-MM-DD-daily-message.md`
- **FR-013**: Links to readings MUST use path format `readings/YYYY-MM-DD.html`
- **FR-014**: Site MUST be accessible at root URL `https://etotten.github.io/catholic-liturgy-tools/` without requiring `/index.html`
- **FR-015**: Site MUST support both `/` and `/index.html` routes serving the same content
- **FR-016**: GitHub Pages MUST be configured to publish from a dedicated branch (e.g., `gh-pages`) containing only `_site/` contents
- **FR-017**: CLI commands MUST be updated to output content to new `_site/` directory structure
- **FR-018**: GitHub Actions workflow MUST commit generated content to `_site/` directory structure and deploy to GitHub Pages branch
- **FR-019**: System MUST preserve existing functionality for generating daily messages and readings while changing only output paths
- **FR-020**: Old content files in original locations (root, `_posts/`, `readings/`) MUST be deleted after successful one-time migration to `_site/` structure

### Key Entities

- **Site Content Directory (`_site/`)**: Root directory for all generated publishable content, separating it from source code and configuration files
- **Messages Subdirectory (`_site/messages/`)**: Contains all daily message files organized by date
- **Readings Subdirectory (`_site/readings/`)**: Contains all daily readings HTML pages organized by date
- **Index Page (`_site/index.html`)**: Single HTML entry point that links to all messages and readings, served at site root URL

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can access the site at root URL (`https://etotten.github.io/catholic-liturgy-tools/`) without requiring `/index.html` suffix
- **SC-002**: All generated content files are located within `_site/` directory structure with zero files remaining in old locations after migration
- **SC-003**: Index page displays as properly formatted HTML viewable in any standard web browser without Markdown rendering
- **SC-004**: All links on the index page successfully navigate to target content with zero broken links or 404 errors
- **SC-005**: Site structure clearly separates content by feature type with messages and readings in distinct subdirectories
- **SC-006**: Existing content generation workflows continue to function with updated output paths requiring zero changes to generation logic
- **SC-007**: Users can click any link on any page without understanding Markdown format or file extensions

## Assumptions

- GitHub Pages can be configured to publish from a dedicated branch (e.g., `gh-pages`) containing only site content
- Existing content generation code (message and readings generators) can be updated to output to new paths without breaking core logic
- GitHub Actions can deploy to a separate branch automatically as part of the workflow
- Migration from old structure to new structure will be a one-time development task, not built into CLI (keeps generation simple)
- Old content files can be safely deleted after migration since they're preserved in Git history
- Both Markdown files (messages) and HTML files (readings) can coexist in the same site structure
- Relative path links will work correctly when the site is served from GitHub Pages
- Users primarily access the site through the published GitHub Pages URL, not by browsing the repository directly
- The index page format change from Markdown to HTML with basic inline CSS is non-breaking for the intended audience
- Basic inline CSS (fonts, spacing, colors) is sufficient for readability without requiring external stylesheets or advanced styling

## Dependencies

- Existing daily message generation functionality (from feature 001-github-pages)
- Existing daily readings generation functionality (from feature 002-daily-readings)
- GitHub Pages hosting service and configuration access
- GitHub Actions workflow that deploys content

## Out of Scope

- Changes to the actual content format of daily messages (remains Markdown)
- Changes to the actual content format of daily readings (remains HTML)
- Changes to the scraping or fetching logic for readings
- Adding new content types beyond messages and readings
- Advanced CSS styling beyond basic inline styles for readability (no external stylesheets, responsive design frameworks, or complex layouts)
- JavaScript interactivity or dynamic features
- SEO optimization or meta tags (beyond basic HTML `<title>` and headings)
- Mobile responsiveness (beyond what basic HTML provides)
- Search functionality within the site
- RSS feeds or other content syndication
- Analytics or usage tracking
- User authentication or personalization
- Automated redirects from old URLs to new structure (old files will be deleted, redirects not implemented)
- Building migration functionality into CLI (migration is one-time development task)

---

## Implementation Additions (Not in Original Spec)

### Date Parameter Support for Content Regeneration

**Added During Implementation**: November 25, 2025  
**Reason**: Discovered need to regenerate content for specific historical dates via CLI workflow triggers

**Changes Made**:
1. GitHub Actions workflow accepts optional `date` input parameter (YYYY-MM-DD format)
2. `trigger-publish` CLI command accepts `--date` parameter to pass to workflow
3. `generate-message` CLI command accepts `--date` parameter for consistency with `generate-readings`
4. All date parameters default to today's date if not specified

**Rationale**:
- Users may need to regenerate content for specific dates (e.g., fixing errors, updating content)
- Workflow manual trigger via GitHub UI supports date input
- CLI trigger command should support same functionality for automation
- Feature parity: if `generate-readings` has `--date`, `generate-message` should too

**Impact**:
- **Backward Compatible**: All commands work without `--date` parameter (defaults to today)
- **Test Coverage**: Added 5 E2E tests for new functionality
- **Documentation**: Added to README.md with examples

