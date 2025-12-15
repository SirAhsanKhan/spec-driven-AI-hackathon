from fastapi import APIRouter
from config import get_content_url, get_content_urls
from database.connection import SessionLocal
from database.content_repository import get_latest_content, get_content_chunks
from datetime import datetime

router = APIRouter()

@router.get("/status")
async def get_system_status():
    """
    Get system status and initialization information
    """
    content_urls = get_content_urls()
    primary_content_url = get_content_url()

    db = SessionLocal()
    try:
        # Check if there's any content in the database
        latest_content = get_latest_content(db)
        content_initialized = latest_content is not None

        return {
            "initialized": content_initialized,
            "content_sources": content_urls,
            "primary_content_source": primary_content_url,
            "last_content_update": latest_content.updated_at.isoformat() if latest_content else None,
            "last_updated": datetime.now().isoformat(),
            "status": "ready" if content_initialized or content_urls else "not_configured"
        }
    finally:
        db.close()