from typing import List, Dict
from services.vector_service import search_similar_embeddings
from database.connection import SessionLocal
from database.content_repository import get_content_chunks
from utils.logging import get_logger
from models.content import ContentChunk

logger = get_logger(__name__)

async def find_relevant_content(query_embedding: List[float], top_k: int = 5) -> List[Dict]:
    """
    Find relevant content chunks based on query embedding
    """
    # Search for similar embeddings in Qdrant
    search_results = await search_similar_embeddings(query_embedding, top_k)
    
    # Get content from database using the chunk IDs from search results
    relevant_content = []
    db = SessionLocal()
    
    try:
        for result in search_results:
            chunk_id = result["id"]
            score = result["score"]
            payload = result["payload"]

            # Extract content from Qdrant payload
            chunk_content = payload.get("chunk_text", "")

            # Log the content to verify it's being retrieved
            logger.info(f"Retrieved chunk content (first 100 chars): {chunk_content[:100] if chunk_content else 'EMPTY'}")

            relevant_content.append({
                "chunk_id": chunk_id,
                "content": chunk_content,
                "source_url": payload.get("source_url", ""),
                "chunk_order": payload.get("chunk_order", 0),
                "similarity_score": score,
                "content_id": payload.get("content_id", "")
            })
    finally:
        db.close()

    logger.info(f"Found {len(relevant_content)} relevant content chunks")
    logger.info(f"First chunk content (first 200 chars if any): {relevant_content[0]['content'][:200] if relevant_content else 'No chunks found'}")
    return relevant_content