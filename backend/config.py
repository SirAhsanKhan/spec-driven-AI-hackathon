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

# Use Neon PostgreSQL in production (Vercel), SQLite for local development
VERCEL_ENV = os.getenv("VERCEL_ENV")
if VERCEL_ENV:
    # In Vercel, require a proper database URL (PostgreSQL, etc.)
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL or "sqlite" in DATABASE_URL.lower():
        raise ValueError("SQLite is not supported in Vercel. Please configure a PostgreSQL database (like Neon).")
else:
    # Local development can use SQLite
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rag_chatbot.db")

def validate_config():
    """
    Validate required environment variables
    """
    # Only validate critical vars in Vercel, allow optional ones to be unset elsewhere
    required_vars = ["OPENAI_API_KEY"]
    
    # Only make CONTENT_URL required if not in Vercel (where it might be configured differently)
    if not os.getenv("VERCEL_ENV"):  
        required_vars.append("CONTENT_URL")
    
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