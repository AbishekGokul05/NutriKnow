# backend/app/database/base.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create the SQLAlchemy declarative base
Base = declarative_base()

# Database URL (SQLite for development)
SQLALCHEMY_DATABASE_URL = "sqlite:///./nutriknow.db"

# Create the SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a configured SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Make sure all models are imported before creating tables
__all__ = ["Base", "engine", "SessionLocal"]