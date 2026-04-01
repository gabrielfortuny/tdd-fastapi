from unittest.mock import AsyncMock, patch

import pytest


def test_health(test_app_with_db):
    response = test_app_with_db.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "environment": "dev",
        "testing": True,
        "db": "ok",
    }


@pytest.mark.anyio
async def test_health_db_unavailable(test_app):
    with patch("app.api.health.connections") as mock_connections:
        mock_db = AsyncMock()
        mock_db.execute_query.side_effect = Exception("connection refused")
        mock_connections.get.return_value = mock_db

        response = test_app.get("/health")

    assert response.status_code == 503
    body = response.json()
    assert body["db"] == "unavailable"
    assert body["status"] == "degraded"
