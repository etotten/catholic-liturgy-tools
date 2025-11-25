"""
USCCB readings scraper.

This module provides functionality to scrape daily Catholic liturgical readings
from the United States Conference of Catholic Bishops (USCCB) website.
"""

import logging
import re
from datetime import date
from typing import List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .models import DailyReading, ReadingEntry
from .exceptions import NetworkError, ParseError, ValidationError
from ..utils.retry import retry_with_backoff


logger = logging.getLogger(__name__)


class USCCBReadingsScraper:
    """
    Scraper for USCCB daily readings.
    
    This class fetches and parses Catholic liturgical readings from
    bible.usccb.org for any given date.
    
    Attributes:
        base_url: Base URL for USCCB readings
        timeout: Request timeout in seconds
        user_agent: User-Agent header for requests
    
    Example:
        >>> scraper = USCCBReadingsScraper()
        >>> readings = scraper.get_readings_for_date(date(2025, 11, 22))
        >>> print(readings.liturgical_day)
        'Memorial of Saint Cecilia, Virgin and Martyr'
    """
    
    def __init__(
        self,
        base_url: str = "https://bible.usccb.org/bible/readings",
        timeout: int = 30,
        user_agent: str = "CatholicLiturgyTools/0.2.0"
    ):
        """
        Initialize the USCCB readings scraper.
        
        Args:
            base_url: Base URL for USCCB readings (default: official USCCB site)
            timeout: Request timeout in seconds (default: 30)
            user_agent: User-Agent string for HTTP requests
        """
        self.base_url = base_url
        self.timeout = timeout
        self.user_agent = user_agent
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": user_agent})
    
    def _build_url(self, target_date: date) -> str:
        """
        Build the USCCB URL for a given date.
        
        USCCB uses the format: MMDDYY.cfm (e.g., 112225.cfm for Nov 22, 2025)
        
        Args:
            target_date: The date to build URL for
        
        Returns:
            Full URL string for the date's readings
        
        Example:
            >>> scraper = USCCBReadingsScraper()
            >>> scraper._build_url(date(2025, 11, 22))
            'https://bible.usccb.org/bible/readings/112225.cfm'
        """
        date_str = target_date.strftime("%m%d%y")
        return f"{self.base_url}/{date_str}.cfm"
    
    @retry_with_backoff(max_attempts=3, backoff_factor=2.0, logger_name="catholic_liturgy_tools.scraper.usccb")
    def _fetch_page(self, url: str) -> BeautifulSoup:
        """
        Fetch and parse HTML page from USCCB.
        
        This method is decorated with retry logic to handle transient network failures.
        
        Args:
            url: The URL to fetch
        
        Returns:
            BeautifulSoup object containing parsed HTML
        
        Raises:
            NetworkError: If network request fails after retries
        """
        try:
            logger.debug(f"Fetching URL: {url}")
            response = self._session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "lxml")
            logger.debug(f"Successfully fetched and parsed {url}")
            return soup
            
        except requests.exceptions.Timeout as e:
            raise NetworkError(f"Request timed out after {self.timeout}s: {url}", url=url) from e
        except requests.exceptions.ConnectionError as e:
            raise NetworkError(f"Connection error for {url}: {e}", url=url) from e
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            raise NetworkError(
                f"HTTP error {status_code} for {url}",
                url=url,
                status_code=status_code
            ) from e
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Request failed for {url}: {e}", url=url) from e
        except Exception as e:
            raise NetworkError(f"Unexpected error fetching {url}: {e}", url=url) from e
    
    def _extract_liturgical_day(self, soup: BeautifulSoup) -> str:
        """
        Extract the liturgical day name from the page.
        
        Uses multiple strategies in order of preference:
        1. Extract from <title> tag (most reliable)
        2. Extract from H1 or H2 with specific class
        3. Look for any prominent heading
        
        Args:
            soup: Parsed HTML document
        
        Returns:
            Liturgical day name (e.g., "Memorial of Saint Cecilia, Virgin and Martyr")
        
        Raises:
            ParseError: If liturgical day cannot be found
        """
        # Strategy 1: Extract from title tag
        title_tag = soup.find("title")
        if title_tag and title_tag.string:
            # Title format: "Daily Readings - November 22, 2025 - USCCB"
            # or "Memorial of Saint... - Daily Readings - USCCB"
            title_text = title_tag.string.strip()
            
            # Remove "Daily Readings" and "USCCB" parts
            title_text = re.sub(r'\s*-\s*Daily Readings.*$', '', title_text)
            title_text = re.sub(r'\s*\|\s*USCCB\s*$', '', title_text)
            title_text = re.sub(r'\s*-\s*USCCB\s*$', '', title_text)
            title_text = re.sub(r'^Daily Readings\s*-\s*', '', title_text)
            
            if title_text and len(title_text) > 10:
                logger.debug(f"Extracted liturgical day from title: {title_text}")
                return title_text.strip()
        
        # Strategy 2: Look for H2 or H3 heading (common pattern)
        for tag in ["h2", "h3", "h1"]:
            heading = soup.find(tag, class_=re.compile(r"(liturgical|day|title|heading)", re.I))
            if heading and heading.get_text(strip=True):
                text = heading.get_text(strip=True)
                if len(text) > 5 and text != "Daily Readings":
                    logger.debug(f"Extracted liturgical day from {tag}: {text}")
                    return text
        
        # Strategy 3: Look for any H2/H3 that looks like a liturgical day
        for tag in ["h2", "h3"]:
            headings = soup.find_all(tag)
            for heading in headings:
                text = heading.get_text(strip=True)
                # Check if it looks like a liturgical day (contains certain keywords)
                if any(keyword in text.lower() for keyword in ["sunday", "week", "memorial", "feast", "solemnity", "ordinary time", "advent", "lent", "easter"]):
                    if len(text) > 10:
                        logger.debug(f"Extracted liturgical day from {tag} (keyword match): {text}")
                        return text
        
        # If all strategies fail
        raise ParseError("Could not extract liturgical day from page", element="liturgical_day")
    
    def _extract_readings(self, soup: BeautifulSoup) -> List[ReadingEntry]:
        """
        Extract all reading entries from the page.
        
        Each reading consists of:
        - Title (e.g., "Reading 1", "Gospel")
        - Citation (e.g., "Luke 21:5-11")
        - Text paragraphs
        
        USCCB HTML Structure:
        - H3 with class="name" contains reading title
        - Next div with class="address" contains citation link
        - Next div with class="content-body" contains paragraphs of text
        
        Args:
            soup: Parsed HTML document
        
        Returns:
            List of ReadingEntry objects
        
        Raises:
            ParseError: If no readings can be extracted
        """
        readings = []
        
        # USCCB structure: H3 with class="name" for titles
        reading_headings = soup.find_all("h3", class_="name")
        
        for heading in reading_headings:
            title = heading.get_text(strip=True)
            
            # Skip if not a reading title
            if not any(keyword in title.lower() for keyword in ["reading", "gospel", "psalm", "alleluia"]):
                continue
            
            # Find the parent content-header div
            content_header = heading.find_parent("div", class_="content-header")
            if not content_header:
                logger.warning(f"No content-header div found for {title}, skipping")
                continue
            
            # Find citation in div with class "address" (sibling of H3)
            address_div = content_header.find("div", class_="address")
            if not address_div:
                logger.warning(f"No address div found for {title}, skipping")
                continue
            
            citation_link = address_div.find("a", href=re.compile(r"/bible/", re.I))
            if not citation_link:
                logger.warning(f"No citation link found for {title}, skipping")
                continue
            
            citation = citation_link.get_text(strip=True)
            
            # Find text content in div with class "content-body" (sibling of content-header)
            content_body = content_header.find_next_sibling("div", class_="content-body")
            if not content_body:
                logger.warning(f"No content-body div found for {title}, skipping")
                continue
            
            # Extract all paragraphs from content-body
            text_paragraphs = []
            for p in content_body.find_all("p", recursive=True):
                text = p.get_text(separator=" ", strip=True)
                # Filter out very short text and navigation elements
                if text and len(text) > 20 and not any(skip in text.lower() for skip in ["listen podcast", "view reflection", "en español", "view calendar", "get daily readings"]):
                    text_paragraphs.append(text)
            
            if text_paragraphs:
                readings.append(ReadingEntry(
                    title=title,
                    citation=citation,
                    text=text_paragraphs
                ))
                logger.debug(f"Extracted reading: {title} ({citation}) with {len(text_paragraphs)} paragraphs")
            else:
                logger.warning(f"No text found for {title} ({citation}), skipping")
        
        if not readings:
            raise ParseError("Could not extract any readings from page", element="readings")
        
        logger.info(f"Extracted {len(readings)} readings")
        return readings
    
    def _check_for_multiple_masses(self, soup: BeautifulSoup, date_str: str) -> Optional[str]:
        """
        Check if this is a feast day with multiple Mass options.
        
        Some major feast days (e.g., Christmas, Easter) have separate readings
        for Vigil Mass, Mass during Night/Dawn/Day, etc.
        
        Args:
            soup: Parsed HTML document
            date_str: Date string in MMDDYY format
        
        Returns:
            Warning message if multiple Masses detected, None otherwise
        """
        # Look for links to specific Mass times
        mass_links = soup.find_all("a", href=re.compile(rf"{date_str}-(Vigil|Night|Dawn|Day)\.cfm", re.I))
        
        if mass_links:
            mass_types = [link.get_text(strip=True) for link in mass_links]
            warning = f"Multiple Mass options found: {', '.join(mass_types)}. Using first available."
            logger.warning(warning)
            return warning
        
        return None
    
    def get_readings_for_date(self, target_date: date) -> DailyReading:
        """
        Fetch readings for the specified date.
        
        This is the main public method that orchestrates the scraping process:
        1. Build URL for the date
        2. Fetch and parse HTML
        3. Extract liturgical day
        4. Extract all readings
        5. Validate and return DailyReading object
        
        Args:
            target_date: The date to fetch readings for
        
        Returns:
            DailyReading object containing all readings for the date
        
        Raises:
            NetworkError: If network request fails
            ParseError: If HTML parsing fails
            ValidationError: If extracted data is invalid
        
        Example:
            >>> scraper = USCCBReadingsScraper()
            >>> readings = scraper.get_readings_for_date(date(2025, 11, 22))
            >>> print(f"{readings.liturgical_day}: {len(readings.readings)} readings")
        """
        url = self._build_url(target_date)
        logger.info(f"Fetching readings for {target_date.isoformat()}")
        
        # Fetch and parse HTML
        soup = self._fetch_page(url)
        
        # Check for multiple Masses (feast days)
        date_str = target_date.strftime("%m%d%y")
        multiple_mass_warning = self._check_for_multiple_masses(soup, date_str)
        if multiple_mass_warning:
            logger.warning(multiple_mass_warning)
        
        # Extract liturgical day
        liturgical_day = self._extract_liturgical_day(soup)
        
        # Extract readings
        readings = self._extract_readings(soup)
        
        # Build date display string
        date_display = target_date.strftime("%A, %B %d, %Y")
        
        # Create DailyReading object
        daily_reading = DailyReading(
            date=target_date,
            date_display=date_display,
            liturgical_day=liturgical_day,
            readings=readings,
            source_url=url
        )
        
        # Validate
        try:
            daily_reading.validate()
        except ValidationError as e:
            logger.error(f"Validation failed for readings: {e}")
            raise
        
        logger.info(f"Successfully scraped {len(readings)} readings for {target_date.isoformat()}")
        return daily_reading
