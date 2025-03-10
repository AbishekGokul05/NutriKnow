# backend/app/utils/config_loader.py

import os
from typing import Dict, Any, Optional
import logging
from pydantic import BaseSettings, Field

# Set up logging
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    """
    Configuration settings for the application, loaded from environment variables or a .env file.
    """
    # Database configuration
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    DATABASE_POOL_SIZE: int = Field(default=10, env="DATABASE_POOL_SIZE")
    DATABASE_MAX_OVERFLOW: int = Field(default=20, env="DATABASE_MAX_OVERFLOW")

    # API configuration
    API_HOST: str = Field(default="0.0.0.0", env="API_HOST")
    API_PORT: int = Field(default=8000, env="API_PORT")
    API_DEBUG: bool = Field(default=False, env="API_DEBUG")

    # Gemini API configuration
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")
    GEMINI_API_URL: str = Field(default="https://api.gemini.com/v1", env="GEMINI_API_URL")

    # Logging configuration
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_TO_CONSOLE: bool = Field(default=True, env="LOG_TO_CONSOLE")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

def load_config() -> Settings:
    """
    Load and validate configuration settings.

    Returns:
        Settings: An instance of the Settings class with loaded configuration.
    """
    try:
        config = Settings()
        logger.info("Configuration loaded successfully")
        return config
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        raise

def get_config_value(key: str, default: Optional[Any] = None) -> Any:
    """
    Get a configuration value by key.

    Args:
        key (str): The configuration key.
        default (Optional[Any]): Default value to return if the key is not found.

    Returns:
        Any: The configuration value or the default value.
    """
    try:
        config = load_config()
        return getattr(config, key, default)
    except Exception as e:
        logger.error(f"Error getting configuration value for key {key}: {e}")
        return default