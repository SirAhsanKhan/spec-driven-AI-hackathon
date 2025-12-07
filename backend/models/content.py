from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class ContentEntity(Base):
    __tablename__ = "content_entities"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)  # Raw scraped content
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    status = Column(String, default="processing")  # processing, completed, failed


class ContentChunk(Base):
    __tablename__ = "content_chunks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    content_id = Column(String, nullable=False)  # Foreign key to ContentEntity
    chunk_text = Column(Text, nullable=False)
    chunk_order = Column(Integer, nullable=False)
    # Embedding will be stored in Qdrant, not in SQLite
    created_at = Column(DateTime, default=func.now())