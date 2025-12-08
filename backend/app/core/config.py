from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

# Define o caminho base do backend
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    # App
    APP_NAME: str = "eFootball Coach API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_KEY: str
    
    # Groq AI
    GROQ_API_KEY: str
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Rate Limiting
    FREE_TIER_DAILY_LIMIT: int = 5
    PREMIUM_TIER_DAILY_LIMIT: int = 100
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    @property
    def origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = 'utf-8'
        case_sensitive = False
        extra = "ignore"


settings = Settings()
