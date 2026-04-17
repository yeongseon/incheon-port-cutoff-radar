"""Pydantic schemas for API request/response contracts."""

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
    origin_zone_id: str = Field(
        ..., description="Origin zone identifier (e.g., 'SONGDO', 'NAMDONG')"
    )
    terminal_code: str = Field(..., description="Destination terminal code")
    cut_off_at: datetime = Field(..., description="Gate-in cut-off time (Asia/Seoul)")
    conservative_mode: bool = Field(default=False)
    manual_buffer_minutes: int | None = Field(default=None, ge=0, le=120)


class SimulationInput(BaseModel):
    origin_zone_id: str
    terminal_code: str
    cut_off_at: datetime
    scenario_offsets_minutes: list[int] = Field(
        default=[0, -15, -30, -60],
        description="Dispatch time offsets in minutes (negative = earlier)",
    )


class ReasonItem(BaseModel):
    code: str
    label: str
    contribution_percent: int = Field(ge=0, le=100)
    impact_minutes: float
    direction: str = Field(description="'increase' or 'decrease'")
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
    risk_score: int = Field(ge=0, le=100)
    risk_level: RiskLevel
    on_time_probability: float = Field(ge=0.0, le=1.0)
    latest_safe_dispatch_at: datetime | None
    estimated_total_minutes: int
    verdict: str
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
