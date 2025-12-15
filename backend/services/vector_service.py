from qdrant_client import QdrantClient
from qdrant_client.http import models
from config import QDRANT_HOST, QDRANT_API_KEY, QDRANT_PORT
from typing import List, Dict, Optional
import uuid
from utils.logging import get_logger

logger = get_logger(__name__)

# Initialize Qdrant client
try:
    # Check if QDRANT_HOST contains a protocol (http/https), which indicates Qdrant Cloud
    if QDRANT_HOST.startswith(('http://', 'https://')):
        # For Qdrant Cloud, use url parameter instead of host/port
        qdrant_client = QdrantClient(
            url=QDRANT_HOST,
            api_key=QDRANT_API_KEY,
            prefer_grpc=False  # Use HTTP API for cloud
        )
    else:
        # For local Qdrant, use host/port
        qdrant_client = QdrantClient(
            host=QDRANT_HOST,
            port=QDRANT_PORT,
            api_key=QDRANT_API_KEY,
        )
except Exception as e:
    logger.error(f"Failed to initialize Qdrant client: {e}")
    qdrant_client = None

# Vector dimension for OpenAI text-embedding-3-small (1536)
VECTOR_SIZE = 1536
COLLECTION_NAME = "content_chunks"

def init_qdrant_collection():
    """
    Initialize the Qdrant collection for storing content chunk embeddings
    """
    if not qdrant_client:
        logger.error("Qdrant client not initialized, skipping collection initialization")
        return False

    try:
        # Check if collection already exists
        qdrant_client.get_collection(collection_name=COLLECTION_NAME)
        print(f"Collection '{COLLECTION_NAME}' already exists")
        return True
    except Exception as e:
        logger.error(f"Error checking collection existence: {e}")
        try:
            # Create a new collection
            qdrant_client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(
                    size=VECTOR_SIZE,
                    distance=models.Distance.COSINE
                )
            )
            print(f"Created collection '{COLLECTION_NAME}' with {VECTOR_SIZE}-dimension vectors")
            return True
        except Exception as create_error:
            logger.error(f"Failed to create Qdrant collection: {create_error}")
            return False

async def store_embedding(chunk_id: str, embedding: List[float], content_metadata: Dict):
    """
    Store an embedding in Qdrant with associated metadata (no raw content duplication)
    """
    if not qdrant_client:
        logger.error("Qdrant client not available, cannot store embedding")
        return False

    try:
        points = [
            models.PointStruct(
                id=chunk_id,
                vector=embedding,
                payload={
                    "content_id": content_metadata.get("content_id"),
                    "chunk_order": content_metadata.get("chunk_order"),
                    "source_url": content_metadata.get("source_url"),
                    # Include chunk_text in payload as it's needed for response generation
                    "chunk_text": content_metadata.get("chunk_text", "")
                }
            )
        ]

        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        return True
    except Exception as e:
        logger.error(f"Error storing embedding in Qdrant: {e}")
        # In a real implementation, you might want to queue these for later processing
        # or have a fallback storage mechanism
        return False

async def store_embeddings_batch(chunk_embeddings: List[tuple], content_metadata_list: List[Dict]):
    """
    Store multiple embeddings in Qdrant efficiently
    chunk_embeddings: List of (chunk_id, embedding) tuples
    """
    if not qdrant_client:
        logger.error("Qdrant client not available, cannot store embeddings batch")
        return False

    try:
        points = []
        for i, (chunk_id, embedding) in enumerate(chunk_embeddings):
            metadata = content_metadata_list[i]
            points.append(models.PointStruct(
                id=chunk_id,
                vector=embedding,
                payload={
                    "content_id": metadata.get("content_id"),
                    "chunk_order": metadata.get("chunk_order"),
                    "source_url": metadata.get("source_url"),
                    # Include chunk_text in payload as it's needed for response generation
                    "chunk_text": metadata.get("chunk_text", "")
                }
            ))

        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        return True
    except Exception as e:
        logger.error(f"Error storing embeddings batch in Qdrant: {e}")
        # In a real implementation, you might want to queue these for later processing
        # or have a fallback storage mechanism
        return False

async def clear_collection():
    """
    Clear all points from the Qdrant collection (useful when schema changes)
    """
    if not qdrant_client:
        logger.error("Qdrant client not available, cannot clear collection")
        return False

    try:
        # Delete all points in the collection
        qdrant_client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[]
                )
            )
        )
        logger.info(f"Cleared all points from collection '{COLLECTION_NAME}'")
        return True
    except Exception as e:
        logger.error(f"Error clearing Qdrant collection: {e}")
        return False

async def search_similar_embeddings(query_embedding: List[float], top_k: int = 5):
    """
    Search for similar embeddings in Qdrant
    """
    if not qdrant_client:
        logger.error("Qdrant client not available, cannot perform search")
        # Return empty results as fallback
        return []

    try:
        # Use the correct query API for newer versions of qdrant-client
        search_result = qdrant_client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_embedding,
            limit=top_k
        )

        results = []
        # For newer qdrant-client, search_result should be a QueryResponse object
        # with a points attribute containing the search results
        for point in search_result.points:
            results.append({
                "id": point.id,
                "score": point.score,
                "payload": point.payload
            })

        return results
    except Exception as e:
        logger.error(f"Error searching embeddings in Qdrant: {e}")
        # Return empty results as fallback
        return []