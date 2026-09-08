"""FastAPI application factory for MeetAI."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.websocket import router as websocket_router
from app.api.v1.router import router as api_v1_router
from app.core.config import get_settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Application lifecycle hook reserved for future startup/shutdown work."""
    yield


def create_app() -> FastAPI:
    """Build and configure the MeetAI FastAPI application."""
    settings = get_settings()
    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Real-time AI meeting platform foundation.",
        lifespan=lifespan,
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.get("/health", tags=["system"])
    async def health_check() -> dict[str, str]:
        """Return a lightweight process health response."""
        return {"status": "healthy", "service": "meetai-backend"}

    @application.get("/api/health", tags=["system"])
    async def api_health_check() -> dict[str, str]:
        """Return API health and public version information."""
        return {"status": "healthy", "version": settings.APP_VERSION}

    application.include_router(api_v1_router, prefix="/api/v1")
    application.include_router(websocket_router)
    return application


app = create_app()

