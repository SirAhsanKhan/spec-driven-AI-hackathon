from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from services.embedding_service import generate_embedding
from services.retrieval_service import find_relevant_content
from services.response_service import generate_response
from utils.logging import get_logger
from typing import List, AsyncGenerator
import json

router = APIRouter()
logger = get_logger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str
    sources: List[str]

def validate_query(query: str) -> tuple[bool, str]:
    """
    Validate the user query for content and format
    Returns (is_valid, error_message)
    """
    if not query or len(query.strip()) == 0:
        return False, "Query cannot be empty"

    if len(query.strip()) < 3:
        return False, "Query must be at least 3 characters long"

    if len(query) > 1000:
        return False, "Query must be less than 1000 characters long"

    # Check for potentially harmful patterns
    harmful_patterns = [
        r'<script',  # Potential XSS
        r'javascript:',  # Potential XSS
        r'vbscript:',  # Potential XSS
    ]

    query_lower = query.lower()
    for pattern in harmful_patterns:
        import re
        if re.search(pattern, query_lower):
            return False, "Query contains invalid characters or patterns"

    return True, ""

def sanitize_query(query: str) -> str:
    """
    Sanitize the user query to prevent injection or malicious input
    """
    # Remove any control characters (except \n, \r, \t)
    sanitized = ''.join(char for char in query if ord(char) >= 32 or char in '\n\r\t')
    # Limit length to prevent abuse
    sanitized = sanitized[:1000]  # Max 1000 characters
    return sanitized.strip()

@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest, db: Session = Depends(get_db)):
    """
    Process a user query and return a response based on the scraped content
    """
    try:
        # Validate query
        is_valid, error_msg = validate_query(request.query)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)

        user_query = sanitize_query(request.query)
        
        # Generate embedding for the user query
        query_embedding = await generate_embedding(user_query)
        
        # Find relevant content based on the query embedding
        relevant_content = await find_relevant_content(query_embedding, top_k=5)
        
        # Define the out-of-context message
        out_of_context_message = "I cannot answer that question based on the available content. The information you're looking for is not present in the document."

        # Generate a response using the relevant content
        response = await generate_response(
            user_query=user_query,
            context_chunks=relevant_content,
            out_of_context_message=out_of_context_message
        )
        
        # Extract unique sources from the relevant content
        sources = list(set([chunk.get('source_url') for chunk in relevant_content if chunk.get('source_url')]))
        
        logger.info(f"Processed query: {user_query[:50]}...")
        return QueryResponse(response=response, sources=sources)
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.post("/query-stream")
async def process_query_stream(request: QueryRequest, db: Session = Depends(get_db)):
    """
    Process a user query and return a streaming response based on the scraped content
    """
    async def generate_streamed_response():
        try:
            # Validate query length
            if len(request.query.strip()) < 3:
                yield json.dumps({"error": "Query must be at least 3 characters long"})
                return

            if len(request.query.strip()) > 1000:
                yield json.dumps({"error": "Query must be less than 1000 characters long"})
                return

            user_query = sanitize_query(request.query)
            
            # Generate embedding for the user query
            query_embedding = await generate_embedding(user_query)
            
            # Find relevant content based on the query embedding
            relevant_content = await find_relevant_content(query_embedding, top_k=5)
            
            # Define the out-of-context message
            out_of_context_message = "I cannot answer that question based on the available content. The information you're looking for is not present in the document."

            # Generate a response using the relevant content
            response = await generate_response(
                user_query=user_query,
                context_chunks=relevant_content,
                out_of_context_message=out_of_context_message
            )
            
            # Extract unique sources from the relevant content
            sources = list(set([chunk.get('source_url') for chunk in relevant_content if chunk.get('source_url')]))
            
            logger.info(f"Processed streaming query: {user_query[:50]}...")
            
            # Yield the response in chunks
            chunk_size = 50  # Number of characters per chunk
            for i in range(0, len(response), chunk_size):
                chunk = response[i:i + chunk_size]
                yield json.dumps({"type": "response_chunk", "data": chunk}) + "\n"
            
            # Send sources at the end
            yield json.dumps({"type": "sources", "data": sources}) + "\n"
            yield json.dumps({"type": "done", "data": None}) + "\n"
                
        except Exception as e:
            logger.error(f"Error processing streaming query: {str(e)}")
            yield json.dumps({"error": f"Error processing query: {str(e)}"}) + "\n"

    return StreamingResponse(generate_streamed_response(), media_type="application/x-ndjson")