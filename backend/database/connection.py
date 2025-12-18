from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models.content import Base
import os

def create_db_engine():
    """Create database engine with appropriate settings for the environment"""
    if "sqlite" in DATABASE_URL.lower():
        # SQLite settings (for local development)
        engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
            pool_pre_ping=True
        )
    else:
        # PostgreSQL settings (for production, including Neon)
        engine = create_engine(
            DATABASE_URL,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=300,  # Recycle connections every 5 minutes
            echo=False  # Set to True only for debugging
        )
    
    return engine

# Create database engine
engine = create_db_engine()

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initialize the database by creating all tables
    """
    # Check if we're in a Vercel environment
    if os.getenv("VERCEL_ENV"):
        print("Running in Vercel environment - skipping table creation in init_db()")
        # In Vercel, you should run migrations separately or during build
        # rather than creating tables at runtime
        return
    
    Base.metadata.create_all(bind=engine)