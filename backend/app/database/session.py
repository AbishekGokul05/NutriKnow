# backend/app/database/session.py
from sqlalchemy.orm import Session
from .base import SessionLocal

def get_db():
    """
    Dependency to get the database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()