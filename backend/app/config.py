from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from functools import lru_cache
import json
from loguru import logger

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "NutriKnow API"
    VERSION: str = "1.0.0"
    
    # CORS Settings
    BACKEND_CORS_ORIGINS_RAW: str = '["http://localhost:5173"]'
    
    @property
    def BACKEND_CORS_ORIGINS(self) -> List[str]:
        try:
            return json.loads(self.BACKEND_CORS_ORIGINS_RAW)
        except:
            return ["http://localhost:5173"]
    
    # Database Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./nutriknow.db")
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    
    # JWT Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-jwt")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Gemini API Settings
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GEMINI_MAX_RETRIES: int = 3
    GEMINI_TIMEOUT: int = 30
    
    # Redis Settings (for caching)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_TIMEOUT: int = 5
    CACHE_TTL: int = 3600  # 1 hour
    
    # Logging Settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png"]
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"  # Allow extra fields in the settings

@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    logger.debug(f"Loaded GEMINI_API_KEY from environment: '{settings.GEMINI_API_KEY}'")
    logger.debug(f"Loaded GOOGLE_API_KEY from environment: '{settings.GOOGLE_API_KEY}'")
    return settings 