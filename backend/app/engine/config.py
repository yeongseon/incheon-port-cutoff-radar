"""
리스크 엔진 설정 — 모든 가중치, 임계값, 확률 매핑을 정의합니다.
로직과 분리하여 엔진이 결정론적(deterministic)이고 설정 기반으로 동작하도록 합니다.
이 값을 튜닝할 때 코드 변경이 필요하지 않습니다.
"""

from __future__ import annotations

ENGINE_VERSION = "v1.0.0"

RISK_SCORE_BUCKETS = {
    "LOW": (0, 34),
    "MEDIUM": (35, 69),
    "HIGH": (70, 100),
}

# 터미널 혼잡 상태별 대기 시간 (분)
CONGESTION_WAIT_MINUTES = {
    "smooth": 5,
    "normal": 15,
    "congested": 30,
    "severe": 50,
}

# 게이트 진입 차량 수 기반 추가 지연 (분)
GATE_ENTRY_PENALTY_MINUTES = {
    "low": 0,
    "normal": 5,
    "busy": 15,
    "very_busy": 25,
}

# 출발 지역별 기본 도로 이동 시간 (분)
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

# 교통 속도 → 이동시간 배율 (속도가 낮을수록 배율 증가)
TRAFFIC_SPEED_TO_MULTIPLIER = [
    (60, 1.0),
    (40, 1.3),
    (20, 1.8),
    (0, 2.5),
]

CONSERVATIVE_EXTRA_BUFFER_MINUTES = 20
BASE_BUFFER_MINUTES = 15

# 여유시간(slack) → (리스크 점수, 정시 도착 확률)
# 결정론적 휴리스틱 매핑이며, 통계 모델이 아닙니다.
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

# 데이터 신선도 기준 (초): 이 값을 초과하면 stale로 판단하여 버퍼 추가
FRESHNESS_PENALTY_SECONDS_THRESHOLD = 600
FRESHNESS_PENALTY_MINUTES = 10
