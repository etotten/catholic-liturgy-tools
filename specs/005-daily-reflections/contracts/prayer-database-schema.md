# Contract: Prayer Database Schema

**Feature**: 005-daily-reflections  
**Purpose**: Define JSON schema for curated Catholic prayer database

---

## Overview

The prayer database is a **curated JSON file** containing Catholic prayers sourced from five authoritative websites. Prayers are categorized by liturgical context to enable contextual selection.

**Curation Workflow**:
1. AI finds prayers from approved sources during implementation
2. AI formats prayers according to this schema
3. Human reviews `data/prayers.json` in pull request
4. Human commits to repository = approval
5. Human can request AI to replace unsuitable prayers

**File Location**: `data/prayers.json`

**Update Frequency**: Manual updates as needed (not automated)

**Sources** (per FR-007):
1. USCCB (United States Conference of Catholic Bishops)
2. Vatican.va (Holy See official website)
3. CatholicOnline.org
4. EWTN (Eternal Word Television Network)
5. LoyolaPress.com

---

## JSON Schema

### Root Structure

```json
{
  "version": "1.0.0",
  "last_updated": "YYYY-MM-DD",
  "sources": [
    {
      "name": "Source name",
      "base_url": "https://..."
    }
  ],
  "prayers": [
    {
      "id": "unique-prayer-id",
      "title": "Prayer Title",
      "text": "Full prayer text...",
      "source": "Source name",
      "source_url": "https://...",
      "liturgical_contexts": ["context1", "context2"],
      "tags": ["tag1", "tag2"],
      "language": "en"
    }
  ]
}
```

---

## Field Definitions

### Root Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version` | String | Yes | Semantic version of database schema (e.g., "1.0.0") |
| `last_updated` | String (ISO date) | Yes | Date of last manual update (YYYY-MM-DD) |
| `sources` | Array[Source] | Yes | List of authoritative sources |
| `prayers` | Array[Prayer] | Yes | List of curated prayers |

### Source Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | String | Yes | Display name of source (e.g., "USCCB", "Vatican") |
| `base_url` | String (URL) | Yes | Base URL of source website |

### Prayer Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | String | Yes | Unique identifier (kebab-case, e.g., "hail-mary") |
| `title` | String | Yes | Display title of prayer (e.g., "Hail Mary") |
| `text` | String | Yes | Full prayer text (may include line breaks `\n`) |
| `source` | String | Yes | Name of source (must match a `sources[].name`) |
| `source_url` | String (URL) | Yes | Direct URL to prayer on source website |
| `liturgical_contexts` | Array[String] | Yes | List of applicable liturgical contexts (see below) |
| `tags` | Array[String] | No | Optional tags for additional filtering |
| `language` | String | Yes | ISO 639-1 language code (e.g., "en" for English) |

---

## Liturgical Contexts

**Purpose**: Enable contextual prayer selection based on liturgical season or feast type.

### Valid Context Values

| Context | Description | Example Usage |
|---------|-------------|---------------|
| `advent` | Advent season | First Sunday of Advent - Christmas Eve |
| `christmas` | Christmas season | Christmas - Baptism of the Lord |
| `lent` | Lent season | Ash Wednesday - Holy Saturday |
| `easter` | Easter season | Easter Sunday - Pentecost |
| `ordinary` | Ordinary Time | Weeks outside major seasons |
| `solemnity` | Major feast days | Christmas, Easter, Pentecost, etc. |
| `feast` | Feast days | Feast of a saint or mystery |
| `memorial` | Memorial days | Memorial of a saint |
| `sunday` | Any Sunday | Applicable to all Sundays |
| `weekday` | Any weekday | Applicable to Monday-Saturday |
| `saint` | Any saint's day | Memorials, feasts of saints |
| `marian` | Marian feast days | Feasts of Mary |
| `apostle` | Feast of apostle | Saints who were apostles |
| `martyr` | Feast of martyr | Saints who were martyred |
| `all` | Universal prayers | Applicable to any day |

**Multiple Contexts**: A prayer may have multiple contexts (e.g., `["advent", "sunday"]` for Advent Sunday prayer)

---

## Tags

**Purpose**: Additional filtering beyond liturgical context (optional).

### Suggested Tag Values

- `traditional` - Traditional prayers (e.g., Hail Mary, Our Father)
- `morning` - Morning prayers
- `evening` - Evening prayers
- `scripture-based` - Prayers drawn from Scripture
- `contemporary` - Modern compositions
- `intercession` - Intercessory prayers
- `thanksgiving` - Prayers of thanksgiving
- `petition` - Prayers of petition
- `praise` - Prayers of praise and adoration

**Note**: Tags are flexible and can be extended as needed.

---

## Example Prayer Entries

### Example 1: Anima Christi (Soul of Christ)

```json
{
  "id": "anima-christi",
  "title": "Anima Christi (Soul of Christ)",
  "text": "Soul of Christ, sanctify me.\nBody of Christ, save me.\nBlood of Christ, inebriate me.\nWater from the side of Christ, wash me.\nPassion of Christ, strengthen me.\nO Good Jesus, hear me.\nWithin your wounds hide me.\nPermit me not to be separated from you.\nFrom the wicked foe, defend me.\nAt the hour of my death, call me\nand bid me come to you\nthat with your saints I may praise you\nfor ever and ever. Amen.",
  "source": "USCCB",
  "source_url": "https://www.usccb.org/prayers/anima-christi",
  "liturgical_contexts": ["all", "ordinary"],
  "tags": ["traditional", "eucharistic"],
  "language": "en"
}
```

### Example 2: Seasonal Prayer (Advent)

```json
{
  "id": "advent-prayer-usccb",
  "title": "Prayer for Advent",
  "text": "Almighty God, give us grace to cast away the works of darkness and put on the armor of light, now in the time of this mortal life in which Your Son Jesus Christ came to visit us in great humility; that in the last day, when He shall come again in His glorious majesty to judge both the living and the dead, we may rise to the life immortal; through Him who lives and reigns with You and the Holy Spirit, one God, now and forever. Amen.",
  "source": "USCCB",
  "source_url": "https://www.usccb.org/prayers/advent",
  "liturgical_contexts": ["advent", "weekday"],
  "tags": ["seasonal", "preparation"],
  "language": "en"
}
```

### Example 3: Saint's Day Prayer

```json
{
  "id": "prayer-st-francis",
  "title": "Prayer of St. Francis",
  "text": "Lord, make me an instrument of your peace:\nwhere there is hatred, let me sow love;\nwhere there is injury, pardon;\nwhere there is doubt, faith;\nwhere there is despair, hope;\nwhere there is darkness, light;\nwhere there is sadness, joy.\n\nO divine Master, grant that I may not so much seek\nto be consoled as to console,\nto be understood as to understand,\nto be loved as to love.\nFor it is in giving that we receive,\nit is in pardoning that we are pardoned,\nand it is in dying that we are born to eternal life.\nAmen.",
  "source": "Vatican",
  "source_url": "https://www.vatican.va/special/rosary/documents/peace_en.html",
  "liturgical_contexts": ["all", "saint"],
  "tags": ["traditional", "peace", "franciscan"],
  "language": "en"
}
```

### Example 4: Easter Season Prayer

```json
{
  "id": "regina-caeli",
  "title": "Regina Caeli (Queen of Heaven)",
  "text": "Queen of Heaven, rejoice, alleluia.\nFor He whom you did merit to bear, alleluia.\nHas risen, as he said, alleluia.\nPray for us to God, alleluia.\nRejoice and be glad, O Virgin Mary, alleluia.\nFor the Lord has truly risen, alleluia.\n\nLet us pray. O God, who gave joy to the world through the resurrection of Thy Son, our Lord Jesus Christ, grant we beseech Thee, that through the intercession of the Virgin Mary, His Mother, we may obtain the joys of everlasting life. Through the same Christ our Lord. Amen.",
  "source": "EWTN",
  "source_url": "https://www.ewtn.com/catholicism/devotions/regina-caeli-380",
  "liturgical_contexts": ["easter", "marian"],
  "tags": ["traditional", "marian", "resurrection"],
  "language": "en"
}
```

---

## Selection Algorithm

### Context Matching Rules

1. **Exact Match Priority**: Prefer prayers with liturgical context exactly matching the day
   - Example: Advent weekday → prefer `["advent", "weekday"]`

2. **Partial Match**: Accept prayers with subset of contexts
   - Example: Advent weekday → accept `["advent"]` or `["weekday"]`

3. **Universal Fallback**: Use `["all"]` prayers as last resort

4. **Feast Day Override**: If saint's day, prioritize `["saint"]` prayers
   - If apostle: prioritize `["apostle"]` over generic `["saint"]`
   - If martyr: prioritize `["martyr"]` over generic `["saint"]`

5. **Marian Priority**: For Marian feast days, prioritize `["marian"]` prayers

### Selection Logic (Pseudocode)

```python
def select_prayer(liturgical_context: str, feast_info: Optional[FeastInfo]) -> Prayer:
    """
    Select prayer based on liturgical context and feast information.
    
    Priority:
    1. Exact match with all contexts
    2. Feast-specific prayers (saint, martyr, apostle, marian)
    3. Seasonal prayers (advent, christmas, lent, easter)
    4. General prayers (sunday, weekday)
    5. Universal prayers (all)
    """
    
    # Parse contexts from liturgical_context string
    contexts = parse_contexts(liturgical_context)  # e.g., ["advent", "weekday"]
    
    # Add feast-specific contexts
    if feast_info:
        if feast_info.is_saint:
            contexts.append("saint")
            if is_apostle(feast_info):
                contexts.append("apostle")
            if is_martyr(feast_info):
                contexts.append("martyr")
        if is_marian_feast(feast_info):
            contexts.append("marian")
    
    # Load all prayers
    prayers = load_prayers_from_json()
    
    # Score each prayer by context overlap
    scored_prayers = []
    for prayer in prayers:
        overlap = count_overlapping_contexts(prayer.liturgical_contexts, contexts)
        scored_prayers.append((overlap, prayer))
    
    # Sort by score (descending) and return highest
    scored_prayers.sort(key=lambda x: x[0], reverse=True)
    
    # Return highest-scoring prayer (or random if multiple with same score)
    return scored_prayers[0][1]
```

---

## Initial Database Population

### Recommended Starting Set

**Minimum viable database** (20-30 prayers):

**Exclusions**: Avoid commonly memorized prayers (Hail Mary, Our Father, Glory Be, Memorare, etc.) to provide readers with enriching content they may not have encountered.

1. **Universal Prayers** (5):
   - Prayer of St. Francis
   - Anima Christi
   - Prayer before Scripture reading
   - Act of Spiritual Communion
   - Prayer for God's Will

2. **Seasonal Prayers** (10):
   - Advent: 2 prayers (e.g., O Antiphon-inspired, Advent wreath blessing)
   - Christmas: 2 prayers (e.g., Nativity prayers, Epiphany)
   - Lent: 3 prayers (e.g., Stations prayers, penitential prayers)
   - Easter: 3 prayers (e.g., Resurrection prayers, Pentecost prayers)

3. **Saint Prayers** (5):
   - Prayers by/for saints from USCCB/Vatican saint pages
   - Apostle prayers (not overly familiar)
   - Martyr prayers
   - Lesser-known Marian prayers (not Memorare)

4. **Daily Prayers** (5):
   - Morning offering (traditional but not rote)
   - Evening examination prayer
   - Prayer for particular day's liturgical focus
   - Prayer inspired by saint of the day
   - Prayer from Liturgy of the Hours tradition

### Expansion Strategy

- Add prayers gradually as new liturgical seasons approached
- Prioritize feast days in current month
- Balance across five sources

---

## Validation Rules

### Database Validation

1. **Schema Compliance**: JSON must match defined schema
2. **Unique IDs**: All prayer IDs must be unique
3. **Valid Sources**: All `prayer.source` must reference a `sources[].name`
4. **Valid URLs**: All URLs must be valid HTTP(S) and reachable
5. **Valid Contexts**: All contexts must be from approved list
6. **Language Codes**: All language codes must be valid ISO 639-1

### Prayer Validation

1. **Non-empty Text**: Prayer text must not be empty
2. **Non-empty Title**: Prayer title must not be empty
3. **At Least One Context**: Must have at least one liturgical context
4. **Source Attribution**: Must have valid source and URL

---

## Maintenance

### Update Process

1. **AI Discovery**: AI finds prayers on approved sources (initial population or additions)
2. **AI Formatting**: AI converts to JSON format following schema
3. **Human Review**: Human reviews prayers in `data/prayers.json`
4. **Human Approval**: Human commits = approval, or requests AI to replace specific prayers
5. **Validate**: Run validation script to check schema compliance
6. **Test**: Verify prayer selection algorithm works with new entries

### Version Control

- Track `data/prayers.json` in Git
- Use semantic versioning in `version` field
- Update `last_updated` field with each change
- Document major changes in commit messages

---

## Implementation Notes

### File Location

```
catholic-liturgy-tools/
└── data/
    └── prayers.json
```

### Loading Logic

```python
import json
from pathlib import Path

def load_prayers() -> List[Prayer]:
    """Load prayers from JSON database."""
    db_path = Path(__file__).parent.parent / "data" / "prayers.json"
    with open(db_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Prayer(**p) for p in data["prayers"]]
```

### Caching Strategy

- Load prayers once at module import
- Cache in memory (database is small ~50-100KB)
- No need for database system (file-based sufficient)

---

## Testing

### Test Cases

1. **Load database**: Verify JSON loads without errors
2. **Schema validation**: Verify all prayers match schema
3. **Unique IDs**: Verify no duplicate prayer IDs
4. **Valid sources**: Verify all sources exist in sources list
5. **Selection algorithm**: Test selection for various liturgical contexts
6. **Feast day selection**: Test saint/martyr/apostle/marian priority
7. **Fallback**: Test universal prayer fallback when no match

### Example Test

```python
def test_prayer_selection_advent():
    """Test prayer selection for Advent weekday."""
    liturgical_context = "Tuesday of the First Week of Advent"
    feast_info = None
    
    prayer = select_prayer(liturgical_context, feast_info)
    
    assert prayer is not None
    assert "advent" in prayer.liturgical_contexts or "weekday" in prayer.liturgical_contexts or "all" in prayer.liturgical_contexts
```
