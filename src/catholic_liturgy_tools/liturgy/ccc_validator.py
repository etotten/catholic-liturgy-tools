"""CCC (Catechism of the Catholic Church) paragraph validator."""

MIN_PARAGRAPH = 1
MAX_PARAGRAPH = 2865


def validate_ccc_paragraph(paragraph_number: int) -> bool:
    """Validate if a CCC paragraph number is in valid range.
    
    The Catechism of the Catholic Church contains paragraphs numbered 1 through 2865.
    
    Args:
        paragraph_number: CCC paragraph number to validate
        
    Returns:
        True if valid, False otherwise
    """
    return MIN_PARAGRAPH <= paragraph_number <= MAX_PARAGRAPH


def get_ccc_url(paragraph_number: int) -> str:
    """Get Vatican website URL for a CCC paragraph.
    
    Args:
        paragraph_number: CCC paragraph number
        
    Returns:
        URL to Vatican CCC online
        
    Raises:
        ValueError: If paragraph number is invalid
    """
    if not validate_ccc_paragraph(paragraph_number):
        raise ValueError(
            f"Invalid CCC paragraph number: {paragraph_number}. "
            f"Must be between {MIN_PARAGRAPH} and {MAX_PARAGRAPH}."
        )
    
    # Vatican CCC URL structure (English version)
    return f"https://www.vatican.va/archive/ENG0015/_P{paragraph_number:X}.HTM"
