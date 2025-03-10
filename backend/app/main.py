# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import (
    chat,
    ingredients,
    comparison,
    allergens,
    harmful_substances,
    nutritional_benefits,
    user_insights,
    alternatives,
    profile,  # New: Profile endpoint
    history,  # New: History endpoint
)

# Initialize FastAPI app
app = FastAPI(
    title="NutriKnow API",
    description="API for NutriKnow - A product analysis and recommendation system.",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(chat.router, prefix="/api/v1")
app.include_router(ingredients.router, prefix="/api/v1")
app.include_router(comparison.router, prefix="/api/v1")
app.include_router(allergens.router, prefix="/api/v1")
app.include_router(harmful_substances.router, prefix="/api/v1")
app.include_router(nutritional_benefits.router, prefix="/api/v1")
app.include_router(alternatives.router, prefix="/api/v1")
app.include_router(profile.router, prefix="/api/v1")  # New: Profile router
app.include_router(history.router, prefix="/api/v1")  # New: History router

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to NutriKnow API!"}