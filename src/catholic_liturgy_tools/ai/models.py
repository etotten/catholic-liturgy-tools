"""Data models for AI-generated content."""

from dataclasses import dataclass
from typing import List


@dataclass
class ReadingSynopsis:
    """One-line AI-generated synopsis for a single Scripture reading."""

    reading_title: str
    synopsis_text: str
    tokens_used: int

    def __post_init__(self):
        """Validate synopsis data."""
        if not self.synopsis_text:
            raise ValueError("Synopsis text cannot be empty")
        if not self.reading_title:
            raise ValueError("Reading title cannot be empty")
        if self.tokens_used < 0:
            raise ValueError("Tokens used cannot be negative")


@dataclass
class CCCCitation:
    """Citation of the Catechism of the Catholic Church."""

    paragraph_number: int
    excerpt_text: str
    context_note: str = ""

    def __post_init__(self):
        """Validate CCC citation data."""
        if not 1 <= self.paragraph_number <= 2865:
            raise ValueError(
                f"CCC paragraph number must be 1-2865, got {self.paragraph_number}"
            )
        if not self.excerpt_text:
            raise ValueError("CCC excerpt text cannot be empty")


@dataclass
class DailyReflection:
    """Unified reflection synthesizing all readings for a day."""

    reflection_text: str
    pondering_questions: List[str]
    ccc_citations: List[CCCCitation]
    input_tokens: int
    output_tokens: int

    def __post_init__(self):
        """Validate reflection data."""
        if not self.reflection_text:
            raise ValueError("Reflection text cannot be empty")
        if len(self.pondering_questions) < 2:
            raise ValueError("Must have at least 2 pondering questions")
        for question in self.pondering_questions:
            if not question.endswith("?"):
                raise ValueError(f"Pondering question must end with '?': {question}")
        if not 1 <= len(self.ccc_citations) <= 2:
            raise ValueError("Must have 1-2 CCC citations")
        if self.input_tokens < 0 or self.output_tokens < 0:
            raise ValueError("Token counts cannot be negative")
