# backend/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import List, Union

class Settings(BaseSettings):
    """
    Centralized application settings using Pydantic.
    Reads configuration from environment variables or a .env file.
    """
    # Application settings
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "a_very_secret_key" # Should be loaded from .env in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    BACKEND_CORS_ORIGINS: Union[str, List[str]] = "http://localhost:3000"

    @property
    def allowed_origins(self) -> List[str]:
        if isinstance(self.BACKEND_CORS_ORIGINS, str):
            return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]
        return self.BACKEND_CORS_ORIGINS

    # Database URL - Pydantic will automatically read this from the environment.
    # This is the single source of truth for the database connection.
    DATABASE_URL: str = "postgresql://inventory_user:secure_password@localhost/inventory_db"
    
    # Celery Configuration
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(
      case_sensitive=True, 
      env_file=".env"
    )

@lru_cache()
def get_settings():
    """
    Returns the settings instance.
    The lru_cache decorator ensures this is only created once.
    """
    return Settings()

settings = get_settings()
