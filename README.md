# Catholic Liturgy Tools

A Python-based tool for generating and publishing daily Catholic liturgical messages to GitHub Pages.

**Live Site**: https://etotten.github.io/catholic-liturgy-tools/

New messages are published daily at 6 AM Central Time, or whenever commits are pushed to the `main` branch.

## Features

- **Daily Message Generation**: Automatically generate markdown messages with Jekyll frontmatter
- **Index Page Generation**: Create and maintain an index of all daily messages in reverse chronological order
- **GitHub Actions Integration**: Trigger automated workflows to publish content to GitHub Pages
- **Command-Line Interface**: Simple CLI for local development and testing

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git
- A GitHub repository with Pages enabled

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
# Generate today's message in the _posts directory
catholic-liturgy generate-message

# Generate to a custom directory
catholic-liturgy generate-message --output-dir custom/posts
```

This creates a file like `_posts/2025-01-15-daily-message.md` with:
- YAML frontmatter (layout, date, title)
- A heading with the date
- Placeholder content for daily reflection

### 2. Generate an Index Page

```bash
# Scan _posts directory and create index.md
catholic-liturgy generate-index

# Use custom paths
catholic-liturgy generate-index --posts-dir custom/posts --output-file custom-index.md
```

The index page includes:
- YAML frontmatter with "Daily Messages" title
- Links to all message files in reverse chronological order (newest first)

### 3. Check GitHub Pages Status

```bash
# Check deployment status and recent workflow runs
catholic-liturgy check-pages
```

This displays:
- Site URL and configuration
- Current build status
- Recent workflow runs with status indicators
- Direct links to view workflow details

### 4. Trigger GitHub Actions Workflow

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

### 2. Configure Jekyll

The repository includes a `_config.yml` file with minimal Jekyll configuration:

```yaml
theme: minima
title: Daily Catholic Messages
description: Daily reflections and messages
exclude:
  - src/
  - tests/
```

### 3. Set Up GitHub Actions

The repository includes a workflow file at `.github/workflows/publish-daily-message.yml` that:
- Runs daily at 6 AM Central Time (noon UTC) via cron schedule
- Can be manually triggered via `workflow_dispatch`
- Generates a new daily message
- Updates the index page
- Commits and pushes changes to trigger GitHub Pages deployment

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
- `--output-dir`: Directory for output (default: `_posts`)

**Example:**
```bash
catholic-liturgy generate-message --output-dir docs/_posts
```

### `generate-index`

Generate an index page listing all daily messages.

```bash
catholic-liturgy generate-index [--posts-dir DIR] [--output-file FILE]
```

**Options:**
- `--posts-dir`: Directory containing message files (default: `_posts`)
- `--output-file`: Output file path (default: `index.md`)

**Example:**
```bash
catholic-liturgy generate-index --posts-dir docs/_posts --output-file docs/index.md
```

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

#### Step 4: Generate Index

```bash
# Generate index page
catholic-liturgy generate-index

# View the index
cat index.md
```

#### Step 5: Run Tests

```bash
# Run all tests with coverage
pytest

# Should show: 108 passed, coverage ≥90%
```

### Running Tests

The project uses pytest for testing with comprehensive coverage requirements (≥90%):

```bash
# Run all tests
pytest tests/

# Run with coverage report
pytest tests/ --cov=catholic_liturgy_tools --cov-report=term-missing

# Run specific test categories
pytest tests/unit/          # Unit tests only
pytest tests/integration/   # Integration tests only
pytest tests/e2e/           # End-to-end tests only

# Run specific test file
pytest tests/unit/test_message.py

# Run specific test function
pytest tests/e2e/test_cli_generate.py::test_generate_message_creates_file
```

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

# 2. Generate index
catholic-liturgy generate-index

# 3. Verify files exist
ls -la _posts/
cat index.md

# 4. Run tests
pytest

# 5. Check coverage
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
│       │   └── index.py          # Index generation logic
│       ├── github/
│       │   └── actions.py        # GitHub Actions API integration
│       └── utils/
│           ├── date_utils.py     # Date handling utilities
│           └── file_ops.py       # File operation utilities
├── tests/
│   ├── conftest.py               # Shared pytest fixtures
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── e2e/                      # End-to-end tests
├── _posts/                       # Generated daily messages
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

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please [open an issue](https://github.com/etotten/catholic-liturgy-tools/issues) on GitHub.
