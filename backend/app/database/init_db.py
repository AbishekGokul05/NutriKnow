from sqlalchemy.exc import SQLAlchemyError
from loguru import logger
from .base import Base, engine
from .models import User, Profile, History  # Import models directly from database.models

def init_db() -> None:
    """Initialize the database by creating all tables."""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except SQLAlchemyError as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise

if __name__ == "__main__":
    init_db() 