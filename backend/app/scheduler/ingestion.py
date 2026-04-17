from __future__ import annotations

import json
import logging
import random
from datetime import datetime, timezone

from app.cache import redis_client, source_cache_key
from app.clients.external import port_client, traffic_client
from app.config import settings
from app.normalizers.source_normalizer import (
    normalize_congestion,
    normalize_gate_entry,
    normalize_operation,
    normalize_traffic,
)

logger = logging.getLogger(__name__)

TERMINALS = ["ICT", "E1", "SNCT", "HJIT", "SGT"]
ZONES = ["SONGDO", "NAMDONG", "SEOGU", "YEONSU", "BUPYEONG", "SIHEUNG", "ANSAN"]


def _mock_congestion() -> dict:
    status = random.choice(["smooth", "normal", "congested", "severe"])
    time_map = {"smooth": 5, "normal": 15, "congested": 30, "severe": 50}
    return {
        "congestion_status": status,
        "congestion_time_minutes": time_map[status] + random.randint(-3, 3),
        "observed_at": datetime.now(timezone.utc).isoformat(),
    }


def _mock_gate_entry() -> dict:
    return {
        "vehicle_count": random.randint(5, 80),
        "entry_type": "container",
        "observed_at": datetime.now(timezone.utc).isoformat(),
    }


def _mock_traffic() -> dict:
    return {
        "average_speed_kph": random.uniform(15, 70),
        "estimated_travel_minutes": random.uniform(15, 60),
        "observed_at": datetime.now(timezone.utc).isoformat(),
    }


def _mock_operation() -> dict:
    return {
        "expected_arrival_applied": random.choice([True, False]),
        "raw_status_note": random.choice(["Normal operation", "Slight delay", "On schedule"]),
        "observed_at": datetime.now(timezone.utc).isoformat(),
    }


async def _cache_normalized(key: str, data: dict | None, ttl: int) -> None:
    if data is not None:
        await redis_client.set(key, json.dumps(data, default=str), ex=ttl)


async def ingest_terminal_data(terminal: str) -> None:
    ttl = settings.cache_ttl_seconds

    raw_congestion = await port_client.fetch_congestion(terminal)
    if raw_congestion is None:
        raw_congestion = _mock_congestion()
    normalized = normalize_congestion(raw_congestion)
    await _cache_normalized(source_cache_key("terminal_congestion", terminal), normalized, ttl)

    raw_operation = await port_client.fetch_operation(terminal)
    if raw_operation is None:
        raw_operation = _mock_operation()
    normalized = normalize_operation(raw_operation)
    await _cache_normalized(source_cache_key("terminal_operation", terminal), normalized, ttl)

    raw_gate = await port_client.fetch_gate_entry(terminal)
    if raw_gate is None:
        raw_gate = _mock_gate_entry()
    normalized = normalize_gate_entry(raw_gate)
    await _cache_normalized(source_cache_key("gate_entry", terminal), normalized, ttl)


async def ingest_traffic_data(zone: str, terminal: str) -> None:
    ttl = settings.cache_ttl_seconds

    raw_traffic = await traffic_client.fetch_traffic(zone, terminal)
    if raw_traffic is None:
        raw_traffic = _mock_traffic()
    normalized = normalize_traffic(raw_traffic)
    await _cache_normalized(source_cache_key("traffic", f"{zone}:{terminal}"), normalized, ttl)


async def ingest_all_sources() -> None:
    for terminal in TERMINALS:
        try:
            await ingest_terminal_data(terminal)
        except Exception as e:
            logger.warning("Failed to ingest terminal %s: %s", terminal, e)

        for zone in ZONES:
            try:
                await ingest_traffic_data(zone, terminal)
            except Exception as e:
                logger.warning("Failed to ingest traffic %s->%s: %s", zone, terminal, e)

    logger.info("Data ingestion cycle complete at %s", datetime.now(timezone.utc).isoformat())
