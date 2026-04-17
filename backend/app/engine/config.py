"""
Risk engine configuration — all weights, thresholds, and probability mappings.
Separated from logic so the engine remains deterministic and config-driven.
Tuning these values does not require code changes.
"""

from __future__ import annotations

ENGINE_VERSION = "v1.0.0"

RISK_SCORE_BUCKETS = {
    "LOW": (0, 34),
    "MEDIUM": (35, 69),
    "HIGH": (70, 100),
}

CONGESTION_WAIT_MINUTES = {
    "smooth": 5,
    "normal": 15,
    "congested": 30,
    "severe": 50,
}

GATE_ENTRY_PENALTY_MINUTES = {
    "low": 0,
    "normal": 5,
    "busy": 15,
    "very_busy": 25,
}

DEFAULT_TRAVEL_MINUTES_BY_ZONE = {
    "SONGDO": 25,
    "NAMDONG": 35,
    "SEOGU": 20,
    "YEONSU": 30,
    "BUPYEONG": 40,
    "SIHEUNG": 45,
    "ANSAN": 55,
    "DEFAULT": 40,
}

TRAFFIC_SPEED_TO_MULTIPLIER = [
    (60, 1.0),
    (40, 1.3),
    (20, 1.8),
    (0, 2.5),
]

CONSERVATIVE_EXTRA_BUFFER_MINUTES = 20
BASE_BUFFER_MINUTES = 15

# slack_minutes → (risk_score, on_time_probability)
# Deterministic heuristic mapping, NOT a calibrated statistical model.
SLACK_TO_RISK_PROBABILITY = [
    (90, 5, 0.97),
    (60, 15, 0.92),
    (45, 25, 0.82),
    (30, 40, 0.68),
    (15, 60, 0.48),
    (5, 78, 0.28),
    (0, 88, 0.15),
    (-999, 98, 0.05),
]

FRESHNESS_PENALTY_SECONDS_THRESHOLD = 600
FRESHNESS_PENALTY_MINUTES = 10
