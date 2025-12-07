import openai
from config import OPENAI_API_KEY
from typing import List
from utils.logging import get_logger

logger = get_logger(__name__)

# Initialize OpenAI client
client = openai.AsyncClient(api_key=OPENAI_API_KEY)

async def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding for a given text using OpenAI's text-embedding-3-small model
    """
    try:
        response = await client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        raise

async def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of texts
    """
    embeddings = []
    for text in texts:
        embedding = await generate_embedding(text)
        embeddings.append(embedding)
    return embeddings