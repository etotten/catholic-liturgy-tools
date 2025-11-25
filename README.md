# Catholic Liturgy Tools

A Python-based tool for generating and publishing daily Catholic liturgical messages to GitHub Pages.

**Live Site**: https://etotten.github.io/catholic-liturgy-tools/

New messages are published daily at 6 AM Central Time, or whenever commits are pushed to the `main` branch.

## Features

- **Daily Message Generation**: Automatically generate markdown messages with Jekyll frontmatter
- **Daily Readings from USCCB**: Fetch and generate Catholic liturgical readings from the United States Conference of Catholic Bishops (USCCB)
- **Index Page Generation**: Create and maintain an index of all daily messages and readings in reverse chronological order
- **GitHub Actions Integration**: Trigger automated workflows to publish content to GitHub Pages
- **Command-Line Interface**: Simple CLI for local development and testing

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git
- A GitHub repository with Pages enabled
- Internet connection (for fetching readings from USCCB.org)

### Dependencies

The package automatically installs:
- `requests>=2.31.0` - HTTP library for fetching data
- `beautifulsoup4>=4.12.0` - HTML parsing library
- `lxml>=5.0.0` - Fast XML and HTML parser
- `python-dotenv>=1.0.0` - Environment variable management

### Install from Source

```bash
# Clone the repository
git clone https://github.com/etotten/catholic-liturgy-tools.git
cd catholic-liturgy-tools

# Install the package
pip install -e .
```

## Quick Start

### 0. Configure Environment Variables (Optional)

For commands that require GitHub API access (like `trigger-publish`), you can store your credentials in a `.env` file:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your GitHub Personal Access Token
# GITHUB_TOKEN=ghp_your_actual_token_here
```

**Security Note**: The `.env` file is already in `.gitignore` and will never be committed to version control.

### 1. Generate a Daily Message

```bash
# Generate today's message in the _site/messages directory (default)
catholic-liturgy generate-message

# Generate to a custom directory
catholic-liturgy generate-message --output-dir custom/posts
```

This creates a file like `_site/messages/2025-01-15-daily-message.md` with:
- YAML frontmatter (layout, date, title)
- A heading with the date
- Placeholder content for daily reflection

### 2. Generate Daily Readings

```bash
# Generate today's readings in the _site/readings directory (default)
catholic-liturgy generate-readings

# Generate readings for a specific date
catholic-liturgy generate-readings --date 2025-12-25

# Generate to a custom directory
catholic-liturgy generate-readings --output-dir custom/readings
```

This fetches readings from USCCB.org and creates a file like `_site/readings/2025-01-15.html` with:
- Liturgical day name (e.g., "Second Sunday in Ordinary Time")
- All daily readings (First Reading, Responsorial Psalm, Second Reading, Gospel)
- Biblical citations and full text
- Embedded CSS styling for readability
- Attribution link to USCCB source

**Note**: Requires internet connection to fetch readings from USCCB.org

### 3. Generate an Index Page

```bash
# Scan _site/messages and _site/readings directories, create _site/index.html
catholic-liturgy generate-index

# Use custom paths
catholic-liturgy generate-index --posts-dir custom/posts --readings-dir custom/readings --output-file custom-index.html
```

The index page is an HTML file with inline CSS that includes:
- HTML5 document structure with responsive styling
- "Catholic Liturgy Tools" heading
- Two sections:
  - **Daily Messages**: Links to all message files in reverse chronological order
  - **Daily Readings**: Links to all readings files (with liturgical day titles) in reverse chronological order
- Clean, readable typography with no external dependencies

### 4. Check GitHub Pages Status

```bash
# Check deployment status and recent workflow runs
catholic-liturgy check-pages
```

This displays:
- Site URL and configuration
- Current build status
- Recent workflow runs with status indicators
- Direct links to view workflow details

### 5. Trigger GitHub Actions Workflow

```bash
# Set your GitHub Personal Access Token
export GITHUB_TOKEN=ghp_your_token_here

# Trigger the publish workflow
catholic-liturgy trigger-publish

# Trigger a custom workflow or branch
catholic-liturgy trigger-publish --workflow-file custom-workflow.yml --branch develop
```

## GitHub Pages Setup

### 1. Enable GitHub Pages

1. Go to your repository settings
2. Navigate to **Pages** section
3. Set source to **GitHub Actions**

### 2. Site Structure

The tool generates a static site in the `_site/` directory:

```
_site/
├── index.html          # Main index with inline CSS
├── messages/           # Daily message files
│   └── YYYY-MM-DD-daily-message.md
└── readings/           # Daily readings HTML files
    └── YYYY-MM-DD.html
```

All files are standalone HTML with inline CSS - no external dependencies or build tools required.

### 3. Set Up GitHub Actions

The repository includes a workflow file at `.github/workflows/publish-content.yml` that:
- Runs daily at 6 AM Central Time (noon UTC) via cron schedule
- Can be manually triggered via `workflow_dispatch`
- Generates daily message and readings
- Updates the index page
- Deploys the `_site/` directory directly to GitHub Pages using artifact-based deployment

**Important**: The workflow uses the `github-pages` environment for deployment. If you want to deploy from branches other than `main`:

1. Go to **Settings** → **Environments** → **github-pages**
2. Under **Deployment branches**, click **Add deployment branch or tag rule**
3. Add patterns for branches you want to allow (e.g., `001-*` for feature branches)

Without this configuration, only the `main` branch will be able to deploy to GitHub Pages.

### 4. Configure GitHub Token

For the `trigger-publish` command to work, you need a GitHub Personal Access Token:

1. Go to **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Click **Generate new token** → **Generate new token (classic)**
3. Give it a descriptive name (e.g., "Catholic Liturgy Tools")
4. Select scopes: `repo` (Full control of private repositories)
5. Click **Generate token** and copy the token
6. Configure the token using **one of these methods**:

**Method 1: Using .env file (Recommended for local development)**

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your token
echo "GITHUB_TOKEN=ghp_your_token_here" > .env
```

**Method 2: Environment variable**

```bash
# Temporary (current session only)
export GITHUB_TOKEN=ghp_your_token_here

# Persistent (add to ~/.bashrc or ~/.zshrc)
echo 'export GITHUB_TOKEN=ghp_your_token_here' >> ~/.zshrc
source ~/.zshrc
```

**Security Note**: The `.env` file is in `.gitignore` and will never be committed. Never commit your token to version control!

## CLI Reference

### `generate-message`

Generate a daily message markdown file.

```bash
catholic-liturgy generate-message [--output-dir DIR]
```

**Options:**
- `--output-dir`, `-o`: Directory for output (default: `_posts`)

**Example:**
```bash
catholic-liturgy generate-message --output-dir docs/_posts
```

---

### `generate-readings`

Fetch daily Catholic liturgical readings from USCCB.org and generate an HTML page.

```bash
catholic-liturgy generate-readings [--date DATE] [--output-dir DIR]
```

**Options:**
- `--date`, `-d`: Date to generate readings for in YYYY-MM-DD format (default: today)
- `--output-dir`, `-o`: Output directory for HTML files (default: `readings`)

**Examples:**

```bash
# Generate today's readings
catholic-liturgy generate-readings

# Generate readings for Christmas
catholic-liturgy generate-readings --date 2025-12-25

# Short options
catholic-liturgy generate-readings -d 2025-12-25 -o custom/readings
```

**Exit Codes:**
- `0`: Success
- `1`: Network error (connection failed, timeout)
- `2`: Validation error (invalid date format)
- `3`: Parse error (USCCB website structure changed)
- `4`: File system error (permission denied, directory not found)
- `5`: Unknown error

**Requirements:**
- Internet connection to fetch from USCCB.org
- Write permissions for output directory

**Output:**
- Creates HTML file: `{output_dir}/{YYYY-MM-DD}.html`
- Includes liturgical day name, readings with citations, embedded CSS
- Attribution link to USCCB source

---

### `generate-index`

Generate an index page listing all daily messages and readings.

```bash
catholic-liturgy generate-index [--posts-dir DIR] [--readings-dir DIR] [--output-file FILE]
```

**Options:**
- `--posts-dir`, `-p`: Directory containing message files (default: `_posts`)
- `--readings-dir`, `-r`: Directory containing readings files (default: `readings`)
- `--output-file`, `-o`: Output file path (default: `index.md`)

**Examples:**

```bash
# Scan both _posts and readings directories
catholic-liturgy generate-index

# Use custom paths
catholic-liturgy generate-index --posts-dir docs/_posts --readings-dir docs/readings --output-file docs/index.md

# Short options
catholic-liturgy generate-index -p custom/posts -r custom/readings -o custom-index.md
```

**Output:**
- Scans message and readings directories
- Displays counts for both
- Generates index.md with two sections:
  - Daily Messages (links to markdown files)
  - Daily Readings (links to HTML files)
- Both sections in reverse chronological order (newest first)

---

### `check-pages`

Check GitHub Pages deployment status and recent workflow runs.

```bash
catholic-liturgy check-pages
```

**Requirements:**
- `GITHUB_TOKEN` environment variable must be set

**Output includes:**
- Site URL and configuration
- Current build status
- Recent workflow runs with status (✅ success, ❌ failure, 🔄 in progress)
- Links to view detailed workflow logs

**Example:**
```bash
export GITHUB_TOKEN=ghp_your_token_here
catholic-liturgy check-pages
```

### `trigger-publish`

Trigger a GitHub Actions workflow to publish content.

```bash
catholic-liturgy trigger-publish [--workflow-file FILE] [--branch BRANCH]
```

**Options:**
- `--workflow-file`: Workflow filename (default: `publish-daily-message.yml`)
- `--branch`: Branch to run workflow on (default: `main`)

**Requirements:**
- `GITHUB_TOKEN` environment variable must be set

**Example:**
```bash
export GITHUB_TOKEN=ghp_your_token_here
catholic-liturgy trigger-publish --branch main
```

## Development

### Local Development Workflow

#### Step 1: Activate Virtual Environment

```bash
# Create virtual environment (first time only)
python3.11 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Verify Python version
python --version  # Should show Python 3.11.x
```

#### Step 2: Install in Editable Mode

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Verify installation
catholic-liturgy --help
```

#### Step 3: Generate Message

```bash
# Generate today's message
catholic-liturgy generate-message

# Verify file created
ls -la _posts/
cat _posts/$(date +%Y-%m-%d)-daily-message.md
```

#### Step 4: Generate Readings

```bash
# Generate today's readings (requires internet connection)
catholic-liturgy generate-readings

# Verify file created
ls -la readings/
# Open in browser to view
open readings/$(date +%Y-%m-%d).html  # macOS
# or: start readings/$(date +%Y-%m-%d).html  # Windows
```

#### Step 5: Generate Index

```bash
# Generate index page (includes both messages and readings)
catholic-liturgy generate-index

# View the index
cat index.md
```

#### Step 6: Run Tests

```bash
# Run all tests with coverage
pytest

# Should show: 289 passed, 1 skipped, coverage ≥90%
```

### Running Tests

The project uses pytest for testing with comprehensive coverage requirements (≥90%):

```bash
# Run all tests (289 tests)
pytest tests/

# Run with coverage report
pytest tests/ --cov=catholic_liturgy_tools --cov-report=term-missing

# Run specific test categories
pytest tests/unit/          # Unit tests only
pytest tests/integration/   # Integration tests only (includes network tests)
pytest tests/e2e/           # End-to-end tests only

# Skip slow integration tests (that hit live USCCB site)
pytest -m "not integration"

# Run only integration tests
pytest -m "integration"

# Run specific test file
pytest tests/unit/test_message.py
pytest tests/unit/test_usccb_scraper.py

# Run specific test function
pytest tests/e2e/test_cli_generate.py::test_generate_message_creates_file
pytest tests/e2e/test_cli_readings.py::test_generate_readings_with_date
```

**Note on Integration Tests**: Some integration tests fetch live data from USCCB.org and are marked with `@pytest.mark.integration` and `@pytest.mark.slow`. These tests:
- Require internet connection
- Take longer to run (~17 seconds with rate limiting)
- Can be skipped with `-m "not integration"`
- Are useful for verifying the scraper still works with current USCCB website structure

### Generate HTML Coverage Report

```bash
# Generate HTML report
pytest --cov-report=html

# Open in browser
open htmlcov/index.html  # macOS
# or: start htmlcov/index.html  # Windows
# or: xdg-open htmlcov/index.html  # Linux
```

### Test Organization

- **Unit Tests** (`tests/unit/`): Test individual functions and modules in isolation
- **Integration Tests** (`tests/integration/`): Test workflows across multiple modules
- **End-to-End Tests** (`tests/e2e/`): Test CLI commands via subprocess execution

### Common Development Tasks

#### Clean Generated Files

```bash
# Remove all generated files
rm -rf _posts/
rm -f index.md

# Regenerate from scratch
catholic-liturgy generate-message
catholic-liturgy generate-index
```

#### Test Full Workflow Locally

```bash
# 1. Generate message
catholic-liturgy generate-message

# 2. Generate readings (requires internet)
catholic-liturgy generate-readings

# 3. Generate index (includes both messages and readings)
catholic-liturgy generate-index

# 4. Verify files exist
ls -la _posts/
ls -la readings/
cat index.md

# 5. View readings in browser
open readings/$(date +%Y-%m-%d).html  # macOS

# 6. Run tests (skip slow integration tests)
pytest -m "not integration"

# 7. Run all tests including integration tests
pytest

# 8. Check coverage
pytest --cov-report=term-missing
```

### Troubleshooting

#### Issue: `catholic-liturgy` command not found

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall package
pip install -e ".[dev]"
```

#### Issue: Permission denied when writing files

**Solution**:
```bash
# Check directory permissions
ls -la

# Ensure you have write permissions
chmod u+w .
```

#### Issue: `GITHUB_TOKEN` not set

**Solution**:
```bash
# Set environment variable
export GITHUB_TOKEN=ghp_your_token_here

# Verify it's set
echo $GITHUB_TOKEN
```

#### Issue: GitHub Actions workflow not found

**Solution**:
- Ensure `.github/workflows/publish-daily-message.yml` exists
- Ensure workflow file is committed and pushed to GitHub
- Verify workflow name matches the one specified in `trigger-publish` command

#### Issue: Tests failing with import errors

**Solution**:
```bash
# Reinstall package in editable mode
pip install -e ".[dev]"

# Verify installation
pip list | grep catholic-liturgy-tools
```

#### Issue: Coverage below 90%

**Solution**:
```bash
# Generate detailed coverage report
pytest --cov-report=term-missing

# Identify uncovered lines (shown with `!!!!!`)
# Add tests for those lines
```

#### Issue: `generate-readings` network error

**Symptoms**:
```
Error: Failed to fetch readings from USCCB.org
Network error: Connection timeout after 30 seconds
```

**Solution**:
```bash
# Check internet connection
ping bible.usccb.org

# Check if USCCB site is accessible
curl -I https://bible.usccb.org/bible/readings/

# Try with explicit date
catholic-liturgy generate-readings --date 2025-12-25

# Check firewall/proxy settings if behind corporate network
```

#### Issue: `generate-readings` parse error

**Symptoms**:
```
Error: Failed to parse readings from USCCB page
The USCCB website structure may have changed.
```

**Solution**:
- The USCCB website structure may have changed
- Report issue at: https://github.com/etotten/catholic-liturgy-tools/issues
- Include the date you were trying to fetch
- Developers will update the scraper to match new HTML structure

#### Issue: `generate-readings` returns no readings for future date

**Symptoms**:
- Command succeeds but USCCB shows no readings for distant future date

**Solution**:
- USCCB typically publishes readings 4-8 weeks in advance
- For major feast days (Christmas, Easter), readings may be available earlier
- Try dates closer to current date
- Check USCCB.org directly to see if readings are published

#### Issue: `generate-index` doesn't show readings

**Symptoms**:
- Index page only shows "Daily Messages" section
- Missing "Daily Readings" section

**Solution**:
```bash
# Ensure readings directory exists and has HTML files
ls -la readings/
file readings/*.html

# Verify readings directory path
catholic-liturgy generate-index --readings-dir readings

# Generate a reading first if directory is empty
catholic-liturgy generate-readings
catholic-liturgy generate-index
```

### Jekyll Local Preview (Optional)

To preview the GitHub Pages site locally before publishing:

#### 1. Install Jekyll

```bash
# macOS (requires Homebrew)
brew install ruby
gem install bundler jekyll

# Linux (Ubuntu/Debian)
sudo apt-get install ruby-full build-essential zlib1g-dev
gem install bundler jekyll

# Windows: Use RubyInstaller (https://rubyinstaller.org/)
```

#### 2. Create Gemfile

```bash
# In repository root, create Gemfile:
cat > Gemfile << 'EOF'
source "https://rubygems.org"
gem "github-pages", group: :jekyll_plugins
EOF
```

#### 3. Install Dependencies

```bash
bundle install
```

#### 4. Serve Locally

```bash
bundle exec jekyll serve

# Output: Server running at http://127.0.0.1:4000/
```

#### 5. View in Browser

Open http://127.0.0.1:4000/ to see the site.

**Note**: Jekyll preview is optional and not required for development. The GitHub Actions workflow handles publishing automatically.

### Project Structure

```
catholic-liturgy-tools/
├── src/
│   └── catholic_liturgy_tools/
│       ├── __init__.py
│       ├── __main__.py          # Module entry point
│       ├── cli.py                # CLI interface
│       ├── generator/
│       │   ├── message.py        # Message generation logic
│       │   ├── index.py          # Index generation logic
│       │   └── readings.py       # Readings HTML generation
│       ├── scraper/
│       │   ├── usccb.py          # USCCB readings scraper
│       │   ├── models.py         # Data models (ReadingEntry, DailyReading)
│       │   └── exceptions.py     # Custom exceptions
│       ├── github/
│       │   └── actions.py        # GitHub Actions API integration
│       └── utils/
│           ├── date_utils.py     # Date handling utilities
│           ├── file_ops.py       # File operation utilities
│           ├── html_utils.py     # HTML sanitization utilities
│           └── retry.py          # Retry decorator with backoff
├── tests/
│   ├── conftest.py               # Shared pytest fixtures
│   ├── fixtures/
│   │   └── usccb_html/           # HTML fixtures for testing scraper
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests (includes live USCCB tests)
│   └── e2e/                      # End-to-end tests
├── _posts/                       # Generated daily messages
├── readings/                     # Generated daily readings HTML files
├── index.md                      # Generated index page
├── _config.yml                   # Jekyll configuration
├── .github/
│   └── workflows/
│       └── publish-daily-message.yml  # GitHub Actions workflow
└── pyproject.toml                # Package configuration
```

### Development Best Practices

1. **Always activate virtual environment** before working
2. **Run tests before committing** (ensure nothing breaks)
3. **Check coverage** (must be 90%+)
4. **Write E2E tests** for CLI commands (constitutional requirement)
5. **Keep it simple** (avoid premature abstractions)
6. **Document as you go** (update README with new commands)

## Data Sources & Attribution

### Daily Readings

Daily Catholic liturgical readings are sourced from the **United States Conference of Catholic Bishops (USCCB)** website:

- **Source**: https://bible.usccb.org/
- **Purpose**: Educational and personal devotional use
- **Content**: Scripture readings from the Lectionary for Mass
- **Copyright**: Scripture texts are from the New American Bible, revised edition © 2010, 1991, 1986, 1970 Confraternity of Christian Doctrine, Washington, D.C.

All generated HTML pages include:
- Attribution link to USCCB source
- Direct link to original readings on USCCB.org
- Copyright notice for Scripture texts

**Note**: This tool is for educational and personal devotional purposes. The readings are fetched programmatically from publicly available pages on USCCB.org. Users should respect USCCB's terms of use and copyright policies.

### Limitations

- **Availability**: USCCB typically publishes readings 4-8 weeks in advance
- **Special Days**: Some feast days may have multiple Mass options (e.g., Christmas Day); the tool will detect and report these cases
- **Website Changes**: If USCCB changes their website structure, the scraper may need updates. Please report issues on GitHub.
- **Rate Limiting**: The tool implements polite scraping with retry logic and backoff to avoid overwhelming USCCB servers

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please [open an issue](https://github.com/etotten/catholic-liturgy-tools/issues) on GitHub.
