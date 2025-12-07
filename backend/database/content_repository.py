from sqlalchemy.orm import Session
from models.content import ContentEntity, ContentChunk
from typing import List
import uuid
from utils.logging import get_logger

logger = get_logger(__name__)

def store_content_entity(db: Session, url: str, title: str, content: str) -> ContentEntity:
    """
    Store the main content entity in SQLite
    """
    content_entity = ContentEntity(
        id=str(uuid.uuid4()),
        url=url,
        title=title,
        content=content,
        status="processing"
    )
    db.add(content_entity)
    db.commit()
    db.refresh(content_entity)
    
    logger.info(f"Stored content entity with ID: {content_entity.id}")
    return content_entity

def store_content_chunks(db: Session, content_id: str, chunks: List[str]) -> List[ContentChunk]:
    """
    Store content chunks in SQLite database
    """
    stored_chunks = []
    
    for i, chunk_text in enumerate(chunks):
        chunk = ContentChunk(
            id=str(uuid.uuid4()),
            content_id=content_id,
            chunk_text=chunk_text,
            chunk_order=i
        )
        db.add(chunk)
        stored_chunks.append(chunk)
    
    db.commit()
    
    logger.info(f"Stored {len(stored_chunks)} content chunks for content ID: {content_id}")
    return stored_chunks

def get_content_chunks(db: Session, content_id: str) -> List[ContentChunk]:
    """
    Retrieve content chunks for a specific content entity
    """
    chunks = db.query(ContentChunk).filter(ContentChunk.content_id == content_id).order_by(ContentChunk.chunk_order).all()
    return chunks

def update_content_status(db: Session, content_id: str, status: str):
    """
    Update the processing status of a content entity
    """
    content_entity = db.query(ContentEntity).filter(ContentEntity.id == content_id).first()
    if content_entity:
        content_entity.status = status
        db.commit()
        logger.info(f"Updated content {content_id} status to {status}")

def get_latest_content(db: Session):
    """
    Retrieve the most recently updated content entity
    """
    content_entity = db.query(ContentEntity).order_by(ContentEntity.updated_at.desc()).first()
    return content_entity

def update_content_source(db: Session, content_id: str, new_url: str):
    """
    Update the source URL of a content entity (for future updates)
    """
    content_entity = db.query(ContentEntity).filter(ContentEntity.id == content_id).first()
    if content_entity:
        content_entity.url = new_url
        db.commit()
        logger.info(f"Updated content {content_id} URL to {new_url}")