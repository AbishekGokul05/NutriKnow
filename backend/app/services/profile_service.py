# backend/app/services/profile_service.py
from sqlalchemy.orm import Session
from app.models.database_models import User
from typing import Optional, Dict, List

def get_user_profile(db: Session, username: str) -> Optional[User]:
    """
    Fetches a user's profile from the database.

    Args:
        db (Session): The database session.
        username (str): The username of the user.

    Returns:
        Optional[User]: The user's profile if found, otherwise None.
    """
    return db.query(User).filter(User.username == username).first()

def update_user_profile(
    db: Session,
    username: str,
    name: Optional[str] = None,
    profile_picture: Optional[str] = None,
    preferences: Optional[Dict[str, List[str]]] = None
) -> User:
    """
    Updates a user's profile in the database.

    Args:
        db (Session): The database session.
        username (str): The username of the user.
        name (Optional[str]): The new name of the user.
        profile_picture (Optional[str]): The new profile picture (URL or base64 encoded).
        preferences (Optional[Dict[str, List[str]]]): The new user preferences.

    Returns:
        User: The updated user profile.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise ValueError(f"User with username {username} not found")

    if name:
        user.name = name
    if profile_picture:
        user.profile_picture = profile_picture
    if preferences:
        user.preferences = preferences

    db.commit()
    db.refresh(user)
    return user

def get_user_preferences(db: Session, username: str) -> Optional[Dict[str, List[str]]]:
    """
    Fetches a user's preferences from the database.

    Args:
        db (Session): The database session.
        username (str): The username of the user.

    Returns:
        Optional[Dict[str, List[str]]]: The user's preferences if found, otherwise None.
    """
    user = db.query(User).filter(User.username == username).first()
    return user.preferences if user else None

def update_user_preferences(db: Session, username: str, preferences: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Updates a user's preferences in the database.

    Args:
        db (Session): The database session.
        username (str): The username of the user.
        preferences (Dict[str, List[str]]): The new user preferences.

    Returns:
        Dict[str, List[str]]: The updated user preferences.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise ValueError(f"User with username {username} not found")

    user.preferences = preferences
    db.commit()
    db.refresh(user)
    return user.preferences