from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, patch

from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


MOCK_CACHE_DATA = {
    "congestion_status": "normal",
    "congestion_time_minutes": 15,
    "observed_at": "2026-07-10T13:00:00+00:00",
}


@pytest.mark.anyio
async def test_health_endpoint(client: AsyncClient):
    with patch("app.cache.redis_client") as mock_redis:
        mock_redis.ping = AsyncMock(return_value=True)
        resp = await client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] in ("ok", "degraded")
    assert "version" in data


@pytest.mark.anyio
async def test_terminals_endpoint(client: AsyncClient):
    resp = await client.get("/api/v1/terminals")
    assert resp.status_code == 200
    terminals = resp.json()
    assert len(terminals) == 5
    codes = {t["terminal_code"] for t in terminals}
    assert "ICT" in codes
    assert "E1" in codes


@pytest.mark.anyio
async def test_evaluate_valid_request(client: AsyncClient):
    with patch("app.services.dispatch_service.cache_get", new_callable=AsyncMock) as mock_cache:
        mock_cache.return_value = MOCK_CACHE_DATA
        resp = await client.post(
            "/api/v1/risk/evaluate",
            json={
                "origin_zone_id": "SONGDO",
                "terminal_code": "ICT",
                "cut_off_at": "2026-07-10T17:00:00+09:00",
                "conservative_mode": False,
                "manual_buffer_minutes": None,
            },
        )

    assert resp.status_code == 200
    data = resp.json()
    assert "risk_score" in data
    assert "risk_level" in data
    assert "on_time_probability" in data
    assert "latest_safe_dispatch_at" in data
    assert "verdict" in data
    assert "reason_items" in data
    assert "source_freshness" in data
    assert "evaluation_id" in data
    assert data["result_status"] in ("FULL", "DEGRADED")
    assert data["engine_version"].startswith("v")


@pytest.mark.anyio
async def test_evaluate_unsupported_terminal(client: AsyncClient):
    resp = await client.post(
        "/api/v1/risk/evaluate",
        json={
            "origin_zone_id": "SONGDO",
            "terminal_code": "INVALID_TERMINAL",
            "cut_off_at": "2026-07-10T17:00:00+09:00",
            "conservative_mode": False,
        },
    )
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_evaluate_missing_required_fields(client: AsyncClient):
    resp = await client.post(
        "/api/v1/risk/evaluate",
        json={
            "origin_zone_id": "SONGDO",
        },
    )
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_simulate_valid_request(client: AsyncClient):
    with patch("app.services.dispatch_service.cache_get", new_callable=AsyncMock) as mock_cache:
        mock_cache.return_value = MOCK_CACHE_DATA
        resp = await client.post(
            "/api/v1/risk/simulate",
            json={
                "origin_zone_id": "SONGDO",
                "terminal_code": "ICT",
                "cut_off_at": "2026-07-10T17:00:00+09:00",
                "scenario_offsets_minutes": [0, -15, -30, -60],
            },
        )

    assert resp.status_code == 200
    data = resp.json()
    assert "base_scenario" in data
    assert "scenarios" in data
    assert len(data["scenarios"]) == 4
    for scenario in data["scenarios"]:
        assert "risk_score" in scenario
        assert "risk_level" in scenario
        assert "on_time_probability" in scenario


@pytest.mark.anyio
async def test_simulate_unsupported_terminal(client: AsyncClient):
    resp = await client.post(
        "/api/v1/risk/simulate",
        json={
            "origin_zone_id": "SONGDO",
            "terminal_code": "NONEXIST",
            "cut_off_at": "2026-07-10T17:00:00+09:00",
            "scenario_offsets_minutes": [0],
        },
    )
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_evaluate_degraded_when_sources_missing(client: AsyncClient):
    with patch("app.services.dispatch_service.cache_get", new_callable=AsyncMock) as mock_cache:
        mock_cache.return_value = None
        resp = await client.post(
            "/api/v1/risk/evaluate",
            json={
                "origin_zone_id": "SONGDO",
                "terminal_code": "ICT",
                "cut_off_at": "2026-07-10T17:00:00+09:00",
                "conservative_mode": False,
            },
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["result_status"] == "FAILED"
    assert len(data["warnings"]) > 0


@pytest.mark.anyio
async def test_evaluate_with_conservative_mode(client: AsyncClient):
    with patch("app.services.dispatch_service.cache_get", new_callable=AsyncMock) as mock_cache:
        mock_cache.return_value = MOCK_CACHE_DATA
        resp_normal = await client.post(
            "/api/v1/risk/evaluate",
            json={
                "origin_zone_id": "SONGDO",
                "terminal_code": "ICT",
                "cut_off_at": "2026-07-10T17:00:00+09:00",
                "conservative_mode": False,
            },
        )
        resp_conservative = await client.post(
            "/api/v1/risk/evaluate",
            json={
                "origin_zone_id": "SONGDO",
                "terminal_code": "ICT",
                "cut_off_at": "2026-07-10T17:00:00+09:00",
                "conservative_mode": True,
            },
        )

    normal = resp_normal.json()
    conservative = resp_conservative.json()
    assert conservative["estimated_total_minutes"] >= normal["estimated_total_minutes"]
