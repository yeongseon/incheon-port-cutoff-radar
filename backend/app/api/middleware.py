from __future__ import annotations

import time
from collections import defaultdict

from fastapi import Depends, HTTPException, Request, Security
from fastapi.security import APIKeyHeader

from app.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_REQUESTS = 60

_request_counts: dict[str, list[float]] = defaultdict(list)


async def verify_api_key(
    api_key: str | None = Security(api_key_header),
) -> str | None:
    if not settings.api_key:
        return None
    if api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return api_key


async def rate_limit(request: Request) -> None:
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW_SECONDS

    _request_counts[client_ip] = [t for t in _request_counts[client_ip] if t > window_start]

    if len(_request_counts[client_ip]) >= RATE_LIMIT_MAX_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Max {RATE_LIMIT_MAX_REQUESTS} requests per {RATE_LIMIT_WINDOW_SECONDS}s.",
        )

    _request_counts[client_ip].append(now)
