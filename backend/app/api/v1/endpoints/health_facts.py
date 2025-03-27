# backend/app/api/v1/endpoints/health_facts.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from app.services.gemini_service import generate_health_fact
from loguru import logger

# Initialize router
router = APIRouter(prefix="/health-facts", tags=["health-facts"])

# Pydantic models for response
class HealthFactResponse(BaseModel):
    fact: str

@router.get("/", response_model=HealthFactResponse)
async def get_health_fact(previous_facts: Optional[List[str]] = Query(None)):
    """
    Get a random health fact.
    
    - **previous_facts**: Optional list of previously shown facts to avoid repetition
    """
    try:
        fact = generate_health_fact(previous_facts)
        return HealthFactResponse(fact=fact)
    except Exception as e:
        logger.error(f"Error retrieving health fact: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate health fact: {str(e)}") 