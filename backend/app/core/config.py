"""
Application configuration settings.
"""
import os
from typing import List


class Settings:
    """Application settings."""

    # API Settings
    API_TITLE: str = "NoteHub API"
    API_VERSION: str = "1.0.0"

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret")  # Change in production!
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ]

    # Production CORS - read from environment variable
    if origins_env := os.getenv("CORS_ORIGINS"):
        CORS_ORIGINS = origins_env.split(",")

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql+asyncpg://postgres:postgres@localhost:5432/notehub"
    )
    
    # Render.com provides postgresql:// but we need postgresql+asyncpg://
    # Automatically convert for compatibility with asyncpg driver
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)


settings = Settings()
