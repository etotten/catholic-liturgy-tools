# Quick Start Guide: Daily Reflections with AI

**Feature**: 005-daily-reflections  
**Purpose**: Get up and running with AI-augmented daily reflections in 5 minutes

---

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git (optional, for cloning repository)
- Anthropic API account and key

---

## 1. Installation

### Clone Repository

```bash
git clone https://github.com/etotten/catholic-liturgy-tools.git
cd catholic-liturgy-tools
```

### Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package in editable mode
pip install -e .
```

---

## 2. Get Anthropic API Key

### Sign Up for Anthropic Account

1. Visit https://console.anthropic.com/
2. Create an account (or sign in)
3. Navigate to "API Keys" section
4. Click "Create Key"
5. Copy your API key (starts with `sk-ant-api03-...`)

### Set Environment Variables

**Create `.env` file in project root** (recommended for local development)

```bash
# In project root directory
cat > .env << EOF
ANTHROPIC_API_KEY=sk-ant-api03-YOUR-KEY-HERE
ANTHROPIC_MAX_COST_PER_REFLECTION=0.04
EOF
```

**For GitHub Actions**: Set as repository secrets
1. Go to repository Settings → Secrets and variables → Actions
2. Add `ANTHROPIC_API_KEY` as a secret
3. Add `ANTHROPIC_MAX_COST_PER_REFLECTION` as a variable (or secret)

**Note**: The `.env` file is gitignored and will never be committed to version control.

---

## 3. Generate Your First Reflection

### Basic Usage (Today's Date)

```bash
catholic-liturgy-tools generate-readings
```

**Expected output:**
```
✓ Fetching readings for 2025-11-30...
✓ Generating synopses (4 readings)...
✓ Generating reflection...
✓ Selecting prayer...
✓ Cost: $0.016 (within $0.04 limit)
✓ Generated: _site/readings/2025-11-30.html
```

### View the Output

```bash
# Open in browser (macOS)
open _site/readings/2025-11-30.html

# Open in browser (Linux)
xdg-open _site/readings/2025-11-30.html

# Open in browser (Windows)
start _site/readings/2025-11-30.html
```

---

## 4. Understanding the Output

### HTML Structure

The generated HTML file includes:

1. **Daily Readings**: Full Scripture texts (existing feature)
2. **Reading Synopses**: One-line summaries for each reading (NEW)
3. **Opening Prayer**: Contextual Catholic prayer (NEW)
4. **Daily Reflection**: Unified reflection with pondering questions (NEW)
5. **CCC Citations**: References to Catechism paragraphs (NEW)
6. **Feast Day Info**: Saint biography or solemnity description (NEW, when applicable)

### Example Reflection Section

```html
<div class="reflection">
  <h2>Daily Reflection</h2>
  <p>Today's readings invite us to consider the mystery of God's mercy...</p>
  
  <h3>Pondering Questions</h3>
  <ul>
    <li>How does God's call to comfort challenge me today?</li>
    <li>Where in my life do I need to trust more fully?</li>
  </ul>
  
  <h3>From the Catechism</h3>
  <blockquote>
    <p><strong>CCC 2558:</strong> Prayer is the raising of one's mind and heart to God...</p>
  </blockquote>
</div>
```

---

## 5. Common Use Cases

### Generate for Specific Date

```bash
# Generate for Christmas
catholic-liturgy-tools generate-readings --date 2025-12-25
```

### Generate Without Reflections

```bash
# Revert to old behavior (readings only, no AI content)
catholic-liturgy-tools generate-readings --no-reflections
```

### Custom Output Directory

```bash
# Save to custom directory
catholic-liturgy-tools generate-readings --output-dir /custom/path/
```

### Adjust Cost Limit

```bash
# Edit .env file to change cost limit
echo "ANTHROPIC_MAX_COST_PER_REFLECTION=0.10" >> .env
catholic-liturgy-tools generate-readings
```

---

## 6. Scheduled Daily Generation

### Using Cron (Linux/macOS)

Generate automatically every day at 6:00 AM CT:

```bash
# Edit crontab
crontab -e

# Add this line (adjust path to your installation)
0 12 * * * cd /path/to/catholic-liturgy-tools && /path/to/venv/bin/catholic-liturgy-tools generate-readings
```

**Note**: `0 12 * * *` = 12:00 PM UTC = 6:00 AM CST (7:00 AM CDT)

### Using GitHub Actions

See `.github/workflows/publish-site.yml` for automated deployment configuration.

---

## 7. Troubleshooting

### Error: "Anthropic API key required"

**Solution**: Set `ANTHROPIC_API_KEY` environment variable

```bash
export ANTHROPIC_API_KEY=sk-ant-api03-YOUR-KEY-HERE
```

### Error: "Cost exceeds limit"

**Output**:
```
✗ Warning: Cost exceeds limit ($0.045 > $0.04)
✓ Generated readings without AI content: _site/readings/2025-11-30.html
```

**Solution**: Increase cost limit in `.env` file or accept readings-only output

```bash
# Edit .env file
echo "ANTHROPIC_MAX_COST_PER_REFLECTION=0.10" >> .env
# Then re-run
catholic-liturgy-tools generate-readings
```

### Error: "API Rate Limit Exceeded"

**Output**:
```
✗ API Error: Rate limit exceeded. Retrying in 5 seconds...
```

**Solution**: Wait for automatic retry (up to 3 attempts with exponential backoff)

### Error: "Network Error"

**Output**:
```
✗ Network Error: Unable to reach Anthropic API after 3 retries
✓ Generated readings without AI content: _site/readings/2025-11-30.html
```

**Solution**: Check internet connection, API status at https://status.anthropic.com/

---

## 8. Configuration Options

### Environment Variables

| Variable | Description | Default | Where to Set |
|----------|-------------|---------|-------------|
| `ANTHROPIC_API_KEY` | Anthropic API key | (required) | `.env` (local), GitHub secret (Actions) |
| `ANTHROPIC_MAX_COST_PER_REFLECTION` | Max cost per reflection | `0.04` | `.env` (local), GitHub variable (Actions) |

### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--with-reflections` | Enable AI-generated content | Enabled |
| `--no-reflections` | Disable AI-generated content | - |
| `--date` | Date to generate (YYYY-MM-DD) | Today |
| `--output-dir` | Output directory | `_site/readings/` |

---

## 9. Cost Estimation

### Typical Costs (per reflection)

- **Weekday** (3 readings): ~$0.014
- **Sunday** (4 readings): ~$0.018
- **Feast Day** (4 readings + feast info): ~$0.020

### Monthly Estimate

- 30 days × $0.016 average = **~$0.48/month**
- At $0.04 limit = **~$1.20/month maximum**

### Annual Estimate

- 365 days × $0.016 average = **~$5.84/year**
- At $0.04 limit = **~$14.60/year maximum**

---

## 10. Next Steps

### Customize Configuration

**Adjust Cost Limit**: Edit `.env` file
```bash
ANTHROPIC_MAX_COST_PER_REFLECTION=0.10
```

**Customize Prayer Database**: Edit `data/prayers.json` to add your own curated prayers

```json
{
  "id": "my-custom-prayer",
  "title": "My Prayer",
  "text": "Prayer text here...",
  "source": "USCCB",
  "source_url": "https://...",
  "liturgical_contexts": ["all"],
  "language": "en"
}
```

See `contracts/prayer-database-schema.md` for full schema.

### Integrate with Website

Deploy generated HTML files to your static site:

```bash
# Generate all readings
catholic-liturgy-tools generate-readings

# Deploy to GitHub Pages (if configured)
git add _site/
git commit -m "Update daily reflections"
git push
```

### Run Tests

Verify everything works:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=catholic_liturgy_tools --cov-report=html
```

---

## 11. Getting Help

### Documentation

- **Specification**: `specs/005-daily-reflections/spec.md`
- **Implementation Plan**: `specs/005-daily-reflections/plan.md`
- **Research**: `specs/005-daily-reflections/research.md`
- **Contracts**: `specs/005-daily-reflections/contracts/`

### Support

- **Issues**: https://github.com/etotten/catholic-liturgy-tools/issues
- **Email**: [your-email@example.com]

---

## Quick Reference Card

```bash
# Setup (one-time)
cat > .env << EOF
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MAX_COST_PER_REFLECTION=0.04
EOF

# Generate today's reflection
catholic-liturgy-tools generate-readings

# Generate for specific date
catholic-liturgy-tools generate-readings --date 2025-12-25

# Generate without AI content
catholic-liturgy-tools generate-readings --no-reflections

# View output
open _site/readings/$(date +%Y-%m-%d).html
```

---

**That's it! You're ready to generate AI-augmented daily reflections.** 🎉
