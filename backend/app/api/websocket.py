"""WebSocket route connected to the foundation room manager."""

from uuid import UUID

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.websocket.manager import connection_manager

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/{meeting_id}")
async def meeting_websocket(websocket: WebSocket, meeting_id: UUID) -> None:
    """Accept a room connection and keep its lifecycle managed.

    Authentication and event routing are intentionally deferred to a later
    implementation day; this endpoint establishes the stable transport path.
    """
    await connection_manager.connect(meeting_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connection_manager.disconnect(meeting_id, websocket)

