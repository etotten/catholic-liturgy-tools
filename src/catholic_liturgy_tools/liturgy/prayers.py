"""Prayer loader and selection for daily readings."""

import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class SourcedPrayer:
    """Catholic prayer with source attribution."""

    id: str
    title: str
    text: str
    source: str
    source_url: str
    liturgical_contexts: List[str]
    tags: List[str]
    language: str


def load_prayers(prayer_db_path: Optional[str] = None) -> List[SourcedPrayer]:
    """Load prayers from JSON database.
    
    Args:
        prayer_db_path: Path to prayers.json (defaults to data/prayers.json)
        
    Returns:
        List of SourcedPrayer objects
        
    Raises:
        FileNotFoundError: If prayers database not found
        ValueError: If prayers database is invalid
    """
    if prayer_db_path is None:
        # Default to data/prayers.json relative to project root
        project_root = Path(__file__).parent.parent.parent.parent
        prayer_db_path = project_root / "data" / "prayers.json"
    
    prayer_path = Path(prayer_db_path)
    if not prayer_path.exists():
        raise FileNotFoundError(f"Prayer database not found: {prayer_path}")
    
    with open(prayer_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    prayers = []
    for prayer_data in data.get("prayers", []):
        prayer = SourcedPrayer(
            id=prayer_data["id"],
            title=prayer_data["title"],
            text=prayer_data["text"],
            source=prayer_data["source"],
            source_url=prayer_data["source_url"],
            liturgical_contexts=prayer_data["liturgical_contexts"],
            tags=prayer_data.get("tags", []),
            language=prayer_data["language"]
        )
        prayers.append(prayer)
    
    return prayers


def select_prayer(
    liturgical_contexts: List[str],
    prayers: Optional[List[SourcedPrayer]] = None,
    feast_info: Optional[dict] = None
) -> SourcedPrayer:
    """Select most appropriate prayer based on liturgical context.
    
    Selection priority:
    1. Exact match with all contexts
    2. Feast-specific prayers (saint, martyr, apostle, marian)
    3. Seasonal prayers (advent, christmas, lent, easter)
    4. General prayers (sunday, weekday)
    5. Universal prayers (all)
    
    Args:
        liturgical_contexts: List of context strings (e.g., ["advent", "weekday"])
        prayers: List of SourcedPrayer objects (loads from DB if None)
        feast_info: Optional feast day information dict
        
    Returns:
        Selected SourcedPrayer
        
    Raises:
        ValueError: If no prayers available or context invalid
    """
    if prayers is None:
        prayers = load_prayers()
    
    if not prayers:
        raise ValueError("No prayers available in database")
    
    # Build complete context list
    contexts = set(liturgical_contexts)
    
    # Add feast-specific contexts if provided
    if feast_info:
        if feast_info.get("is_saint"):
            contexts.add("saint")
            if feast_info.get("is_apostle"):
                contexts.add("apostle")
            if feast_info.get("is_martyr"):
                contexts.add("martyr")
        if feast_info.get("is_marian"):
            contexts.add("marian")
    
    # Score each prayer by context overlap
    scored_prayers = []
    for prayer in prayers:
        prayer_contexts = set(prayer.liturgical_contexts)
        overlap = len(contexts & prayer_contexts)
        
        # "all" context gets minimum score of 1
        if "all" in prayer_contexts:
            overlap = max(overlap, 1)
        
        if overlap > 0:
            scored_prayers.append((overlap, prayer))
    
    if not scored_prayers:
        # Fallback to first "all" context prayer
        for prayer in prayers:
            if "all" in prayer.liturgical_contexts:
                return prayer
        raise ValueError(f"No suitable prayer found for contexts: {contexts}")
    
    # Sort by score (descending)
    scored_prayers.sort(key=lambda x: x[0], reverse=True)
    
    # Get all prayers with highest score
    highest_score = scored_prayers[0][0]
    top_prayers = [p for score, p in scored_prayers if score == highest_score]
    
    # Return random prayer from highest-scoring group
    return random.choice(top_prayers)
