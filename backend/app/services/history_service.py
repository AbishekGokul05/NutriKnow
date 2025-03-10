# backend/app/services/history_service.py
from sqlalchemy.orm import Session
from app.models.database_models import History
from typing import List, Dict

def add_to_history(db: Session, user_id: int, product_name: str, analysis: Dict[str, List[str]]) -> History:
    """
    Adds a new entry to the user's history.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user.
        product_name (str): The name of the product.
        analysis (Dict[str, List[str]]): The analysis results for the product.

    Returns:
        History: The newly created history entry.
    """
    # Ensure only the last 10 entries are kept
    history_entries = db.query(History).filter(History.user_id == user_id).order_by(History.id.desc()).limit(10).all()
    if len(history_entries) >= 10:
        # Delete the oldest entry
        db.delete(history_entries[-1])

    # Create a new history entry
    new_entry = History(user_id=user_id, product_name=product_name, analysis=analysis)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

def get_history(db: Session, user_id: int) -> List[History]:
    """
    Fetches the last 10 history entries for a user.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user.

    Returns:
        List[History]: A list of the last 10 history entries.
    """
    return db.query(History).filter(History.user_id == user_id).order_by(History.id.desc()).limit(10).all()