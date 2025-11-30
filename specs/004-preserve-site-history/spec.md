# Feature Specification: Preserve Site Historical Content

**Feature Branch**: `004-preserve-site-history`  
**Created**: 2025-11-25  
**Status**: Draft  
**Input**: User description: "We introduced an issue with the site restructure: the index page for the site now only shows the latest reading and message; history of past generation and publishing is lost (at least to the index page, but I'm concerned it may be lost from the site completely); this is probably due to no longer preserving the old generated content in the repo; the requirement which we need to re-establish is that we preserve everything we generated, so each time we publish to the site, there is more content added to what already exists; The index page should get longer as the links to the pages will grow; the latest publishing needs to be at the top for each feature."

## Clarifications

### Session 2025-11-30

- Q: When content is regenerated for a date that already exists, how should the system handle the duplicate? → A: Overwrite - Replace existing files with newly generated content to allow corrections, bug fixes, and experimentation. Old versions can be retrieved from Git history if needed.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Accumulate Content Over Time (Priority: P1)

Each time content is generated and published, it is added to existing content rather than replacing it. The repository preserves all previously generated messages and readings files. Users can browse the complete history of published content dating back to the first generation. The site grows over time as new content is added daily.

**Why this priority**: This is the core issue - without content preservation, the site loses its historical value and users cannot access past content. This must work first before anything else matters. Can be tested independently by generating content on multiple dates and verifying all files persist.

**Independent Test**: Generate content for Date 1, verify files exist. Generate content for Date 2, verify both Date 1 and Date 2 files exist. Check repository shows all generated files. Verify no files are deleted between generation runs.

**Acceptance Scenarios**:

1. **Given** content has been generated for November 23, **When** content is generated for November 24, **Then** both November 23 and November 24 files exist in the repository
2. **Given** five days of messages exist in `_site/messages/`, **When** generating a sixth message, **Then** all six message files are present in the directory
3. **Given** three days of readings exist in `_site/readings/`, **When** generating a fourth reading, **Then** all four readings files are present in the directory
4. **Given** content generation has run for 30 days, **When** viewing the `_site/` directory, **Then** 30 message files and 30 readings files are present
5. **Given** the repository contains generated content, **When** the generation workflow runs again, **Then** no existing content files are deleted or overwritten

---

### User Story 2 - Index Page Shows Complete History (Priority: P2)

The index page displays links to all previously generated content, organized in reverse chronological order (newest first). As new content is generated, the index page grows to include new links while preserving all previous links. Users can click any link to access historical messages and readings from any past date.

**Why this priority**: Depends on P1 preserving files, but is the primary way users discover and access content. Without an updated index, preserved files are difficult to find. Can be tested independently by verifying index HTML contains all expected links.

**Independent Test**: Generate content for multiple dates, inspect `_site/index.html`, verify it contains links to all message and readings files. Check that newest content appears first in each section. Verify all links are clickable and point to existing files.

**Acceptance Scenarios**:

1. **Given** messages exist for November 21, 22, and 23, **When** the index page is regenerated, **Then** links to all three messages appear with November 23 listed first
2. **Given** readings exist for five different dates, **When** the index page is regenerated, **Then** all five readings links appear in reverse chronological order
3. **Given** new content is generated for November 25, **When** the index page is regenerated, **Then** the November 25 links appear at the top of their respective sections
4. **Given** the index page lists 20 messages, **When** a 21st message is generated and index regenerated, **Then** the index displays all 21 message links with the newest first
5. **Given** historical content exists from September through November, **When** viewing the index page, **Then** all months' content is linked and organized chronologically within each section

---

### User Story 3 - Prevent Accidental Content Loss (Priority: P3)

The publishing workflow never deletes existing content files from other dates. Content files are only added, never removed from the historical archive. If a file with the same name already exists (regenerating the same date), the system overwrites it to allow corrections and updates, while all other dates' content remains untouched.

**Why this priority**: Depends on P1 and P2 working. Provides safety guardrails to prevent accidental content loss. Can be tested by attempting to regenerate content for the same date multiple times.

**Independent Test**: Generate content for November 23, note the file. Regenerate content for November 23, verify the original content is either preserved as-is, renamed with version, or explicitly overwritten only if that behavior is intended. Verify no unintended deletion of other dates' content.

**Acceptance Scenarios**:

1. **Given** a message exists for November 23, **When** regenerating content for November 23, **Then** the November 23 file is overwritten with new content while all other dates' content remains unchanged
2. **Given** 10 days of content exist, **When** generation runs for a new date, **Then** all 10 existing files remain untouched
3. **Given** the workflow runs for date November 24, **When** generation completes, **Then** no files for November 23 or earlier are modified or deleted
4. **Given** content is generated incrementally over time, **When** checking the repository history, **Then** all generated content files show as additions, not deletions or replacements
5. **Given** the index page is regenerated, **When** the new index is written, **Then** the old index content (all historical links) is preserved in the new version

---

### Edge Cases

- What happens when the `_site` directory is accidentally deleted?
  - System should regenerate all content on next run, including index with all available files
  - Historical content may be lost if not preserved elsewhere (e.g., deployment branch)
- How does system handle gaps in published dates (e.g., no content for weekends)?
  - Index page lists only dates with actual content, gaps are acceptable
  - No placeholder files needed for missing dates
- What happens if generation fails partway through?
  - Partially generated content should not corrupt or delete existing content
  - Failed generation should be retryable without data loss
- How does system handle very large numbers of historical files (years of daily content)?
  - Index page may become long but should handle hundreds of links
  - Consider future pagination or filtering if performance degrades
- What if the deployment process fails after generation but before publishing?
  - Generated files persist in repository for retry
  - Next deployment publishes all accumulated content including previous run's files
- What happens if content for the same date is regenerated intentionally?
  - System overwrites the existing file for that date with newly generated content
  - Allows fixing bugs, correcting errors, or updating content after improvements
  - Previous versions can be retrieved from Git history if needed
  - Other dates' content remains completely unaffected

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST preserve all previously generated content files when generating new content
- **FR-002**: System MUST NOT delete existing content files during generation or publishing workflows
- **FR-003**: Content generation MUST operate in append-only mode, adding new files without removing old ones
- **FR-004**: System MUST commit all generated content files to the repository after each generation run
- **FR-005**: System MUST include all historical content files when deploying to the publishing branch (e.g., `gh-pages`)
- **FR-006**: Index page generation MUST scan all existing content files in `_site/messages/` and `_site/readings/` directories
- **FR-007**: Index page MUST include links to all discovered message files, not just the most recent one
- **FR-008**: Index page MUST include links to all discovered readings files, not just the most recent one
- **FR-009**: Index page MUST list content in reverse chronological order with newest items appearing first in each section
- **FR-010**: Each content generation run MUST add the new content files to the existing set without overwriting the index's historical links
- **FR-011**: System MUST regenerate the index page to include newly generated content while preserving links to all existing content
- **FR-012**: Publishing workflow MUST deploy all files in `_site/` directory, not just newly generated ones
- **FR-013**: System MUST overwrite existing content files when regenerating content for a date that already has files, allowing corrections and updates while preserving all other dates' content
- **FR-014**: Content files MUST remain in the repository permanently unless explicitly removed by manual intervention
- **FR-015**: System MUST verify all content files referenced in index links actually exist in the repository

### Key Entities

- **Historical Content Archive**: The complete collection of all generated message and readings files accumulated over time
- **Content Generation Run**: A single execution of content generation that adds new files without removing existing ones
- **Index Page**: A dynamically generated page that lists all available historical content with newest items first
- **Publishing Workflow**: The process that deploys all accumulated content files from the repository to the public site

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: After 30 days of daily generation, the site contains 30 message files and 30 readings files with zero deletions
- **SC-002**: Users can access content from any previously published date by clicking links on the index page
- **SC-003**: The index page displays all historical content links, growing by 2 links (1 message + 1 reading) per day of generation
- **SC-004**: Regenerating the index page after 10 days of content results in 10 message links and 10 readings links in reverse chronological order
- **SC-005**: Content generated on Day 1 remains accessible and unchanged on Day 30 after 29 additional generation runs
- **SC-006**: All links on the index page successfully resolve to existing content files with zero broken links
- **SC-007**: The published site shows continuous growth with each deployment adding to previous content, never replacing it

## Assumptions

- The issue was introduced by feature 003-site-content-restructure which changed how content is generated and published
- The current generation workflow may be regenerating the entire `_site/` directory from scratch each time instead of adding to it
- The repository's main branch should contain all generated content for preservation and version control
- The deployment process should copy all content from the main branch to the publishing branch, not just new files
- Content files follow predictable naming patterns (`YYYY-MM-DD-daily-message.md`, `YYYY-MM-DD.html`) allowing the index generator to discover them
- The index page can handle displaying dozens or hundreds of links without significant performance issues
- Users want to access historical content and view the site's growth over time
- No content should be deleted unless explicitly managed outside the automated workflow
- Regenerating content for the same date is supported to allow bug fixes, corrections, and experimentation, with overwrite behavior that replaces the specific date's content
- The repository size can accommodate daily content accumulation for an extended period (multiple years)

## Dependencies

- Feature 001-github-pages (daily message generation)
- Feature 002-daily-readings (readings generation)
- Feature 003-site-content-restructure (`_site/` directory structure and index page generation)
- GitHub Actions workflow for automated generation and publishing
- Git repository for content preservation

## Out of Scope

- Manual content curation or editing of historical content
- Archival or backup strategies beyond Git version control
- Performance optimization for extremely large content collections (>1000 files)
- Search functionality to help users find specific historical dates
- Pagination or filtering of the index page
- Content versioning when regenerating the same date (overwrite behavior replaces files; previous versions available in Git history)
- Migration of content that may have been lost before this fix
- Automated recovery of accidentally deleted content
- Content expiration or cleanup policies
- Alternate views of historical content (calendar view, monthly archives, etc.)
