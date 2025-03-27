# backend/app/main.py
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys
from typing import List

from app.config import get_settings
from app.middleware.error_handler import error_handler_middleware
from app.api.v1.endpoints import (
    chat,
    ingredients,
    comparison,
    allergens,
    harmful_substances,
    nutritional_benefits,
    alternatives,
    profile,
    history,
    health_facts,
)

# Get settings
settings = get_settings()

# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=settings.LOG_LEVEL
)

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for NutriKnow - A product analysis and recommendation system.",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add middleware
app.middleware("http")(error_handler_middleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# Include API routers
api_prefix = settings.API_V1_STR
app.include_router(chat.router, prefix=api_prefix)
app.include_router(ingredients.router, prefix=api_prefix)
app.include_router(comparison.router, prefix=api_prefix)
app.include_router(allergens.router, prefix=api_prefix)
app.include_router(harmful_substances.router, prefix=api_prefix)
app.include_router(nutritional_benefits.router, prefix=api_prefix)
app.include_router(alternatives.router, prefix=api_prefix)
app.include_router(profile.router, prefix=api_prefix)
app.include_router(history.router, prefix=api_prefix)
app.include_router(health_facts.router, prefix=api_prefix)

# Root endpoint
@app.get("/")
async def read_root():
    return {
        "status": "success",
        "message": f"Welcome to {settings.PROJECT_NAME}!",
        "version": settings.VERSION
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.PROJECT_NAME} version {settings.VERSION}")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.PROJECT_NAME}")

# Legacy endpoint - will be deprecated
@app.get("/api/v1/health-fact/")
async def get_health_fact(previous_facts: List[str] = Query(None)):
    """
    Generate a random health fact. 
    DEPRECATED: Use /api/v1/health-facts/ endpoint instead.
    """
    try:
        from app.services.gemini_service import generate_health_fact
        fact = generate_health_fact(previous_facts)
        return {"fact": fact}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))