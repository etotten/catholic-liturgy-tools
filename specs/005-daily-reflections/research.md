# Research: Daily Reflections with AI-Augmented Content

**Feature**: 005-daily-reflections  
**Date**: November 30, 2025  
**Purpose**: Resolve technical unknowns and establish implementation approach

## Research Tasks

This document resolves all "NEEDS CLARIFICATION" items from the Technical Context section of [plan.md](./plan.md).

---

## 1. Anthropic SDK Integration

**Unknown**: Best practices for Anthropic Claude API integration - version, initialization pattern, error handling

### Decision: Use Anthropic Python SDK 0.8.0+

**Rationale**:
- Official SDK provides type-safe interface and automatic retries
- Handles authentication, rate limiting, and error responses
- Supports streaming responses (if needed for long reflections)
- Well-documented and maintained by Anthropic

**Installation**:
```python
# pyproject.toml
anthropic = "^0.8.0"
python-dotenv = "^1.0.0"  # For .env file management
```

**Initialization Pattern**:
```python
from anthropic import Anthropic, AnthropicError
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file for local development

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),  # From .env or environment
    timeout=60.0,  # 60 second timeout per request
)
```

**Error Handling**:
- `AnthropicError`: Base exception for all API errors
- `APIConnectionError`: Network/connection failures
- `APIStatusError`: HTTP errors (rate limiting, invalid requests)
- `RateLimitError`: Specific rate limit exceptions

**Cost Tracking**:
- Response object includes `usage` attribute with `input_tokens` and `output_tokens`
- Track per-request and aggregate for $0.04 limit enforcement

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| Direct HTTP requests | More complex, no automatic retry/error handling |
| LangChain wrapper | Unnecessary abstraction for simple use case |

---

## 2. Prayer Sourcing Strategy

**Unknown**: How to programmatically source prayers from multiple Catholic websites (USCCB, Vatican, Catholic Online, EWTN, Loyola Press)

### Decision: Curated Prayer Database (AI-Assisted with Human Approval)

**Rationale**:
- Web scraping 5 different sites daily is fragile (HTML structure changes)
- Copyright concerns with automated scraping
- No unified API across these Catholic sites
- Prayers are relatively static content - reusable across liturgical cycles
- Quality control: human review ensures appropriate prayers

**Implementation Approach (AI-Assisted Curation)**:
1. AI finds prayers from 5 approved sources during implementation
2. AI creates `data/prayers.json` following schema
3. **Exclude commonly memorized prayers** (Hail Mary, Our Father, Glory Be, etc.)
4. **Focus on lesser-known prayers** that enrich spiritual life with new content
5. Human reviews prayers in pull request/branch
6. Human commits to repository = approval
7. Human can request AI to replace any unsuitable prayers
8. Prayer selection algorithm matches date context to appropriate prayer
9. Each entry includes: prayer text, attribution, source URL

**Prayer Database Schema**:
```json
{
  "advent_prayers": [...],
  "christmas_prayers": [...],
  "lent_prayers": [...],
  "easter_prayers": [...],
  "ordinary_time_prayers": [...],
  "feast_day_prayers": {
    "saints": [...],
    "solemnities": [...]
  },
  "gospel_theme_prayers": {
    "mercy": [...],
    "discipleship": [...],
    "prayer": [...]
  }
}
```

**Fallback Strategy**:
- Default prayer: Traditional "Prayer before reading Scripture"
- Graceful degradation if no matching prayer found

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| Web scraping daily | Fragile, copyright issues, maintenance burden |
| Single prayer source API | No comprehensive Catholic prayer API exists |
| AI-generated prayers | Explicitly rejected by user (FR-006) |

---

## 3. Liturgical Calendar Data

**Unknown**: Reliable source for liturgical calendar data (feast days, solemnities, saint information)

### Decision: Romcal NPM Package + Python Wrapper

**Rationale**:
- `romcal` is authoritative liturgical calendar library
- Maintained by Catholic developers, follows Roman Calendar
- Provides feast rankings, saint information, liturgical seasons
- Can be called from Python via subprocess or through a thin wrapper

**Installation & Usage**:
```bash
# Install romcal globally or in project
npm install romcal
```

```python
import subprocess
import json
from datetime import date

def get_liturgical_day(target_date: date) -> dict:
    """Get liturgical calendar info using romcal"""
    result = subprocess.run(
        ["node", "-e", f"const romcal = require('romcal'); console.log(JSON.stringify(romcal.calendarFor({target_date.year}).get('{target_date.isoformat()}')))"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)
```

**Data Provided by Romcal**:
- Liturgical day name
- Feast rank (solemnity, feast, memorial, optional memorial)
- Liturgical season (Advent, Christmas, Lent, Easter, Ordinary Time)
- Saint information (if applicable)
- Liturgical color

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| Manual calendar file | High maintenance, error-prone, incomplete |
| Catholic calendar API | No free, reliable API with comprehensive data |
| Parse from USCCB page | Incomplete saint biographies, no structured data |

**Note**: For saint biographies, will need to supplement romcal with additional sources (Catholic Online, EWTN saint database).

---

## 4. CCC Validation

**Unknown**: How to validate CCC paragraph references (1-2865) against Vatican's official Catechism

### Decision: Simple Range Validation + Optional Scraping Verification

**Rationale**:
- CCC has exactly 2865 numbered paragraphs
- Paragraph numbers are stable and won't change
- Simple range check (1 ≤ n ≤ 2865) handles 99% of validation
- Optional: verify against Vatican website for paranoid checking

**Implementation**:

**Tier 1 - Range Validation (Always)**:
```python
def validate_ccc_paragraph(paragraph_num: int) -> bool:
    """Validate CCC paragraph is in valid range"""
    return 1 <= paragraph_num <= 2865
```

**Tier 2 - Vatican Website Verification (Optional)**:
```python
def verify_ccc_paragraph_exists(paragraph_num: int) -> bool:
    """Verify paragraph exists on Vatican's official CCC website"""
    url = f"https://www.vatican.va/archive/ENG0015/_P{paragraph_num:X}.HTM"
    response = requests.head(url, timeout=10)
    return response.status_code == 200
```

**Usage Strategy**:
- Always use Tier 1 validation
- Tier 2 verification only if suspicious (e.g., AI consistently suggests same invalid numbers)
- Cache verified paragraphs to avoid repeated HTTP requests

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| Local CCC database | Overkill for simple validation, storage overhead |
| Always verify via HTTP | Slow, unnecessary for valid range |
| No validation | Risk of invalid references slipping through |

---

## 5. AI Prompt Engineering for Theological Accuracy

**Unknown**: Best practices for crafting AI prompts that ensure orthodox Catholic teaching

### Decision: Multi-Part Prompt Strategy with Explicit Constraints

**Rationale**:
- Claude excels at following detailed instructions
- Explicit theological guardrails in system prompt
- Structured output format ensures consistency
- CCC references provide grounding in official Church teaching

**Prompt Structure**:

**System Prompt (All Requests)**:
```
You are a Catholic theologian and spiritual director helping Catholics deepen their understanding of Scripture. Your reflections must:

1. Be faithful to orthodox Catholic teaching as found in the Catechism of the Catholic Church
2. Avoid personal theological opinions or speculative interpretations
3. Ground reflections in Sacred Scripture and Church Tradition
4. Present Church teaching with clarity and reverence
5. Encourage personal prayer and application to daily life

When citing the Catechism, use only paragraph numbers between 1 and 2865. Ensure all references are accurate and relevant to the Scripture readings.
```

**Synopsis Generation Prompt**:
```
Provide a one-line synopsis (max 20 words) of the following Scripture reading. Focus on the core message that would help a Catholic preparing for Mass understand the reading's main point:

[Scripture text]

Respond with only the synopsis, no additional commentary.
```

**Reflection Generation Prompt**:
```
Generate a Catholic reflection on today's liturgical readings. The reflection should:

1. Synthesize the common themes across all readings (First Reading, Psalm, Second Reading if present, Gospel)
2. Include 2-3 questions for personal pondering that connect the readings to daily spiritual life
3. Cite 1-2 relevant paragraphs from the Catechism of the Catholic Church (CCC) that illuminate the readings
4. Be approximately 300-400 words
5. Maintain a tone of reverence and encouragement

Today's Readings:
- First Reading: [title and text]
- Responsorial Psalm: [title and text]
- [Second Reading if applicable]
- Gospel: [title and text]

Format your response as:
## Daily Reflection
[reflection paragraph(s)]

## Questions for Pondering
1. [question]
2. [question]
3. [question]

## From the Catechism
CCC [number]: [brief quote or summary]
CCC [number]: [brief quote or summary]
```

**Validation Steps**:
1. Parse AI response for CCC paragraph numbers
2. Validate each number is in range 1-2865
3. If invalid, retry with explicit correction
4. Log any persistent invalid references for prompt refinement

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| Generic prompts | Risk of theologically inaccurate output |
| Chain-of-thought prompting | Unnecessary complexity for this use case |
| Multiple AI calls for validation | Expensive, slower, diminishing returns |

---

## 6. Cost Tracking Implementation

**Unknown**: How to accurately track API costs and enforce $0.04 per reflection limit

### Decision: Token-Based Tracking with Pre-Flight Estimation

**Rationale**:
- Anthropic API returns exact token counts in response
- Can estimate input tokens before sending request
- Enforce limit before generating reflection (fail-fast)
- Track costs per date for reporting and budgeting

**Implementation**:

```python
class CostTracker:
    # Pricing as of Nov 2025 (Claude 3.5 Sonnet)
    INPUT_COST_PER_MILLION = 3.00
    OUTPUT_COST_PER_MILLION = 15.00
    MAX_COST_PER_REFLECTION = 0.04
    
    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
    
    def estimate_input_tokens(self, text: str) -> int:
        """Rough estimate: ~0.75 tokens per word"""
        return int(len(text.split()) * 0.75)
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost in dollars"""
        input_cost = (input_tokens / 1_000_000) * self.INPUT_COST_PER_MILLION
        output_cost = (output_tokens / 1_000_000) * self.OUTPUT_COST_PER_MILLION
        return input_cost + output_cost
    
    def can_afford_request(self, estimated_input_tokens: int, 
                           estimated_output_tokens: int) -> bool:
        """Check if request would exceed budget"""
        estimated_cost = self.calculate_cost(
            self.total_input_tokens + estimated_input_tokens,
            self.total_output_tokens + estimated_output_tokens
        )
        return estimated_cost < self.MAX_COST_PER_REFLECTION
    
    def record_usage(self, input_tokens: int, output_tokens: int):
        """Record actual usage from API response"""
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
    
    def get_total_cost(self) -> float:
        """Get total cost for this reflection"""
        return self.calculate_cost(self.total_input_tokens, self.total_output_tokens)
```

**Usage Pattern**:
1. Initialize CostTracker per reflection
2. Estimate tokens for each API call before sending
3. Check `can_afford_request()` - fail if false
4. After API response, call `record_usage()` with actual tokens
5. Log final cost with `get_total_cost()`

**Cost Monitoring**:
- Log costs to file per date for analysis
- Alert if consistently approaching limit (>$0.035)
- Monthly report of total costs

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| Post-hoc cost tracking | Can't prevent overages, only detect them |
| No cost tracking | Risk of budget overruns, no visibility |
| External cost monitoring service | Unnecessary complexity, privacy concerns |

---

## 7. GitHub Actions Scheduling

**Unknown**: How to configure GitHub Actions for 6:00 AM Central Time daily execution

### Decision: Cron Expression with UTC Conversion

**Rationale**:
- GitHub Actions uses UTC time zone
- Central Time is UTC-6 (CST) or UTC-5 (CDT)
- Use UTC time to ensure consistent scheduling
- Account for daylight saving time

**Implementation**:

```yaml
# .github/workflows/publish-site.yml
name: Generate and Publish Daily Content

on:
  schedule:
    # 6:00 AM Central = 12:00 PM UTC (CST) or 11:00 AM UTC (CDT)
    # Using 12:00 PM UTC as baseline (works for CST, 1 hour off during CDT)
    - cron: '0 12 * * *'
  workflow_dispatch:  # Allow manual triggers

jobs:
  generate-and-publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -e .
      
      - name: Generate today's reflection
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          ANTHROPIC_MAX_COST_PER_REFLECTION: ${{ vars.ANTHROPIC_MAX_COST_PER_REFLECTION || '0.04' }}
        run: |
          catholic-liturgy generate-readings --date $(date +%Y-%m-%d)
      
      # [Additional steps for index generation and publishing]
```

**Considerations**:
- **CST (Nov-Mar)**: 6:00 AM CST = 12:00 PM UTC ✓
- **CDT (Mar-Nov)**: 6:00 AM CDT = 11:00 AM UTC (1 hour off)
- **Decision**: Use 12:00 PM UTC (CST time). During CDT, content generates at 7:00 AM local time (acceptable)
- **Alternative**: Use 11:00 AM UTC (CDT time), 5:00 AM during CST (less ideal)

**Secrets and Variables Configuration**:
- Add `ANTHROPIC_API_KEY` to GitHub repository secrets (sensitive)
- Add `ANTHROPIC_MAX_COST_PER_REFLECTION` to GitHub repository variables (or use default 0.04)
- Access via `${{ secrets.ANTHROPIC_API_KEY }}` and `${{ vars.ANTHROPIC_MAX_COST_PER_REFLECTION }}` in workflow

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| Timezone-aware cron | GitHub Actions doesn't support timezone specification |
| External scheduler (cron job on server) | Adds infrastructure complexity |
| 12:00 PM UTC year-round | Chosen approach - simple, predictable |

---

## Summary of Decisions

| Unknown | Decision | Key Dependencies |
|---------|----------|------------------|
| Anthropic SDK | Official Python SDK 0.8.0+ | `anthropic` package |
| Prayer Sourcing | Curated JSON database | Manual curation effort |
| Liturgical Calendar | Romcal NPM package + Python wrapper | Node.js, `romcal` package |
| CCC Validation | Range validation (1-2865) + optional HTTP verify | None (or `requests` for Tier 2) |
| AI Prompts | Multi-part structured prompts with theological constraints | Prompt templates in code |
| Cost Tracking | Token-based tracking with pre-flight estimation | Built-in to Anthropic SDK |
| GitHub Actions | Cron at 12:00 PM UTC (6am CST) | GitHub Actions, secrets |

**Next Steps**: Proceed to Phase 1 (Data Model & Contracts) with these technical decisions established.
