# backend/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

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
    
    # PostgreSQL Database Configuration
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "inventory_user"
    POSTGRES_PASSWORD: str = "secure_password"
    POSTGRES_DB: str = "inventory_db"
    
    # Celery Configuration
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """Construct the SQLAlchemy database URI from components."""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
        )

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
