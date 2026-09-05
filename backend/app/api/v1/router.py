"""Versioned API router composition."""

from fastapi import APIRouter

from app.api.v1 import audio, auth, meetings, search

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(meetings.router, prefix="/meetings", tags=["meetings"])
router.include_router(audio.router, prefix="/audio", tags=["audio"])
router.include_router(search.router, prefix="/search", tags=["search"])


@router.get("", tags=["system"])
async def api_version() -> dict[str, str]:
    """Confirm that the versioned API namespace is available."""
    return {"version": "v1", "status": "available"}

