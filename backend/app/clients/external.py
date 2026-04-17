from __future__ import annotations

import httpx

from app.config import settings

TIMEOUT = httpx.Timeout(10.0, connect=5.0)


class PortCongestionClient:
    def __init__(self) -> None:
        self.base_url = settings.port_api_base_url
        self.api_key = settings.port_api_key

    async def fetch_congestion(self, terminal_code: str) -> dict | None:
        if not self.base_url:
            return None
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                resp = await client.get(
                    f"{self.base_url}/congestion",
                    params={"terminal": terminal_code, "apiKey": self.api_key},
                )
                resp.raise_for_status()
                return resp.json()
        except (httpx.HTTPError, Exception):
            return None

    async def fetch_operation(self, terminal_code: str) -> dict | None:
        if not self.base_url:
            return None
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                resp = await client.get(
                    f"{self.base_url}/operation",
                    params={"terminal": terminal_code, "apiKey": self.api_key},
                )
                resp.raise_for_status()
                return resp.json()
        except (httpx.HTTPError, Exception):
            return None

    async def fetch_gate_entry(self, terminal_code: str) -> dict | None:
        if not self.base_url:
            return None
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                resp = await client.get(
                    f"{self.base_url}/gate-entry",
                    params={"terminal": terminal_code, "apiKey": self.api_key},
                )
                resp.raise_for_status()
                return resp.json()
        except (httpx.HTTPError, Exception):
            return None


class TrafficClient:
    def __init__(self) -> None:
        self.base_url = settings.traffic_api_base_url
        self.api_key = settings.traffic_api_key

    async def fetch_traffic(self, origin_zone_id: str, terminal_code: str) -> dict | None:
        if not self.base_url:
            return None
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                resp = await client.get(
                    f"{self.base_url}/traffic",
                    params={
                        "origin": origin_zone_id,
                        "destination": terminal_code,
                        "apiKey": self.api_key,
                    },
                )
                resp.raise_for_status()
                return resp.json()
        except (httpx.HTTPError, Exception):
            return None


port_client = PortCongestionClient()
traffic_client = TrafficClient()
