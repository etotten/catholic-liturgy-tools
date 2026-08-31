"""Anthropic API client for generating synopses and reflections."""

import json
import os
from typing import Optional

from anthropic import Anthropic
from dotenv import load_dotenv

from .cost_tracker import CostTracker
from .models import CCCCitation, DailyReflection, ReadingSynopsis
from .prompts import (
    REFLECTION_SYSTEM_PROMPT,
    SYNOPSIS_SYSTEM_PROMPT,
    build_reflection_user_prompt,
    build_synopsis_user_prompt,
)

# Load environment variables
load_dotenv()


class AnthropicClient:
    """Wrapper for Anthropic API to generate Catholic liturgical content."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        max_cost_per_reflection: float = 0.04,
        model: str = "claude-3-5-sonnet-20241022"
    ):
        """Initialize Anthropic client.
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            max_cost_per_reflection: Maximum cost per reflection in USD
            model: Claude model to use
            
        Raises:
            ValueError: If API key is not provided or found in environment
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key required. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = model
        self.cost_tracker = CostTracker(max_cost_usd=max_cost_per_reflection)

    def generate_synopsis(
        self, reading_title: str, reading_text: str, citation: str
    ) -> ReadingSynopsis:
        """Generate one-line synopsis for a Scripture reading.
        
        Args:
            reading_title: Title of reading (e.g., "First Reading", "Gospel")
            reading_text: Full Scripture text
            citation: Biblical citation (e.g., "Isaiah 40:1-5")
            
        Returns:
            ReadingSynopsis object
            
        Raises:
            ValueError: If reading_text is empty, citation is invalid/empty, 
                       API cost limit exceeded, or response invalid
        """
        # Validate inputs
        if not reading_text or not reading_text.strip():
            raise ValueError("reading_text cannot be empty")
        if not citation or not citation.strip():
            raise ValueError("citation must be in format 'Book Chapter:Verse-Verse'")
        
        user_prompt = build_synopsis_user_prompt(reading_title, reading_text, citation)
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=100,
            system=SYNOPSIS_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}]
        )
        
        # Extract token usage
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        
        # Record cost (will raise if exceeds limit)
        self.cost_tracker.record_call("synopsis", input_tokens, output_tokens)
        
        # Parse response
        response_text = response.content[0].text
        try:
            data = json.loads(response_text)
            synopsis_text = data.get("synopsis", "").strip()
            if not synopsis_text:
                raise ValueError("Empty synopsis in response")
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise ValueError(f"Invalid API response: {e}\nResponse: {response_text}")
        
        return ReadingSynopsis(
            reading_title=reading_title,
            synopsis_text=synopsis_text,
            tokens_used=output_tokens
        )

    def generate_reflection(
        self,
        date_display: str,
        liturgical_day: str,
        feast_context: Optional[str],
        readings: list,
        max_retries: int = 3
    ) -> DailyReflection:
        """Generate unified daily reflection with CCC citations.
        
        Args:
            date_display: Human-readable date
            liturgical_day: Liturgical context
            feast_context: Optional feast day info object or None
            readings: List of reading dicts with 'title', 'citation', 'text'
            max_retries: Maximum retries for invalid CCC citations
            
        Returns:
            DailyReflection object
            
        Raises:
            ValueError: If API cost limit exceeded, retries exhausted, or response invalid
        """
        user_prompt = build_reflection_user_prompt(
            date_display, liturgical_day, feast_context, readings
        )
        
        for attempt in range(max_retries):
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                system=REFLECTION_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            # Extract token usage
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            
            # Record cost (will raise if exceeds limit)
            self.cost_tracker.record_call("reflection", input_tokens, output_tokens)
            
            # Parse response
            response_text = response.content[0].text
            try:
                data = json.loads(response_text)
                
                # Extract and validate CCC citations
                ccc_citations = []
                for cit_data in data.get("ccc_citations", []):
                    citation = CCCCitation(
                        paragraph_number=cit_data["paragraph_number"],
                        excerpt_text=cit_data["excerpt_text"],
                        context_note=cit_data.get("context_note", "")
                    )
                    ccc_citations.append(citation)
                
                # Build DailyReflection (validation happens in __post_init__)
                reflection = DailyReflection(
                    reflection_text=data["reflection_text"],
                    pondering_questions=data["pondering_questions"],
                    ccc_citations=ccc_citations,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens
                )
                
                return reflection
                
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                if attempt < max_retries - 1:
                    # Add guidance for next attempt
                    user_prompt += f"\n\nPrevious attempt had error: {e}. Please try again with valid CCC citations (1-2865)."
                    continue
                else:
                    raise ValueError(
                        f"Failed to generate valid reflection after {max_retries} attempts. "
                        f"Last error: {e}\nResponse: {response_text}"
                    )
        
        raise ValueError("Unexpected: reached end of retry loop")

    def get_cost_summary(self) -> dict:
        """Get summary of API costs for this session.
        
        Returns:
            Cost summary dictionary
        """
        return self.cost_tracker.get_summary()
