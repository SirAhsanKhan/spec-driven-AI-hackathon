from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models.content import Base

# Create database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initialize the database by creating all tables
    """
    Base.metadata.create_all(bind=engine)