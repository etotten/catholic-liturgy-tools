# Catholic Liturgy Tools

A Python-based tool for generating and publishing daily Catholic liturgical messages to GitHub Pages.

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

### 3. Trigger GitHub Actions Workflow

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
- Runs daily at 6 AM UTC via cron schedule
- Can be manually triggered via `workflow_dispatch`
- Generates a new daily message
- Updates the index page
- Commits and pushes changes to trigger GitHub Pages deployment

### 4. Configure GitHub Token

For the `trigger-publish` command to work, you need a GitHub Personal Access Token:

1. Go to **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Click **Generate new token** → **Generate new token (classic)**
3. Give it a descriptive name (e.g., "Catholic Liturgy Tools")
4. Select scopes: `repo` (Full control of private repositories)
5. Click **Generate token** and copy the token
6. Set it as an environment variable:

```bash
export GITHUB_TOKEN=ghp_your_token_here
```

For persistent storage, add it to your `~/.bashrc` or `~/.zshrc`:

```bash
echo 'export GITHUB_TOKEN=ghp_your_token_here' >> ~/.zshrc
```

**Security Note**: Never commit your token to version control!

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
```

### Test Organization

- **Unit Tests** (`tests/unit/`): Test individual functions and modules in isolation
- **Integration Tests** (`tests/integration/`): Test workflows across multiple modules
- **End-to-End Tests** (`tests/e2e/`): Test CLI commands via subprocess execution

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
├── _config.yml                   # Jekyll configuration
├── .github/
│   └── workflows/
│       └── publish-daily-message.yml  # GitHub Actions workflow
└── pyproject.toml                # Package configuration
```

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please [open an issue](https://github.com/etotten/catholic-liturgy-tools/issues) on GitHub.
