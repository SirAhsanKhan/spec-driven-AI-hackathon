import os
from qdrant_client import QdrantClient, models
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "rag_chatbot_collection" # Default collection name

def get_qdrant_client():
    """Initializes and returns a Qdrant client."""
    if not QDRANT_URL or not QDRANT_API_KEY:
        raise ValueError("QDRANT_URL and QDRANT_API_KEY must be set in the environment variables.")
    
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )
    return client

def create_collection_if_not_exists(client: QdrantClient, vector_size: int):
    """Creates a Qdrant collection if it doesn't already exist."""
    current_collections = client.get_collections().collections
    if COLLECTION_NAME not in [c.name for c in current_collections]:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
        )
        print(f"Collection '{COLLECTION_NAME}' created with vector size {vector_size}.")
    else:
        print(f"Collection '{COLLECTION_NAME}' already exists.")

def upsert_vectors(client: QdrantClient, points: list[models.PointStruct]):
    """Upserts (inserts or updates) vectors into the Qdrant collection."""
    operation_info = client.upsert(
        collection_name=COLLECTION_NAME,
        wait=True,
        points=points,
    )
    print(f"Upserted vectors. Status: {operation_info.status}")

def search_vectors(client: QdrantClient, query_vector: list[float], limit: int = 5):
    """Searches the Qdrant collection for similar vectors."""
    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=limit,
    )
    return search_result

if __name__ == "__main__":
    # Example usage:
    # This block will only run if the script is executed directly
    # To run this, you need to set QDRANT_URL and QDRANT_API_KEY in your .env file
    # and also have an OpenAI API key to generate a dummy vector.

    print("Running Qdrant client example...")
    try:
        qdrant_client = get_qdrant_client()
        # For demonstration, let's assume a vector size of 1536 (typical for OpenAI embeddings)
        DUMMY_VECTOR_SIZE = 1536
        create_collection_if_not_exists(qdrant_client, DUMMY_VECTOR_SIZE)

        # Dummy data for upsert
        dummy_points = [
            models.PointStruct(
                id=1,
                vector=[0.1] * DUMMY_VECTOR_SIZE,
                payload={"text": "This is a test document about AI.", "source": "test_doc_1"}
            ),
            models.PointStruct(
                id=2,
                vector=[0.2] * DUMMY_VECTOR_SIZE,
                payload={"text": "Another document on machine learning.", "source": "test_doc_2"}
            ),
        ]
        upsert_vectors(qdrant_client, dummy_points)

        # Dummy query vector
        dummy_query_vector = [0.15] * DUMMY_VECTOR_SIZE
        search_results = search_vectors(qdrant_client, dummy_query_vector, limit=2)
        print("\nSearch Results:")
        for hit in search_results:
            print(f"ID: {hit.id}, Score: {hit.score}, Payload: {hit.payload}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
