import requests
from bs4 import BeautifulSoup
from typing import Optional
from utils.logging import get_logger
import urllib.parse
import os

logger = get_logger(__name__)

async def scrape_content_from_url(url: str) -> Optional[str]:
    """
    Scrape text content from a given URL
    For local Docusaurus content, read markdown files directly
    For remote URLs, use HTTP requests
    """
    # Check if this is a local docs URL that we can access directly
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Go up 3 levels to project root
    website_docs_path = os.path.join(project_root, "website", "docs")

    # For Docusaurus docs paths
    if "spec-driven-ai-hackathon.vercel.app/docs" in url or url.startswith("http://localhost:") or "docs/" in url:
        try:
            # Convert URL to local file path
            if "physical-ai-humanoid-robotics" in url:
                local_path = os.path.join(website_docs_path, "physical-ai-humanoid-robotics")
            elif "study" in url:
                local_path = os.path.join(website_docs_path, "study")
            else:
                # Default to general docs
                local_path = website_docs_path

            # Look for markdown files in the appropriate directory
            import glob
            md_files = glob.glob(os.path.join(local_path, "**/*.md"), recursive=True)
            mdx_files = glob.glob(os.path.join(local_path, "**/*.mdx"), recursive=True)

            all_files = md_files + mdx_files
            if all_files:
                # Read and combine content from all markdown files in the path
                combined_content = ""
                for file_path in all_files:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Remove frontmatter if present
                            if content.startswith('---'):
                                try:
                                    end_frontmatter = content.find('---', 3)
                                    if end_frontmatter != -1:
                                        content = content[end_frontmatter+3:].strip()
                                except:
                                    pass  # If frontmatter parsing fails, use content as-is
                            combined_content += f"\n\n{content}"

                        logger.info(f"Successfully read local markdown file: {file_path}")
                    except Exception as e:
                        logger.error(f"Error reading local markdown file {file_path}: {str(e)}")
                        continue

                if combined_content:
                    # Clean up the text similar to the HTML parsing
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(combined_content, 'html.parser')
                    text = soup.get_text()

                    # Clean up the text
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = ' '.join(chunk for chunk in chunks if chunk)

                    logger.info(f"Successfully loaded content from local docs for URL {url}, length: {len(text)} characters")
                    return text
        except Exception as e:
            logger.error(f"Error accessing local docs for URL {url}: {str(e)}")

    # Fallback to traditional web scraping for non-docs URLs
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