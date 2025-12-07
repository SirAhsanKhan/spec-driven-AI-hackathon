import re
from typing import List
from utils.logging import get_logger
from utils.token_utils import chunk_text

logger = get_logger(__name__)

def clean_content(content: str) -> str:
    """
    Clean and preprocess scraped content
    """
    if not content:
        return ""

    # Remove extra whitespace and normalize line breaks
    content = re.sub(r'\s+', ' ', content)
    content = content.strip()

    # Remove any non-printable characters
    content = ''.join(char for char in content if ord(char) < 127 or char.isspace())

    # Remove multiple consecutive newlines
    content = re.sub(r'\n\s*\n', '\n\n', content)

    logger.info(f"Cleaned content: original length {len(content)} characters")
    return content

def preprocess_content(content: str) -> str:
    """
    Additional preprocessing steps for the content
    """
    if not content:
        return ""

    # Remove common web navigation elements that might have been scraped
    content = re.sub(r'Copyright \d{4}.*?(?=\n|$)', '', content)
    content = re.sub(r'Home\s+About\s+Contact\s+Privacy', '', content)

    # Normalize whitespace again after content-specific cleaning
    content = re.sub(r'\s+', ' ', content).strip()

    return content

def validate_content(content: str) -> bool:
    """
    Validate content to ensure it meets minimum requirements
    """
    if not content or len(content.strip()) == 0:
        logger.warning("Content validation failed: Empty content")
        return False

    # Check that content has a reasonable minimum length
    if len(content) < 100:  # At least 100 characters
        logger.warning(f"Content validation failed: Content too short ({len(content)} chars)")
        return False

    return True

def create_content_chunks(content: str, max_tokens: int = 1024, min_tokens: int = 512) -> List[str]:
    """
    Create content chunks within the specified token range
    """
    if not validate_content(content):
        raise ValueError("Content validation failed")

    chunks = chunk_text(content, max_tokens, min_tokens)

    logger.info(f"Created {len(chunks)} content chunks from content")
    return chunks