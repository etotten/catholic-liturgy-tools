# USCCB HTML Test Fixtures

This directory contains real HTML snapshots from the USCCB daily readings website (bible.usccb.org) for testing the scraper.

## Files

### `weekday_memorial_112225.html`
- **Date**: November 22, 2025
- **Liturgical Day**: Memorial of Saint Cecilia, Virgin and Martyr
- **Lectionary**: 502
- **Readings**: 4 readings (First Reading, Responsorial Psalm, Alleluia, Gospel)
- **URL**: https://bible.usccb.org/bible/readings/112225.cfm
- **Purpose**: Test typical weekday memorial day structure with standard 3-4 readings

### `sunday_113024.html`
- **Date**: November 30, 2025
- **Liturgical Day**: First Sunday of Advent
- **Lectionary**: (Sunday cycle)
- **Readings**: 4-5 readings (First Reading, Responsorial Psalm, Second Reading, Alleluia, Gospel)
- **URL**: https://bible.usccb.org/bible/readings/113024.cfm
- **Purpose**: Test Sunday structure which often has additional readings (Second Reading)

### `christmas_hub_122524.html`
- **Date**: December 25, 2024
- **Liturgical Day**: The Nativity of the Lord (Christmas)
- **Lectionaries**: 13, 14, 15, 16
- **Readings**: Multiple links to different Masses
- **URL**: https://bible.usccb.org/bible/readings/122524.cfm
- **Purpose**: Test major feast day that has multiple Mass options (Vigil, Night, Dawn, Day)
- **Special**: This is a "hub" page with links to 4 different Mass readings

### `christmas_day_mass_122524.html`
- **Date**: December 25, 2024
- **Liturgical Day**: The Nativity of the Lord (Christmas) - Mass during the Day
- **Lectionary**: 16
- **Readings**: 4 readings (First Reading, Responsorial Psalm, Second Reading, Alleluia, Gospel)
- **URL**: https://bible.usccb.org/bible/readings/122524-Day.cfm
- **Purpose**: Test specific Mass readings for a major feast day

## HTML Structure Notes

All USCCB pages follow a similar structure:

1. **Page Title**: Usually in `<title>` tag and H1 with class `page-title` or similar
2. **Liturgical Day**: Heading (H2 or H3) with the full liturgical day name
3. **Reading Entries**: Each reading has:
   - Title div with class `content-header` (e.g., "Reading 1", "Gospel")
   - Citation link
   - Text div with class `content-body` containing paragraphs

## Usage in Tests

These fixtures should be used for:
- Unit tests that parse HTML without making network requests
- Testing different liturgical day types
- Testing edge cases (multiple Masses, special feast days)
- Verifying scraper handles various HTML structures

## Updating Fixtures

If USCCB changes their HTML structure, these fixtures should be updated by fetching new snapshots:

```python
import requests
from pathlib import Path

url = 'https://bible.usccb.org/bible/readings/MMDDYY.cfm'
response = requests.get(url, headers={'User-Agent': 'CatholicLiturgyTools/0.2.0'})
Path('tests/fixtures/usccb_html/filename.html').write_text(response.text, encoding='utf-8')
```

**Note**: Always respect USCCB's robots.txt and rate limit requests (at least 1 second between requests).

## Copyright

These HTML files are copyrighted by the United States Conference of Catholic Bishops (USCCB) and the Confraternity of Christian Doctrine. They are included here solely for automated testing purposes under fair use. The scraped content must include proper attribution when displayed to users.
