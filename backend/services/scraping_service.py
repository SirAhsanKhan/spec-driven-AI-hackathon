import requests
from bs4 import BeautifulSoup
from typing import Optional
from utils.logging import get_logger

logger = get_logger(__name__)

async def scrape_content_from_url(url: str) -> Optional[str]:
    """
    Scrape text content from a given URL
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up the text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        logger.info(f"Successfully scraped content from {url}, length: {len(text)} characters")
        return text
    
    except requests.RequestException as e:
        logger.error(f"Error scraping content from {url}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error scraping content from {url}: {str(e)}")
        return None