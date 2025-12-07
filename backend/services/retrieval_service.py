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
            
            # For now, we're using the content from Qdrant payload
            # In a real implementation, you might want to fetch the full content from SQLite
            relevant_content.append({
                "chunk_id": chunk_id,
                "content": payload.get("chunk_text", ""),
                "source_url": payload.get("source_url", ""),
                "chunk_order": payload.get("chunk_order", 0),
                "similarity_score": score,
                "content_id": payload.get("content_id", "")
            })
    finally:
        db.close()
    
    logger.info(f"Found {len(relevant_content)} relevant content chunks")
    return relevant_content