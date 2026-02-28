# Contract: AI Prompt Templates

**Feature**: 005-daily-reflections  
**Purpose**: Define structured prompts for Anthropic Claude API to generate theologically accurate content

---

## Overview

All prompts use **multi-part structured format** with:
1. **System Prompt**: Sets theological constraints and role
2. **User Prompt**: Provides readings and specific task
3. **Output Format**: Specifies expected JSON structure

**Theological Constraints** (Applied to All Prompts):
- Stay within bounds of Catholic teaching
- Reference Scripture and Catechism appropriately
- Avoid personal interpretation or speculation
- Use accessible language for general audience
- Maintain reverence and pastoral tone

---

## Prompt 1: Synopsis Generation

**Purpose**: Generate one-line synopsis for a single Scripture reading

### System Prompt

```
You are a Catholic theologian and Scripture scholar assisting with liturgical reflection. 
Your task is to create concise, accessible summaries of Scripture readings that capture 
the core message in plain language suitable for a general audience.

Guidelines:
- Stay within the bounds of Catholic teaching
- Use simple, clear language (avoid theological jargon)
- Capture the reading's main theme in one sentence
- Length: 10-25 words maximum
- Maintain reverence and pastoral tone
- Do not add personal interpretation beyond the text's clear meaning

Your output must be valid JSON.
```

### User Prompt Template

```
Reading Title: {reading_title}
Reading Text:
{reading_text}

Citation: {citation}

Task: Generate a one-line synopsis (10-25 words) that captures the core message of this reading.

Output as JSON:
{
  "synopsis": "Your one-line summary here"
}
```

### Expected Output Format

```json
{
  "synopsis": "God calls us to trust in His providence even in times of uncertainty."
}
```

### Variables

- `{reading_title}`: String - Title of reading (e.g., "First Reading", "Gospel")
- `{reading_text}`: String - Full Scripture text
- `{citation}`: String - Biblical citation (e.g., "Isaiah 40:1-5")

### Example

**Input**:
```
Reading Title: First Reading
Reading Text: 
Comfort, give comfort to my people, says your God. Speak tenderly to Jerusalem, 
and proclaim to her that her service is at an end, her guilt is expiated; 
Indeed, she has received from the hand of the LORD double for all her sins.

Citation: Isaiah 40:1-5
```

**Output**:
```json
{
  "synopsis": "God offers comfort and forgiveness, proclaiming that Jerusalem's time of suffering has ended."
}
```

---

## Prompt 2: Daily Reflection Generation

**Purpose**: Generate unified reflection synthesizing all readings with pondering questions and CCC citations

### System Prompt

```
You are a Catholic theologian and spiritual director assisting with liturgical reflection. 
Your task is to create a unified reflection that synthesizes the day's Scripture readings, 
helping readers encounter God's Word in their daily lives.

Guidelines:
- Stay within the bounds of Catholic teaching
- Synthesize ALL readings into a coherent reflection (do not treat separately)
- Use accessible language suitable for adults seeking spiritual growth
- Include 2-3 pondering questions for personal meditation
- Cite 1-2 relevant paragraphs from the Catechism of the Catholic Church (CCC)
- All CCC citations must be in the range 1-2865
- Length: 300-500 words for reflection text
- Maintain reverence, warmth, and pastoral encouragement
- Connect Scripture to contemporary Christian life

Your output must be valid JSON.
```

### User Prompt Template

```
Date: {date_display}
Liturgical Context: {liturgical_day}
{feast_context}

Readings for the Day:

{readings_list}

Task: Generate a unified daily reflection that:
1. Synthesizes the themes across ALL readings
2. Helps readers apply God's Word to their lives
3. Includes 2-3 pondering questions (each ending with "?")
4. Cites 1-2 relevant CCC paragraphs (range: 1-2865) with brief excerpts
5. Maintains length of 300-500 words

Output as JSON:
{
  "reflection_text": "Main reflection content (may include HTML <p> tags for paragraphs)",
  "pondering_questions": [
    "Question 1?",
    "Question 2?",
    "Question 3?"
  ],
  "ccc_citations": [
    {
      "paragraph_number": 1234,
      "excerpt_text": "Brief quote or summary from CCC paragraph",
      "context_note": "How this teaching connects to today's readings"
    }
  ]
}
```

### Expected Output Format

```json
{
  "reflection_text": "<p>Today's readings invite us to consider the mystery of God's mercy...</p><p>In the First Reading, Isaiah proclaims comfort to a weary people...</p>",
  "pondering_questions": [
    "How does God's call to comfort challenge me today?",
    "Where in my life do I need to trust more fully in God's providence?",
    "What does it mean for me to speak tenderly to others as God speaks to Jerusalem?"
  ],
  "ccc_citations": [
    {
      "paragraph_number": 2558,
      "excerpt_text": "Prayer is the raising of one's mind and heart to God or the requesting of good things from God.",
      "context_note": "This teaching connects to today's Gospel call to persistent prayer and trust in God's loving care."
    },
    {
      "paragraph_number": 1427,
      "excerpt_text": "Jesus calls to conversion... This call is an essential part of the proclamation of the kingdom.",
      "context_note": "Isaiah's message of comfort includes a call to turn back to God, echoing Jesus' call to conversion."
    }
  ]
}
```

### Variables

- `{date_display}`: String - Human-readable date (e.g., "Saturday, November 30, 2025")
- `{liturgical_day}`: String - Liturgical context (e.g., "Saturday of the Thirty-Fourth Week in Ordinary Time")
- `{feast_context}`: String - Optional feast day info (e.g., "Memorial of Saint Andrew, Apostle" or empty string)
- `{readings_list}`: String - Formatted list of all readings with titles, citations, and full text

### Example readings_list Format

```
First Reading - Isaiah 40:1-5
Comfort, give comfort to my people, says your God...

Responsorial Psalm - Psalm 23:1-3a, 3b-4, 5, 6
The LORD is my shepherd; I shall not want...

Gospel - Matthew 11:28-30
Come to me, all you who labor and are burdened, and I will give you rest...
```

---

## Prompt 3: CCC Validation (Reference)

**Purpose**: Validate that CCC citations are within acceptable range

**Note**: This is NOT an AI prompt, but a validation step performed programmatically.

### Validation Rules

1. **Range Check**: Paragraph number must be 1 ≤ n ≤ 2865
2. **Format Check**: Paragraph number must be an integer
3. **Optional HTTP Check**: Verify URL `https://www.vatican.va/archive/ENG0015/__P{paragraph_number}.HTM` returns 200 OK

### Error Handling

- **Out of Range**: Log warning, retry generation with explicit constraint reminder
- **HTTP Failure**: Log warning, accept citation (offline tolerance)
- **Format Error**: Reject citation, retry generation

---

## Prompt Engineering Best Practices

### 1. Explicit Constraints

Always include explicit boundaries in system prompts:
- CCC range: 1-2865
- Word count limits
- Required JSON structure
- Theological guardrails

### 2. Output Format Specification

Provide exact JSON schema in user prompt to ensure structured output:
```json
{
  "field_name": "Description of expected content"
}
```

### 3. Example-Based Guidance

Include examples in system prompts when introducing new concepts (e.g., "pondering questions" format)

### 4. Retry Strategy

If output doesn't match schema or violates constraints:
1. Parse error message
2. Add specific correction to prompt ("Previous output had issue X, please ensure Y")
3. Retry with modified prompt
4. Maximum 3 retries per generation

### 5. Temperature Settings

- **Synopsis Generation**: `temperature=0.3` (more deterministic, factual)
- **Reflection Generation**: `temperature=0.5` (balanced creativity and consistency)

---

## Token Estimation

### Synopsis Prompt (Per Reading)

- System prompt: ~200 tokens
- User prompt base: ~50 tokens
- Reading text: ~300-800 tokens (varies)
- Output: ~20-30 tokens
- **Total per reading**: ~570-1080 tokens

### Reflection Prompt

- System prompt: ~250 tokens
- User prompt base: ~100 tokens
- Readings list: ~1200-2000 tokens (3-4 readings)
- Output: ~400-500 tokens
- **Total per reflection**: ~1950-2850 tokens

### Daily Total Estimate

- 4 synopses: 4 × 700 = ~2800 tokens
- 1 reflection: ~2400 tokens
- **Total**: ~5200 tokens (input + output)
- **Estimated cost**: ~$0.016 at current Anthropic pricing

---

## Error Messages and Recovery

### Invalid JSON Output

```
Error: AI returned invalid JSON. Retrying with format reminder...
```

**Recovery**: Retry with additional prompt:
```
Previous output was not valid JSON. Please ensure your response is ONLY valid JSON 
with no additional text before or after the JSON object.
```

### CCC Citation Out of Range

```
Error: CCC citation 3500 exceeds maximum (2865). Retrying with constraint reminder...
```

**Recovery**: Retry with additional prompt:
```
Previous output included invalid CCC citation (out of range 1-2865). 
Please ensure all CCC paragraph numbers are between 1 and 2865.
```

### Pondering Questions Missing "?"

```
Error: Pondering questions must end with "?". Retrying...
```

**Recovery**: Retry with additional prompt:
```
Previous output had pondering questions without question marks. 
Please ensure all pondering questions end with "?".
```

---

## Testing Prompts

### Test Cases

1. **Basic Weekday**: Ordinary time, 3 readings, no feast
2. **Sunday**: 4 readings including Gospel
3. **Saint's Day**: Memorial with feast day context
4. **Solemnity**: Major feast (e.g., Christmas, Easter)
5. **Edge Case**: Very long readings (test token limits)

### Validation Checklist

- [ ] Synopsis within word count (10-25 words)
- [ ] Reflection within word count (300-500 words)
- [ ] 2-3 pondering questions present
- [ ] All questions end with "?"
- [ ] 1-2 CCC citations present
- [ ] All CCC citations in range 1-2865
- [ ] Valid JSON structure
- [ ] No theological errors or speculation
- [ ] Accessible language for general audience
- [ ] Pastoral and reverent tone

---

## Implementation Notes

### Claude Model Selection

- **Model**: `claude-3-5-sonnet-20241022` (or latest)
- **Rationale**: Balance of quality, speed, and cost
- **Alternative**: `claude-3-opus` for higher quality (if needed)

### API Parameters

```python
{
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 1000,  # Synopsis: 50, Reflection: 1000
    "temperature": 0.3,  # Synopsis: 0.3, Reflection: 0.5
    "system": "System prompt text...",
    "messages": [
        {"role": "user", "content": "User prompt text..."}
    ]
}
```

### Prompt Storage

- Store prompts as constants in `ai/prompts.py`
- Use Python f-strings for variable interpolation
- Version prompts if major changes needed (e.g., `SYNOPSIS_PROMPT_V1`)
