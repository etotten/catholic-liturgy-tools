# Contract: CLI Commands

**Feature**: 005-daily-reflections  
**Purpose**: Define command-line interface extensions for generating AI-augmented daily reflections

---

## Command Extensions

### `generate-readings` (Extended)

**Current Behavior**: Generates HTML files for daily Mass readings from USCCB

**New Options**:

```bash
catholic-liturgy-tools generate-readings [OPTIONS]
```

**Options**:

- `--with-reflections` / `--no-reflections`
  - **Type**: Boolean flag
  - **Default**: `--with-reflections` (enabled)
  - **Purpose**: Enable/disable AI-generated reflection content
  - **Example**: `--no-reflections` to generate only readings without AI content

- `--date DATE`
  - **Type**: Date (YYYY-MM-DD format)
  - **Default**: Today's date
  - **Purpose**: Generate reflection for specific date
  - **Example**: `--date 2025-12-25`
  - **Notes**: Existing option, works with reflections

- `--output-dir PATH`
  - **Type**: Directory path
  - **Default**: `_site/readings/`
  - **Purpose**: Output directory for generated HTML
  - **Example**: `--output-dir /custom/path/`
  - **Notes**: Existing option, unchanged

---

## Usage Examples

### Example 1: Generate Today's Reflection (Default)

```bash
# With reflections enabled (default)
# Ensure .env file has ANTHROPIC_API_KEY and ANTHROPIC_MAX_COST_PER_REFLECTION
catholic-liturgy-tools generate-readings

# Expected output:
# ✓ Fetching readings for 2025-11-30...
# ✓ Generating synopses (4 readings)...
# ✓ Generating reflection...
# ✓ Selecting prayer...
# ✓ Cost: $0.016 (within $0.04 limit)
# ✓ Generated: _site/readings/2025-11-30.html
```

### Example 2: Generate Without Reflections

```bash
# Disable AI-generated content
catholic-liturgy-tools generate-readings --no-reflections

# Expected output:
# ✓ Fetching readings for 2025-11-30...
# ✓ Generated: _site/readings/2025-11-30.html
```

### Example 3: Generate for Specific Date

```bash
# Generate for Christmas
catholic-liturgy-tools generate-readings --date 2025-12-25

# Expected output:
# ✓ Fetching readings for 2025-12-25...
# ✓ Detected feast: Solemnity of the Nativity of the Lord
# ✓ Generating synopses (4 readings)...
# ✓ Generating reflection...
# ✓ Selecting prayer (Christmas theme)...
# ✓ Cost: $0.018 (within $0.04 limit)
# ✓ Generated: _site/readings/2025-12-25.html
```

### Example 4: Custom Output Directory

```bash
# Generate to custom location
catholic-liturgy-tools generate-readings --output-dir /custom/path/

# Expected output:
# ✓ Fetching readings for 2025-11-30...
# ✓ Generating synopses (4 readings)...
# ✓ Generating reflection...
# ✓ Selecting prayer...
# ✓ Cost: $0.016 (within $0.04 limit)
# ✓ Generated: /custom/path/2025-11-30.html
```

---

## Error Handling

### Missing API Key

```bash
$ catholic-liturgy-tools generate-readings
✗ Error: Anthropic API key required. Set ANTHROPIC_API_KEY in .env file or environment.
```

**Exit Code**: 1  
**Resolution**: Add `ANTHROPIC_API_KEY=sk-ant-...` to `.env` file in project root

### Cost Exceeded

```bash
$ catholic-liturgy-tools generate-readings
✓ Fetching readings for 2025-11-30...
✓ Pre-flight cost estimate: $0.018
✓ Generating synopses (4 readings)...
✗ Warning: Cost exceeds limit ($0.045 > $0.04)
✓ Generated readings without AI content: _site/readings/2025-11-30.html
```

**Exit Code**: 0 (graceful degradation)  
**Behavior**: Falls back to readings-only output

### API Rate Limit

```bash
$ catholic-liturgy-tools generate-readings
✓ Fetching readings for 2025-11-30...
✓ Generating synopses (4 readings)...
✗ API Error: Rate limit exceeded. Retrying in 5 seconds...
✓ Retry successful
✓ Generating reflection...
[... continues normally ...]
```

**Exit Code**: 0 (automatic retry)  
**Behavior**: Exponential backoff with 3 retries

### Network Error

```bash
$ catholic-liturgy-tools generate-readings
✓ Fetching readings for 2025-11-30...
✗ Network Error: Unable to reach Anthropic API after 3 retries
✓ Generated readings without AI content: _site/readings/2025-11-30.html
```

**Exit Code**: 0 (graceful degradation)  
**Behavior**: Falls back to readings-only output

### Invalid Date

```bash
$ catholic-liturgy-tools generate-readings --date 2025-13-45
✗ Error: Invalid date format. Use YYYY-MM-DD.
```

**Exit Code**: 1  
**Resolution**: Provide valid date in YYYY-MM-DD format

---

## Environment Variables

### Required

- `ANTHROPIC_API_KEY`: Anthropic API key for Claude access
  - **Format**: `sk-ant-api03-...`
  - **Where to Get**: https://console.anthropic.com/
  - **Local Development**: Store in `.env` file (gitignored), never commit to repository
  - **GitHub Actions**: Set as repository secret or environment secret
  - **Security**: Never expose in logs or commit to version control

### Optional

- `ANTHROPIC_MAX_COST_PER_REFLECTION`: Maximum allowed cost per reflection
  - **Format**: Float (e.g., `0.04`)
  - **Default**: `0.04` if not set
  - **Local Development**: Set in `.env` file
  - **GitHub Actions**: Set as repository variable or environment variable
  - **Example**: `ANTHROPIC_MAX_COST_PER_REFLECTION=0.04`

---

## Exit Codes

| Code | Meaning | Scenarios |
|------|---------|-----------|
| 0 | Success | Reflection generated successfully, or graceful degradation to readings-only |
| 1 | Configuration Error | Missing API key, invalid date format, invalid options |
| 2 | Network Error (Fatal) | Cannot reach USCCB or API after all retries AND cannot degrade gracefully |

---

## Backward Compatibility

### Existing Behavior Preserved

```bash
# Old usage still works (no changes)
catholic-liturgy-tools generate-readings --date 2025-12-25 --output-dir _site/readings/

# New default behavior with reflections (requires .env configuration)
# To get old behavior, explicitly disable:
catholic-liturgy-tools generate-readings --no-reflections
```

### Migration Path

1. **Phase 1** (Current): `--with-reflections` enabled by default, users can opt-out with `--no-reflections`
2. **Phase 2** (Future): Consider making `--with-reflections` required explicit opt-in if users prefer simpler default

---

## Testing Checklist

- [ ] Generate with default options (today's date, with reflections)
- [ ] Generate with `--no-reflections` flag
- [ ] Generate for specific historical date (`--date 2024-01-01`)
- [ ] Generate for future date (within reason)
- [ ] Test missing API key error handling
- [ ] Test invalid API key error handling
- [ ] Test cost exceeded scenario (adjust ANTHROPIC_MAX_COST_PER_REFLECTION in .env)
- [ ] Test network error graceful degradation
- [ ] Test API rate limit retry logic
- [ ] Verify environment variable loading from .env file
- [ ] Verify GitHub Actions uses secrets correctly
- [ ] Test custom output directory with reflections
- [ ] Verify exit codes for all scenarios

---

## Implementation Notes

### CLI Framework

- Uses existing Click framework (already in use)
- Extend `cli.py` with new options
- Maintain existing option structure

### Option Defaults

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

@click.command()
@click.option('--with-reflections/--no-reflections', default=True, 
              help='Enable AI-generated reflection content')
@click.option('--date', type=click.DateTime(formats=['%Y-%m-%d']), 
              default=str(date.today()), help='Date to generate (YYYY-MM-DD)')
@click.option('--output-dir', default='_site/readings/', type=click.Path(),
              help='Output directory for generated HTML')
def generate_readings(with_reflections, date, output_dir):
    """Generate daily Mass readings with optional AI-augmented reflections."""
    # Load from environment (set in .env locally, GitHub secrets in Actions)
    api_key = os.getenv('ANTHROPIC_API_KEY')
    max_cost = float(os.getenv('ANTHROPIC_MAX_COST_PER_REFLECTION', '0.04'))
    
    if with_reflections and not api_key:
        raise click.ClickException(
            'Anthropic API key required. Set ANTHROPIC_API_KEY in .env file or environment.'
        )
    
    # Implementation continues...
```

### Dependency Injection

- Load environment variables using `python-dotenv` package
- Pass API key from environment to `AIClient` initialization
- Pass max cost from environment to `CostTracker` initialization
- Keep modules decoupled from CLI and environment loading
