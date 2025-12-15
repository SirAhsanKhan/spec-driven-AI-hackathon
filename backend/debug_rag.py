import asyncio
import sys
import os

# Add the backend directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.embedding_service import generate_embedding
from services.vector_service import search_similar_embeddings
from services.retrieval_service import find_relevant_content
from utils.logging import get_logger

logger = get_logger(__name__)

async def debug_rag_flow():
    query = "What is this website about?"
    print(f"Debugging RAG flow for query: '{query}'")
    
    # Step 1: Generate embedding for the query
    print("\n1. Generating embedding for query...")
    try:
        query_embedding = await generate_embedding(query)
        print(f"   Query embedding generated, length: {len(query_embedding)}")
    except Exception as e:
        print(f"   Error generating query embedding: {e}")
        return
    
    # Step 2: Search for similar embeddings in Qdrant
    print("\n2. Searching for similar embeddings in Qdrant...")
    try:
        search_results = await search_similar_embeddings(query_embedding, top_k=5)
        print(f"   Found {len(search_results)} search results")
        
        # Print details of the first result if available
        if search_results:
            first_result = search_results[0]
            print(f"   First result ID: {first_result['id']}")
            print(f"   First result score: {first_result['score']}")
            print(f"   First result payload keys: {list(first_result['payload'].keys())}")
            print(f"   First result chunk_text (first 100 chars): {first_result['payload'].get('chunk_text', '')[:100]}")
    except Exception as e:
        print(f"   Error searching embeddings: {e}")
        return
    
    # Step 3: Find relevant content (this is what the API actually calls)
    print("\n3. Finding relevant content using find_relevant_content...")
    try:
        relevant_content = await find_relevant_content(query_embedding, top_k=5)
        print(f"   Found {len(relevant_content)} relevant content chunks")
        
        if relevant_content:
            first_chunk = relevant_content[0]
            print(f"   First chunk ID: {first_chunk['chunk_id']}")
            print(f"   First chunk content (first 100 chars): {first_chunk['content'][:100]}")
            print(f"   First chunk source: {first_chunk['source_url']}")
            print(f"   First chunk similarity score: {first_chunk['similarity_score']}")
        else:
            print("   No relevant content found - this is the likely issue!")
    except Exception as e:
        print(f"   Error finding relevant content: {e}")
        return

    print("\nDebugging completed.")

if __name__ == "__main__":
    asyncio.run(debug_rag_flow())