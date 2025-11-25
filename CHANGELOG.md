# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.3.0] - 2025-11-25

### Added

- **`_site/` directory structure**: All generated content now organized in a dedicated site directory
  - `_site/messages/`: Daily message Markdown files
  - `_site/readings/`: Daily readings HTML files
  - `_site/index.html`: Site index page (now HTML instead of Markdown)
  
- **HTML index page**: Converted from Markdown to HTML5 with inline CSS
  - Clean, modern design with "Catholic Liturgy Tools" heading
  - Responsive layout (max-width 800px, centered)
  - Two sections: Daily Messages and Daily Readings
  - Relative links for subdirectory navigation
  - Reverse chronological sorting for both sections
  - Empty state messages when no content available
  - Mobile-friendly with viewport meta tag

- **GitHub Pages deployment**: Automated deployment to gh-pages branch
  - Uses `peaceiris/actions-gh-pages@v3` action
  - Deploys only `_site/` contents to branch root
  - Force orphan history for clean commits
  - Enables root URL access: https://etotten.github.io/catholic-liturgy-tools/

### Changed

- **Version**: Bumped from 0.2.0 to 0.3.0 (MINOR - backward compatible new features)
- **CLI defaults**: All commands now default to `_site/` subdirectories:
  - `generate-message`: `_site/messages/` (was `_posts/`)
  - `generate-readings`: `_site/readings/` (was `readings/`)
  - `generate-index`: `_site/index.html` (was `index.md`)
- **Index format**: Changed from Markdown (`index.md`) to HTML (`index.html`)
- **Workflow**: Simplified from 2 jobs (89 lines) to 1 job (42 lines)
  - Removed manual git commit steps
  - Removed separate Pages artifact upload and deploy job
  - Deploys directly to gh-pages branch

### Fixed

- Test coverage improved to 92.5% (exceeds 90% requirement)
- All 294 tests passing with updated HTML expectations
- Removed dead code files (backup generators)

### Backward Compatibility

- Custom `--output-dir` paths still supported for all commands
- Existing content migration required (see README.md)

### Technical Details

- **Coverage**: 92.52% (481 statements, 36 uncovered - all defensive/exceptional paths)
- **Tests**: 294 passed, 1 skipped (expected)
- **HTML Generation**: Proper DOCTYPE, charset, viewport, semantic structure
- **CSS**: Inline styles for zero external dependencies
- **Deployment**: gh-pages branch with orphan history

---

## [0.2.0] - 2025-01-25

### Added

- **Daily Catholic Readings**: Automatically fetch and publish daily readings from the USCCB
  - Includes First Reading, Responsorial Psalm, Second Reading (when applicable), and Gospel
  - Supports all liturgical seasons (Ordinary Time, Advent, Christmas, Lent, Easter)
  - Handles special feast days and solemnities
  - Beautiful, mobile-friendly HTML pages with responsive design
  - Automatic liturgical day names (e.g., "Memorial of Saint Cecilia")

- **`generate-readings` CLI command**: Generate daily readings HTML page
  - `--date` / `-d`: Specify date in YYYY-MM-DD format (default: today)
  - `--output-dir` / `-o`: Custom output directory (default: readings/)
  - Example: `catholic-liturgy generate-readings --date 2025-12-25`

- **Enhanced index page**: Now includes both Daily Messages and Daily Readings sections
  - Automatic scanning and parsing of readings HTML files
  - Liturgical day names extracted from page content
  - Reverse chronological sorting for both sections

- **GitHub Actions automation**: Renamed workflow now generates both messages and readings
  - Workflow renamed: `publish-daily-message.yml` → `publish-content.yml`
  - Runs daily via cron schedule
  - Supports manual workflow dispatch

### Changed

- **Version**: Bumped from 0.1.0 to 0.2.0
- **Dependencies**: Added `beautifulsoup4>=4.12.0` and `lxml>=5.0.0`
- **Workflow Name**: Changed default workflow from `publish-daily-message.yml` to `publish-content.yml`
- **Test Performance**: Optimized slow tests with mocked `time.sleep`, reducing test suite time from ~50s to ~21s

### Fixed

- CLI parser default workflow name bug (was using old workflow name, causing 422 errors)
- All tests now properly mock `time.sleep` to avoid real delays

### Technical Details

- **Scraper Coverage**: 92.42% (132 statements, 10 uncovered)
- **HTML Generator Coverage**: 100% (28 statements, 0 uncovered)
- **Total Test Suite**: 291 tests (290 passing, 1 skipped as expected)
- **Test Execution Time**: 20.88s (58% improvement from 49.28s)

## [0.1.0] - 2025-11-22

### Added

- Initial release
- Daily message generation with Jekyll frontmatter
- Index page generation for messages
- GitHub Actions integration for automated publishing
- CLI with three commands: `generate-message`, `generate-index`, `trigger-publish`
- GitHub Pages deployment workflow
- Basic test suite with unit and E2E tests

### Features

- Generate daily messages in Markdown format
- Create and maintain an index page of all messages
- Trigger GitHub Actions workflows via CLI
- Automated daily publishing at 6 AM Central Time

---

[0.2.0]: https://github.com/etotten/catholic-liturgy-tools/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/etotten/catholic-liturgy-tools/releases/tag/v0.1.0
