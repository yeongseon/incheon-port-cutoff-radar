"""Redis cache client."""

from __future__ import annotations

import json
from datetime import datetime

import redis.asyncio as redis

from app.config import settings

redis_client = redis.from_url(settings.redis_url, decode_responses=True)


async def cache_get(key: str) -> dict | None:
    raw = await redis_client.get(key)
    if raw is None:
        return None
    return json.loads(raw)


async def cache_set(key: str, data: dict, ttl: int | None = None) -> None:
    ttl = ttl or settings.cache_ttl_seconds
    await redis_client.set(key, json.dumps(data, default=str), ex=ttl)


async def cache_get_freshness(key: str) -> tuple[dict | None, int | None]:
    """Get cached data and its age in seconds."""
    raw = await redis_client.get(key)
    ttl = await redis_client.ttl(key)
    if raw is None:
        return None, None
    data = json.loads(raw)
    age = settings.cache_ttl_seconds - ttl if ttl and ttl > 0 else None
    return data, age


def source_cache_key(source_type: str, identifier: str) -> str:
    return f"source:{source_type}:{identifier}"
