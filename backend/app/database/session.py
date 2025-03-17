# backend/app/database/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool
from loguru import logger
from app.config import get_settings
from contextlib import contextmanager
from typing import Generator
import secrets

settings = get_settings()

def create_database_engine():
    try:
        connect_args = {}
        if settings.DATABASE_URL.startswith('sqlite'):
            connect_args["check_same_thread"] = False

        engine = create_engine(
            settings.DATABASE_URL,
            poolclass=QueuePool,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            pool_timeout=settings.DB_POOL_TIMEOUT,
            pool_pre_ping=True,
            connect_args=connect_args,
            echo=False
        )
        return engine
    except Exception as e:
        logger.error(f"Failed to create database engine: {str(e)}")
        raise

try:
    engine = create_database_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except SQLAlchemyError as e:
    logger.error(f"Failed to create database session: {str(e)}")
    raise

def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get the database session.
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.
    Use this when you need a database session outside of a FastAPI endpoint.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        logger.error(f"Database context error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

print(secrets.token_urlsafe(32))