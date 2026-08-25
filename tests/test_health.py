"""Health endpoint: DB ping + version."""

from __future__ import annotations

from httpx import AsyncClient


async def test_health_ok(client: AsyncClient) -> None:
    resp = await client.get("/v1/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["version"]
    # Request-id middleware echoes the header.
    assert resp.headers["X-Request-ID"]
    # Security headers present.
    assert resp.headers["X-Content-Type-Options"] == "nosniff"
