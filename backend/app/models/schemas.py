"""API 요청/응답 계약을 위한 Pydantic 스키마."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ResultStatus(str, Enum):
    FULL = "FULL"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"


class FreshnessStatus(str, Enum):
    LIVE = "LIVE"
    CACHED = "CACHED"
    STALE = "STALE"
    UNAVAILABLE = "UNAVAILABLE"


class DispatchJobInput(BaseModel):
    origin_zone_id: str = Field(..., description="출발 지역 식별자 (예: 'SONGDO', 'NAMDONG')")
    terminal_code: str = Field(..., description="도착 터미널 코드")
    cut_off_at: datetime = Field(..., description="Gate-in cut-off 시간 (Asia/Seoul)")
    conservative_mode: bool = Field(default=False, description="보수적 모드 활성화 여부")
    manual_buffer_minutes: int | None = Field(
        default=None, ge=0, le=120, description="수동 버퍼 시간 (분)"
    )


class SimulationInput(BaseModel):
    origin_zone_id: str
    terminal_code: str
    cut_off_at: datetime
    scenario_offsets_minutes: list[int] = Field(
        default=[0, -15, -30, -60],
        description="출발 시각 오프셋 (분 단위, 음수 = 조기 출발)",
    )


class ReasonItem(BaseModel):
    code: str
    label: str
    contribution_percent: int = Field(ge=0, le=100)
    impact_minutes: float
    direction: str = Field(description="'increase' 또는 'decrease'")
    summary: str


class SourceFreshness(BaseModel):
    source_name: str
    observed_at: datetime | None
    status: FreshnessStatus
    freshness_seconds: int | None = None


class Warning(BaseModel):
    code: str
    message: str
    affected_source: str | None = None


class DispatchRiskResult(BaseModel):
    evaluation_id: str
    result_status: ResultStatus
    risk_score: int = Field(ge=0, le=100, description="리스크 점수 (0~100)")
    risk_level: RiskLevel
    on_time_probability: float = Field(ge=0.0, le=1.0, description="정시 도착 확률 (0~1)")
    latest_safe_dispatch_at: datetime | None = Field(description="최늦 안전 출발 시각")
    estimated_total_minutes: int = Field(description="예상 총 소요시간 (분)")
    verdict: str = Field(description="종합 판단 문구")
    reason_items: list[ReasonItem]
    source_freshness: list[SourceFreshness]
    warnings: list[Warning] = Field(default_factory=list)
    engine_version: str
    evaluated_at: datetime


class ScenarioResult(BaseModel):
    offset_minutes: int
    dispatch_at: datetime
    risk_score: int
    risk_level: RiskLevel
    on_time_probability: float
    latest_safe_dispatch_at: datetime | None
    verdict: str


class SimulationResult(BaseModel):
    base_scenario: ScenarioResult
    scenarios: list[ScenarioResult]
    source_freshness: list[SourceFreshness]
    warnings: list[Warning] = Field(default_factory=list)
    engine_version: str
    evaluated_at: datetime


class TerminalInfo(BaseModel):
    terminal_code: str
    terminal_name: str
    is_active: bool


class HealthStatus(BaseModel):
    status: str
    version: str
    database: str
    redis: str
    source_freshness_summary: dict[str, str] = Field(default_factory=dict)
