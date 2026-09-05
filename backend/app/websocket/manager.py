"""In-memory WebSocket room manager foundation."""

from collections import defaultdict
from uuid import UUID

from fastapi import WebSocket


class ConnectionManager:
    """Track active WebSocket connections grouped by meeting room."""

    def __init__(self) -> None:
        self.active_connections: dict[UUID, list[WebSocket]] = defaultdict(list)

    async def connect(self, meeting_id: UUID, websocket: WebSocket) -> None:
        """Accept and register a connection in a meeting room."""
        await websocket.accept()
        self.active_connections[meeting_id].append(websocket)

    def disconnect(self, meeting_id: UUID, websocket: WebSocket) -> None:
        """Remove a connection and discard empty room state."""
        connections = self.active_connections.get(meeting_id, [])
        if websocket in connections:
            connections.remove(websocket)
        if not connections:
            self.active_connections.pop(meeting_id, None)

    async def broadcast(self, meeting_id: UUID, message: str) -> None:
        """Send a text message to every active room connection."""
        for websocket in self.active_connections.get(meeting_id, []):
            await websocket.send_text(message)


connection_manager = ConnectionManager()

