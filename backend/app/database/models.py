# backend/app/database/models.py
from sqlalchemy import Column, Integer, String, JSON
from .base import Base

# User model for the database
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # Primary key
    username = Column(String, unique=True, index=True)  # Unique username
    name = Column(String, nullable=True)  # User's name (optional)
    profile_picture = Column(String, nullable=True)  # URL or base64 encoded image (optional)
    preferences = Column(JSON, nullable=True)  # User preferences (e.g., dietary restrictions, allergies, habits)

# History model for the database
class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)  # Primary key
    user_id = Column(Integer, index=True)  # Foreign key to the users table
    product_name = Column(String)  # Name of the product
    analysis = Column(JSON)  # Analysis results for the product (e.g., ingredients, allergens, harmful substances)