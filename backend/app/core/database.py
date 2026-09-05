"""Async SQLAlchemy engine, session dependency, and declarative base."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for future SQLAlchemy models."""


def _async_database_url(url: str) -> str:
    """Normalize common PostgreSQL URLs for the async SQLAlchemy driver."""
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+asyncpg://", 1)
    return url


settings = get_settings()
engine: AsyncEngine = create_async_engine(_async_database_url(settings.DATABASE_URL), pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield one database session per request and close it afterward."""
    async with AsyncSessionLocal() as session:
        yield session


async def dispose_engine() -> None:
    """Dispose the shared engine during application shutdown when needed."""
    await engine.dispose()

