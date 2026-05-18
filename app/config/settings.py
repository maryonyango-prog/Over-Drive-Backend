"""Application settings and configuration."""

import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite:///./test.db"
    )
    SQLALCHEMY_POOL_SIZE: int = 20
    SQLALCHEMY_POOL_RECYCLE: int = 3600

    # OpenAI API
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4-vision-preview"
    OPENAI_TIMEOUT: int = 60

    # API Settings
    API_TITLE: str = "Over-Drive Vehicle Analysis API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "AI-powered vehicle analysis and valuation service"

    # File Upload
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {".jpg", ".jpeg", ".png", ".webp"}

    # Analysis Settings
    MIN_CONFIDENCE_THRESHOLD: float = 60.0
    ANALYSIS_TIMEOUT: int = 300  # 5 minutes
    ENABLE_MARKET_ANALYSIS: bool = True
    ENABLE_PRICING_ENGINE: bool = True

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "./logs/app.log")

    # Security
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", "your-secret-key-change-in-production"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create global settings instance
settings = Settings()
