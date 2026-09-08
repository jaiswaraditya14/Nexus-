"""Environment-backed application settings."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


_BACKEND_DIR = Path(__file__).resolve().parents[2]
_REPOSITORY_DIR = _BACKEND_DIR.parent


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables or .env."""

    APP_NAME: str = "MeetAI API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "postgresql://postgres:postgrespassword@localhost:5432/meetai_db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgrespassword"
    POSTGRES_DB: str = "meetai_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"
    JWT_SECRET_KEY: str = Field(default="change-me-in-development")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    OPENAI_API_KEY: str = ""
    AUDIO_UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE_MB: int = 25
    BACKEND_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:5173"
    CORS_ORIGINS: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=(_BACKEND_DIR / ".env", _REPOSITORY_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        """Return comma-separated CORS origins as a normalized list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings instance."""
    return Settings()

