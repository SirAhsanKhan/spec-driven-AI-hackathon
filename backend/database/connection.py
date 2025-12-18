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
        # Adjust connection settings for serverless environments like Vercel
        connect_args = {
            "connect_timeout": 10,  # Timeout for establishing connection
        }

        # For Neon specifically, we may need to add extra parameters
        if "neon" in DATABASE_URL.lower():
            connect_args["sslmode"] = "require"

        engine = create_engine(
            DATABASE_URL,
            pool_size=2,           # Smaller pool size for serverless
            max_overflow=5,        # Limit overflow connections
            pool_pre_ping=True,    # Verify connections before use
            pool_recycle=300,      # Recycle connections every 5 minutes
            pool_timeout=30,       # Timeout for getting connection from pool
            echo=False,            # Set to True only for debugging
            connect_args=connect_args
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
    # In serverless environments like Vercel, we need to be careful about
    # when and how we initialize the database to avoid cold start issues

    # Check if we're in a Vercel environment
    if os.getenv("VERCEL_ENV"):
        print("Running in Vercel environment - skipping table creation in init_db()")
        # In Vercel, tables should be created via migrations during the build process
        # rather than at runtime to avoid timeout issues
        return

    Base.metadata.create_all(bind=engine)