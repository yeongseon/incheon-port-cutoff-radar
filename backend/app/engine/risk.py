"""리스크 엔진 — cut-off 충족 리스크를 계산하는 핵심 로직."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from app.engine.config import (
    BASE_BUFFER_MINUTES,
    CONGESTION_WAIT_MINUTES,
    CONSERVATIVE_EXTRA_BUFFER_MINUTES,
    DEFAULT_TRAVEL_MINUTES_BY_ZONE,
    ENGINE_VERSION,
    FRESHNESS_PENALTY_MINUTES,
    FRESHNESS_PENALTY_SECONDS_THRESHOLD,
    GATE_ENTRY_PENALTY_MINUTES,
    SLACK_TO_RISK_PROBABILITY,
    TRAFFIC_SPEED_TO_MULTIPLIER,
)


def compute_travel_minutes(
    origin_zone_id: str,
    traffic_snapshot: dict[str, Any] | None,
) -> tuple[float, bool]:
    """출발 지역과 교통 데이터를 기반으로 도로 이동 시간을 계산합니다."""
    base = DEFAULT_TRAVEL_MINUTES_BY_ZONE.get(
        origin_zone_id, DEFAULT_TRAVEL_MINUTES_BY_ZONE["DEFAULT"]
    )

    if traffic_snapshot is None:
        return float(base), True

    speed = traffic_snapshot.get("average_speed_kph")
    if speed is None:
        return float(base), True

    multiplier = 1.0
    for threshold, mult in TRAFFIC_SPEED_TO_MULTIPLIER:
        if speed >= threshold:
            multiplier = mult
            break

    return round(base * multiplier, 1), False


def compute_terminal_wait_minutes(
    congestion_snapshot: dict[str, Any] | None,
) -> tuple[float, bool]:
    """터미널 혼잡도 데이터를 기반으로 대기 시간을 계산합니다."""
    if congestion_snapshot is None:
        return float(CONGESTION_WAIT_MINUTES["normal"]), True

    status = congestion_snapshot.get("congestion_status", "normal").lower()
    explicit_time = congestion_snapshot.get("congestion_time_minutes")

    if explicit_time is not None:
        return float(explicit_time), False

    return float(CONGESTION_WAIT_MINUTES.get(status, CONGESTION_WAIT_MINUTES["normal"])), False


def compute_gate_adjustment_minutes(
    gate_snapshot: dict[str, Any] | None,
) -> tuple[float, bool]:
    """게이트 차량 수를 기반으로 진입 지연 시간을 계산합니다."""
    if gate_snapshot is None:
        return float(GATE_ENTRY_PENALTY_MINUTES["normal"]), True

    count = gate_snapshot.get("vehicle_count")
    if count is None:
        return float(GATE_ENTRY_PENALTY_MINUTES["normal"]), True

    if count <= 10:
        level = "low"
    elif count <= 30:
        level = "normal"
    elif count <= 60:
        level = "busy"
    else:
        level = "very_busy"

    return float(GATE_ENTRY_PENALTY_MINUTES[level]), False


def compute_buffer_minutes(
    conservative_mode: bool,
    manual_buffer: int | None,
    has_stale_sources: bool,
) -> float:
    """안전 버퍼 시간을 계산합니다. 보수적 모드나 오래된 데이터 시 추가 버퍼를 적용합니다."""
    if manual_buffer is not None:
        return float(manual_buffer)

    buf = float(BASE_BUFFER_MINUTES)
    if conservative_mode:
        buf += CONSERVATIVE_EXTRA_BUFFER_MINUTES
    if has_stale_sources:
        buf += FRESHNESS_PENALTY_MINUTES
    return buf


def slack_to_risk_and_probability(slack_minutes: float) -> tuple[int, float]:
    """여유시간(slack)을 리스크 점수와 정시 도착 확률로 변환합니다."""
    for threshold, score, prob in SLACK_TO_RISK_PROBABILITY:
        if slack_minutes >= threshold:
            return score, prob
    return 98, 0.05


def risk_score_to_level(score: int) -> str:
    """리스크 점수를 등급(LOW/MEDIUM/HIGH)으로 변환합니다."""
    if score <= 34:
        return "LOW"
    if score <= 69:
        return "MEDIUM"
    return "HIGH"


def build_reason_items(
    travel_min: float,
    terminal_wait_min: float,
    gate_adj_min: float,
    buffer_min: float,
) -> list[dict[str, Any]]:
    """리스크 요인별 기여도를 계산하여 reason_items 목록을 생성합니다."""
    components = [
        ("TRAFFIC", "도로 교통", travel_min),
        ("TERMINAL_CONGESTION", "터미널 혼잡", terminal_wait_min),
        ("GATE_FLOW", "게이트 진입", gate_adj_min),
        ("BUFFER", "안전 버퍼", buffer_min),
    ]

    total = sum(c[2] for c in components) or 1.0
    items = []
    for code, label, minutes in sorted(components, key=lambda c: c[2], reverse=True):
        pct = round((minutes / total) * 100)
        items.append(
            {
                "code": code,
                "label": label,
                "contribution_percent": pct,
                "impact_minutes": minutes,
                "direction": "increase",
                "summary": f"{label} 요인으로 총 소요시간에 {minutes:.0f}분 추가.",
            }
        )

    return items


def evaluate(
    origin_zone_id: str,
    terminal_code: str,
    cut_off_at: datetime,
    now: datetime,
    conservative_mode: bool = False,
    manual_buffer_minutes: int | None = None,
    traffic_snapshot: dict[str, Any] | None = None,
    congestion_snapshot: dict[str, Any] | None = None,
    gate_snapshot: dict[str, Any] | None = None,
    operation_snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """반입 작업의 리스크를 종합 평가합니다."""
    travel_min, travel_fallback = compute_travel_minutes(origin_zone_id, traffic_snapshot)
    terminal_wait_min, congestion_fallback = compute_terminal_wait_minutes(congestion_snapshot)
    gate_adj_min, gate_fallback = compute_gate_adjustment_minutes(gate_snapshot)

    has_stale = travel_fallback or congestion_fallback or gate_fallback
    buffer_min = compute_buffer_minutes(conservative_mode, manual_buffer_minutes, has_stale)

    total_minutes = travel_min + terminal_wait_min + gate_adj_min + buffer_min
    time_remaining = (cut_off_at - now).total_seconds() / 60.0
    slack = time_remaining - total_minutes

    risk_score, probability = slack_to_risk_and_probability(slack)
    risk_level = risk_score_to_level(risk_score)

    latest_safe = cut_off_at - timedelta(minutes=total_minutes)

    if risk_score <= 34:
        verdict = "지금 출발해도 안전합니다."
    elif risk_score <= 69:
        verdict = "배차 가능하지만 여유가 부족합니다. 조기 출발을 권장합니다."
    else:
        verdict = "Cut-off 초과 위험이 높습니다. 즉시 출발하거나 일정을 재조정하세요."

    reason_items = build_reason_items(travel_min, terminal_wait_min, gate_adj_min, buffer_min)

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "on_time_probability": round(probability, 2),
        "latest_safe_dispatch_at": latest_safe,
        "estimated_total_minutes": int(total_minutes),
        "verdict": verdict,
        "reason_items": reason_items,
        "engine_version": ENGINE_VERSION,
        "used_fallbacks": {
            "traffic": travel_fallback,
            "congestion": congestion_fallback,
            "gate": gate_fallback,
        },
    }
