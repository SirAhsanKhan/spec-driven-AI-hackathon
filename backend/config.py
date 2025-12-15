import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
CONTENT_URL = os.getenv("CONTENT_URL")
CONTENT_URL_DOC1 = os.getenv("CONTENT_URL_DOC1")
CONTENT_URL_DOC2 = os.getenv("CONTENT_URL_DOC2")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rag_chatbot.db")

# Validate required environment variables
def validate_config():
    required_vars = ["OPENAI_API_KEY", "CONTENT_URL"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    return True

def get_content_url():
    """
    Retrieve the primary pre-stored URL from environment variables
    """
    return CONTENT_URL

def get_content_urls():
    """
    Retrieve all pre-stored URLs from environment variables
    """
    urls = []
    if CONTENT_URL:
        urls.append(CONTENT_URL)
    if CONTENT_URL_DOC1:
        urls.append(CONTENT_URL_DOC1)
    if CONTENT_URL_DOC2:
        urls.append(CONTENT_URL_DOC2)
    return urls