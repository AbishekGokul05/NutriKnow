# backend/app/database/__init__.py
from .base import Base, engine, SessionLocal
from .session import get_db, get_db_context
from .models import User, History

# Expose all database components for easy access
__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "get_db",
    "get_db_context",
    "User",
    "History",
]