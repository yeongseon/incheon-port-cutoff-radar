from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def normalize_congestion(raw: dict[str, Any] | None) -> dict[str, Any] | None:
    if raw is None:
        return None

    status = raw.get("congestion_status") or raw.get("status") or raw.get("level")
    if isinstance(status, str):
        status = status.lower().strip()

    status_map = {
        "원활": "smooth",
        "보통": "normal",
        "혼잡": "congested",
        "매우혼잡": "severe",
        "smooth": "smooth",
        "normal": "normal",
        "congested": "congested",
        "severe": "severe",
    }
    normalized_status = status_map.get(status, "normal")

    time_minutes = raw.get("congestion_time_minutes") or raw.get("wait_time") or raw.get("waitTime")
    if time_minutes is not None:
        try:
            time_minutes = float(time_minutes)
        except (ValueError, TypeError):
            time_minutes = None

    return {
        "congestion_status": normalized_status,
        "congestion_time_minutes": time_minutes,
        "observed_at": _extract_observed_at(raw),
    }


def normalize_operation(raw: dict[str, Any] | None) -> dict[str, Any] | None:
    if raw is None:
        return None

    return {
        "expected_arrival_applied": raw.get("expected_arrival_applied")
        or raw.get("expectedArrival")
        or raw.get("eta_applied"),
        "raw_status_note": raw.get("raw_status_note") or raw.get("statusNote") or raw.get("note"),
        "observed_at": _extract_observed_at(raw),
    }


def normalize_gate_entry(raw: dict[str, Any] | None) -> dict[str, Any] | None:
    if raw is None:
        return None

    count = raw.get("vehicle_count") or raw.get("vehicleCount") or raw.get("count")
    if count is not None:
        try:
            count = int(count)
        except (ValueError, TypeError):
            count = None

    return {
        "vehicle_count": count,
        "entry_type": raw.get("entry_type") or raw.get("entryType") or "container",
        "lane_code": raw.get("lane_code") or raw.get("laneCode"),
        "observed_at": _extract_observed_at(raw),
    }


def normalize_traffic(raw: dict[str, Any] | None) -> dict[str, Any] | None:
    if raw is None:
        return None

    speed = raw.get("average_speed_kph") or raw.get("avgSpeed") or raw.get("speed")
    if speed is not None:
        try:
            speed = float(speed)
        except (ValueError, TypeError):
            speed = None

    travel = (
        raw.get("estimated_travel_minutes") or raw.get("travelTime") or raw.get("travel_minutes")
    )
    if travel is not None:
        try:
            travel = float(travel)
        except (ValueError, TypeError):
            travel = None

    return {
        "average_speed_kph": speed,
        "estimated_travel_minutes": travel,
        "congestion_level": raw.get("congestion_level") or raw.get("congestionLevel"),
        "observed_at": _extract_observed_at(raw),
    }


def _extract_observed_at(raw: dict[str, Any]) -> str:
    observed = raw.get("observed_at") or raw.get("observedAt") or raw.get("timestamp")
    if observed is None:
        return datetime.now(timezone.utc).isoformat()
    if isinstance(observed, datetime):
        return observed.isoformat()
    return str(observed)
