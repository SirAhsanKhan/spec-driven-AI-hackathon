from fastapi import APIRouter
from config import get_content_url
from database.connection import SessionLocal
from database.content_repository import get_content_chunks
from datetime import datetime

router = APIRouter()

@router.get("/status")
async def get_system_status():
    """
    Get system status and initialization information
    """
    content_url = get_content_url()
    
    db = SessionLocal()
    try:
        # For now, we'll check if there are any content chunks in the database
        # In a real implementation, you might want to track initialization status differently
        # This is a simplified approach for the MVP
        try:
            # Try to get some content chunks to determine if content is initialized
            chunks = get_content_chunks(db, "dummy_id")  # This will return an empty list if no content
            content_initialized = len(chunks) > 0
        except:
            content_initialized = False
            
        return {
            "initialized": content_initialized,
            "content_source": content_url,
            "last_updated": datetime.now().isoformat(),
            "status": "ready" if content_initialized or content_url else "not_configured"
        }
    finally:
        db.close()