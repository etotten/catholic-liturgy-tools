"""Liturgical calendar integration using romcal."""

import json
import subprocess
from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class SaintBiography:
    """Biographical information for a saint."""

    name: str
    feast_date: str
    life_span: str
    patronage: str
    biography_summary: str
    source_url: str


@dataclass
class FeastDayInfo:
    """Information about a feast day or memorial."""

    feast_type: str  # "solemnity", "feast", "memorial", "optional_memorial"
    feast_name: str
    liturgical_color: str
    is_saint: bool
    is_marian: bool
    is_apostle: bool
    is_martyr: bool
    saint_biography: Optional[SaintBiography] = None


def get_liturgical_day(target_date: date) -> dict:
    """Get liturgical day information using romcal.
    
    Calls Node.js romcal library via subprocess to get liturgical calendar data.
    
    Args:
        target_date: Date to query
        
    Returns:
        Dictionary with liturgical day information
        
    Raises:
        RuntimeError: If romcal call fails
    """
    # Create Node.js script to call romcal
    node_script = f"""
const {{ Romcal, Dates }} = require('romcal');

const romcal = new Romcal({{ 
    scope: 'gregorian',
    locale: 'en'
}});

const year = {target_date.year};
const month = {target_date.month};
const day = {target_date.day};

romcal
    .generateCalendar(year)
    .then((calendar) => {{
        const dateKey = `${{year}}-${{month.toString().padStart(2, '0')}}-${{day.toString().padStart(2, '0')}}`;
        const liturgicalDay = calendar.find(d => d.date.toISOString().startsWith(dateKey));
        
        if (liturgicalDay) {{
            console.log(JSON.stringify({{
                date: dateKey,
                name: liturgicalDay.name || 'Ordinary Time',
                type: liturgicalDay.type || 'weekday',
                rank: liturgicalDay.rank || 'weekday',
                liturgicalColors: liturgicalDay.colors || ['green'],
                celebrations: liturgicalDay.celebrations || [],
                season: liturgicalDay.season || 'ordinary_time'
            }}));
        }} else {{
            console.log(JSON.stringify({{
                date: dateKey,
                name: 'Ordinary Time',
                type: 'weekday',
                rank: 'weekday',
                liturgicalColors: ['green'],
                celebrations: [],
                season: 'ordinary_time'
            }}));
        }}
    }})
    .catch((error) => {{
        console.error('Error:', error.message);
        process.exit(1);
    }});
"""
    
    try:
        result = subprocess.run(
            ["node", "-e", node_script],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to get liturgical day from romcal: {e.stderr}"
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError("Romcal call timed out after 10 seconds")
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Failed to parse romcal output: {e}\nOutput: {result.stdout}"
        )


def parse_feast_info(liturgical_data: dict) -> Optional[FeastDayInfo]:
    """Parse feast day information from romcal data.
    
    Args:
        liturgical_data: Dictionary from get_liturgical_day()
        
    Returns:
        FeastDayInfo if a feast/memorial, None for ordinary weekdays
    """
    rank = liturgical_data.get("rank", "weekday")
    feast_type = liturgical_data.get("type", "weekday")
    
    # Only create FeastDayInfo for actual feasts/memorials
    if rank == "weekday" and feast_type == "weekday":
        return None
    
    feast_name = liturgical_data.get("name", "")
    liturgical_colors = liturgical_data.get("liturgicalColors", ["green"])
    
    # Determine if saint-related
    is_saint = any(
        keyword in feast_name.lower()
        for keyword in ["saint", "st.", "blessed"]
    )
    
    is_marian = any(
        keyword in feast_name.lower()
        for keyword in ["mary", "our lady", "virgin", "assumption", "immaculate"]
    )
    
    is_apostle = any(
        keyword in feast_name.lower()
        for keyword in ["apostle", "peter", "paul", "andrew", "james", "john"]
    )
    
    is_martyr = "martyr" in feast_name.lower()
    
    return FeastDayInfo(
        feast_type=feast_type,
        feast_name=feast_name,
        liturgical_color=liturgical_colors[0] if liturgical_colors else "green",
        is_saint=is_saint,
        is_marian=is_marian,
        is_apostle=is_apostle,
        is_martyr=is_martyr
    )


def get_liturgical_context_list(target_date: date) -> list:
    """Get list of liturgical context strings for prayer selection.
    
    Args:
        target_date: Date to query
        
    Returns:
        List of context strings (e.g., ["advent", "weekday"])
    """
    liturgical_data = get_liturgical_day(target_date)
    season = liturgical_data.get("season", "ordinary_time")
    
    contexts = []
    
    # Add season context
    season_map = {
        "advent": "advent",
        "christmas": "christmas",
        "lent": "lent",
        "easter": "easter",
        "ordinary_time": "ordinary"
    }
    contexts.append(season_map.get(season, "ordinary"))
    
    # Add day type
    if target_date.weekday() == 6:  # Sunday is 6 in Python
        contexts.append("sunday")
    else:
        contexts.append("weekday")
    
    # Add feast info if applicable
    feast_info = parse_feast_info(liturgical_data)
    if feast_info:
        rank_map = {
            "solemnity": "solemnity",
            "feast": "feast",
            "memorial": "memorial",
            "optional_memorial": "memorial"
        }
        if feast_info.feast_type in rank_map:
            contexts.append(rank_map[feast_info.feast_type])
    
    return contexts
