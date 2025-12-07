from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from config import get_content_url
from services.scraping_service import scrape_content_from_url
from services.content_service import clean_content, preprocess_content, create_content_chunks
from database.content_repository import store_content_entity, store_content_chunks, update_content_status
from services.embedding_service import generate_embeddings
from services.vector_service import store_embeddings_batch
from typing import Optional
import uuid
from utils.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)

# Dictionary to store job progress (in production, use a proper task queue like Celery)
initialization_jobs = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/initialize")
async def initialize_content():
    """
    Initialize content from the pre-stored URL in environment variables
    """
    content_url = get_content_url()
    if not content_url:
        raise HTTPException(status_code=400, detail="CONTENT_URL not configured in environment")
    
    job_id = str(uuid.uuid4())
    initialization_jobs[job_id] = {"status": "processing", "progress": 0, "url": content_url}
    
    # Process content in the background
    try:
        # Step 1: Scrape content
        raw_content = await scrape_content_from_url(content_url)
        if not raw_content:
            initialization_jobs[job_id]["status"] = "failed"
            initialization_jobs[job_id]["error"] = "Failed to scrape content from URL"
            return {"status": "failed", "message": "Failed to scrape content from URL", "job_id": job_id}
        
        initialization_jobs[job_id]["progress"] = 20
        
        # Step 2: Clean and preprocess content
        cleaned_content = clean_content(raw_content)
        processed_content = preprocess_content(cleaned_content)

        # Validate content before processing
        from services.content_service import validate_content
        if not validate_content(processed_content):
            initialization_jobs[job_id]["status"] = "failed"
            initialization_jobs[job_id]["error"] = "Content validation failed"
            return {"status": "failed", "message": "Content validation failed", "job_id": job_id}

        initialization_jobs[job_id]["progress"] = 40
        
        # Step 3: Create content entity in database
        db = next(get_db())
        try:
            content_entity = store_content_entity(
                db=db,
                url=content_url,
                title="Content from " + content_url,
                content=processed_content
            )
            initialization_jobs[job_id]["progress"] = 50
            
            # Step 4: Create chunks
            chunks = create_content_chunks(processed_content)
            initialization_jobs[job_id]["progress"] = 55
            
            # Step 5: Store chunks in SQLite
            stored_chunks = store_content_chunks(db, content_entity.id, chunks)
            initialization_jobs[job_id]["progress"] = 60
            
            # Step 6: Generate embeddings for chunks
            chunk_texts = [chunk.chunk_text for chunk in stored_chunks]
            embeddings = await generate_embeddings(chunk_texts)
            # Update progress incrementally as embeddings are generated
            initialization_jobs[job_id]["progress"] = 75

            # Step 7: Store embeddings in Qdrant
            chunk_embeddings = [(chunk.id, embedding) for chunk, embedding in zip(stored_chunks, embeddings)]
            content_metadata_list = [{
                "content_id": chunk.content_id,
                "chunk_order": chunk.chunk_order,
                "source_url": content_url,
                "chunk_text": chunk.chunk_text  # This will be filtered out in vector_service
            } for chunk in stored_chunks]

            await store_embeddings_batch(chunk_embeddings, content_metadata_list)
            initialization_jobs[job_id]["progress"] = 95
            
            # Step 8: Update content status to completed
            update_content_status(db, content_entity.id, "completed")
            initialization_jobs[job_id]["progress"] = 100
            initialization_jobs[job_id]["status"] = "completed"
            
        finally:
            db.close()
        
        return {"status": "initializing", "job_id": job_id}
    
    except Exception as e:
        logger.error(f"Error during content initialization: {str(e)}")
        initialization_jobs[job_id]["status"] = "failed"
        initialization_jobs[job_id]["error"] = str(e)
        return {"status": "failed", "message": str(e), "job_id": job_id}

@router.get("/initialize/{job_id}")
async def get_initialization_status(job_id: str):
    """
    Check the status of an initialization job
    """
    if job_id not in initialization_jobs:
        raise HTTPException(status_code=404, detail="Job ID not found")
    
    job_info = initialization_jobs[job_id]
    return job_info