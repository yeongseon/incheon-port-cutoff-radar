"""
Mock data ingestion scheduler.
In production, these would call real external APIs.
For MVP demo, populates Redis with sample snapshot data.
"""

from __future__ import annotations

import json
import random
from datetime import datetime, timezone

from app.cache import redis_client, source_cache_key
from app.config import settings


def _random_congestion() -> dict:
    status = random.choice(["smooth", "normal", "congested", "severe"])
    time_map = {"smooth": 5, "normal": 15, "congested": 30, "severe": 50}
    return {
        "congestion_status": status,
        "congestion_time_minutes": time_map[status] + random.randint(-3, 3),
        "observed_at": datetime.now(timezone.utc).isoformat(),
    }


def _random_gate_entry() -> dict:
    return {
        "vehicle_count": random.randint(5, 80),
        "entry_type": "container",
        "observed_at": datetime.now(timezone.utc).isoformat(),
    }


def _random_traffic(origin: str, terminal: str) -> dict:
    return {
        "average_speed_kph": random.uniform(15, 70),
        "estimated_travel_minutes": random.uniform(15, 60),
        "observed_at": datetime.now(timezone.utc).isoformat(),
    }


def _random_operation() -> dict:
    return {
        "expected_arrival_applied": random.choice([True, False]),
        "raw_status_note": random.choice(["Normal operation", "Slight delay", "On schedule"]),
        "observed_at": datetime.now(timezone.utc).isoformat(),
    }


TERMINALS = ["ICT", "E1", "SNCT", "HJIT", "SGT"]
ZONES = ["SONGDO", "NAMDONG", "SEOGU", "YEONSU", "BUPYEONG", "SIHEUNG", "ANSAN"]


async def ingest_all_sources() -> None:
    ttl = settings.cache_ttl_seconds

    for terminal in TERMINALS:
        congestion_key = source_cache_key("terminal_congestion", terminal)
        await redis_client.set(
            congestion_key, json.dumps(_random_congestion(), default=str), ex=ttl
        )

        gate_key = source_cache_key("gate_entry", terminal)
        await redis_client.set(gate_key, json.dumps(_random_gate_entry(), default=str), ex=ttl)

        operation_key = source_cache_key("terminal_operation", terminal)
        await redis_client.set(operation_key, json.dumps(_random_operation(), default=str), ex=ttl)

        for zone in ZONES:
            traffic_key = source_cache_key("traffic", f"{zone}:{terminal}")
            await redis_client.set(
                traffic_key,
                json.dumps(_random_traffic(zone, terminal), default=str),
                ex=ttl,
            )
