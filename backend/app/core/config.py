"""Environment-backed application settings."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables or .env."""

    APP_NAME: str = "MeetAI"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "postgresql+asyncpg://meetai:meetai@localhost:5432/meetai"
    POSTGRES_USER: str = "meetai"
    POSTGRES_PASSWORD: str = "meetai"
    POSTGRES_DB: str = "meetai"
    REDIS_URL: str = "redis://localhost:6379/0"
    JWT_SECRET_KEY: str = Field(default="change-me-in-development")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    BACKEND_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:5173"
    CORS_ORIGINS: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=".env",
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

