"""AI prompt templates for generating synopses and reflections."""

SYNOPSIS_SYSTEM_PROMPT = """You are a Catholic theologian and Scripture scholar assisting with liturgical reflection. 
Your task is to create concise, accessible summaries of Scripture readings that capture 
the core message in plain language suitable for a general audience.

Guidelines:
- Stay within the bounds of Catholic teaching
- Use simple, clear language (avoid theological jargon)
- Capture the reading's main theme in one sentence
- Length: 10-25 words maximum
- Maintain reverence and pastoral tone
- Do not add personal interpretation beyond the text's clear meaning

Your output must be valid JSON."""


def build_synopsis_user_prompt(reading_title: str, reading_text: str, citation: str) -> str:
    """Build user prompt for synopsis generation.
    
    Args:
        reading_title: Title of reading (e.g., "First Reading", "Gospel")
        reading_text: Full Scripture text
        citation: Biblical citation (e.g., "Isaiah 40:1-5")
        
    Returns:
        Formatted user prompt string
    """
    return f"""Reading Title: {reading_title}
Reading Text:
{reading_text}

Citation: {citation}

Task: Generate a one-line synopsis (10-25 words) that captures the core message of this reading.

Output as JSON:
{{
  "synopsis": "Your one-line summary here"
}}"""


REFLECTION_SYSTEM_PROMPT = """You are a Catholic theologian and spiritual director assisting with liturgical reflection. 
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

Your output must be valid JSON."""


def build_reflection_user_prompt(
    date_display: str,
    liturgical_day: str,
    feast_context: str,
    readings_list: str
) -> str:
    """Build user prompt for daily reflection generation.
    
    Args:
        date_display: Human-readable date (e.g., "Saturday, November 30, 2025")
        liturgical_day: Liturgical context (e.g., "Saturday of the Thirty-Fourth Week in Ordinary Time")
        feast_context: Optional feast day info (e.g., "Memorial of Saint Andrew, Apostle" or empty)
        readings_list: Formatted list of all readings with titles, citations, and full text
        
    Returns:
        Formatted user prompt string
    """
    feast_section = f"\nFeast Day: {feast_context}" if feast_context else ""
    
    return f"""Date: {date_display}
Liturgical Context: {liturgical_day}{feast_section}

Readings for the Day:

{readings_list}

Task: Generate a unified daily reflection that:
1. Synthesizes the themes across ALL readings
2. Helps readers apply God's Word to their lives
3. Includes 2-3 pondering questions (each ending with "?")
4. Cites 1-2 relevant CCC paragraphs (range: 1-2865) with brief excerpts
5. Maintains length of 300-500 words

Output as JSON:
{{
  "reflection_text": "Main reflection content (may include HTML <p> tags for paragraphs)",
  "pondering_questions": [
    "Question 1?",
    "Question 2?",
    "Question 3?"
  ],
  "ccc_citations": [
    {{
      "paragraph_number": 1234,
      "excerpt_text": "Brief quote or summary from CCC paragraph",
      "context_note": "How this teaching connects to today's readings"
    }}
  ]
}}"""


def format_readings_list(readings: list) -> str:
    """Format readings into a single string for the prompt.
    
    Args:
        readings: List of reading dictionaries with 'title', 'citation', and 'text' keys
        
    Returns:
        Formatted readings string
    """
    formatted = []
    for reading in readings:
        title = reading.get("title", "Reading")
        citation = reading.get("citation", "")
        text = reading.get("text", "")
        
        formatted.append(f"{title} - {citation}\n{text}")
    
    return "\n\n".join(formatted)
