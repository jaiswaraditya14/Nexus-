import httpx
import pytest

from app.main import create_app


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("/health", {"status": "healthy", "service": "meetai-backend"}),
        ("/api/health", {"status": "healthy", "version": "1.0.0"}),
    ],
)
async def test_health_endpoints(path: str, expected: dict[str, str]) -> None:
    transport = httpx.ASGITransport(app=create_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get(path)

    assert response.status_code == 200
    assert response.json() == expected


@pytest.mark.asyncio
async def test_openapi_metadata_and_docs() -> None:
    transport = httpx.ASGITransport(app=create_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        schema_response = await client.get("/openapi.json")
        docs_response = await client.get("/docs")

    assert schema_response.status_code == 200
    assert schema_response.json()["info"] == {
        "title": "MeetAI API",
        "description": "Real-time AI meeting platform foundation.",
        "version": "1.0.0",
    }
    assert docs_response.status_code == 200
