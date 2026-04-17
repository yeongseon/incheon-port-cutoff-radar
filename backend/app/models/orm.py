"""SQLAlchemy ORM models."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    Index,
    Integer,
    String,
    Text,
    ForeignKey,
    func,
)
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Terminal(Base):
    __tablename__ = "terminals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    terminal_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    terminal_name: Mapped[str] = mapped_column(String(200), nullable=False)
    aliases: Mapped[str | None] = mapped_column(Text, nullable=True)
    gate_open_time: Mapped[str | None] = mapped_column(String(10), nullable=True)
    gate_close_time: Mapped[str | None] = mapped_column(String(10), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )


class SourceSnapshotTerminalCongestion(Base):
    __tablename__ = "source_snapshots_terminal_congestion"
    __table_args__ = (Index("ix_congestion_terminal_observed", "terminal_code", "observed_at"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    terminal_code: Mapped[str] = mapped_column(String(50), nullable=False)
    congestion_status: Mapped[str | None] = mapped_column(String(50))
    congestion_time_minutes: Mapped[float | None] = mapped_column(Float)
    observed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    normalized_at: Mapped[datetime | None] = mapped_column(DateTime)
    freshness_status: Mapped[str | None] = mapped_column(String(20))
    raw_payload_json: Mapped[dict | None] = mapped_column(JSON)


class SourceSnapshotTerminalOperation(Base):
    __tablename__ = "source_snapshots_terminal_operation"
    __table_args__ = (Index("ix_operation_terminal_observed", "terminal_code", "observed_at"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    terminal_code: Mapped[str] = mapped_column(String(50), nullable=False)
    available_time: Mapped[datetime | None] = mapped_column(DateTime)
    expected_arrival_applied: Mapped[bool | None] = mapped_column(Boolean)
    raw_status_note: Mapped[str | None] = mapped_column(Text)
    observed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    normalized_at: Mapped[datetime | None] = mapped_column(DateTime)
    freshness_status: Mapped[str | None] = mapped_column(String(20))
    raw_payload_json: Mapped[dict | None] = mapped_column(JSON)


class SourceSnapshotGateEntry(Base):
    __tablename__ = "source_snapshots_gate_entry"
    __table_args__ = (Index("ix_gate_terminal_observed", "terminal_name", "observed_at"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    terminal_name: Mapped[str] = mapped_column(String(200), nullable=False)
    lane_code: Mapped[str | None] = mapped_column(String(50))
    entry_type: Mapped[str | None] = mapped_column(String(50))
    vehicle_count: Mapped[int | None] = mapped_column(Integer)
    observed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    normalized_at: Mapped[datetime | None] = mapped_column(DateTime)
    freshness_status: Mapped[str | None] = mapped_column(String(20))
    raw_payload_json: Mapped[dict | None] = mapped_column(JSON)


class SourceSnapshotTraffic(Base):
    __tablename__ = "source_snapshots_traffic"
    __table_args__ = (Index("ix_traffic_route_observed", "route_key", "observed_at"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    route_key: Mapped[str] = mapped_column(String(100), nullable=False)
    origin_zone_id: Mapped[str | None] = mapped_column(String(50))
    terminal_code: Mapped[str | None] = mapped_column(String(50))
    average_speed_kph: Mapped[float | None] = mapped_column(Float)
    estimated_travel_minutes: Mapped[float | None] = mapped_column(Float)
    congestion_level: Mapped[str | None] = mapped_column(String(20))
    observed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    normalized_at: Mapped[datetime | None] = mapped_column(DateTime)
    freshness_status: Mapped[str | None] = mapped_column(String(20))
    raw_payload_json: Mapped[dict | None] = mapped_column(JSON)


class DispatchEvaluation(Base):
    __tablename__ = "dispatch_evaluations"
    __table_args__ = (
        Index("ix_eval_created", "created_at"),
        Index("ix_eval_terminal_created", "terminal_code", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    evaluation_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    origin_zone_id: Mapped[str] = mapped_column(String(50), nullable=False)
    terminal_code: Mapped[str] = mapped_column(String(50), nullable=False)
    cut_off_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    conservative_mode: Mapped[bool] = mapped_column(Boolean, default=False)
    manual_buffer_minutes: Mapped[int | None] = mapped_column(Integer)
    result_status: Mapped[str] = mapped_column(String(20), nullable=False)
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(10), nullable=False)
    on_time_probability: Mapped[float] = mapped_column(Float, nullable=False)
    latest_safe_dispatch_at: Mapped[datetime | None] = mapped_column(DateTime)
    estimated_total_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    verdict: Mapped[str] = mapped_column(Text, nullable=False)
    engine_version: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    reason_items: Mapped[list[DispatchReasonItem]] = relationship(back_populates="evaluation")
    source_links: Mapped[list[DispatchEvaluationSource]] = relationship(back_populates="evaluation")


class DispatchReasonItem(Base):
    __tablename__ = "dispatch_reason_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dispatch_evaluation_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("dispatch_evaluations.id"), nullable=False
    )
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    label: Mapped[str] = mapped_column(String(200), nullable=False)
    contribution_percent: Mapped[int] = mapped_column(Integer, nullable=False)
    impact_minutes: Mapped[float] = mapped_column(Float, nullable=False)
    direction: Mapped[str] = mapped_column(String(20), nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    summary: Mapped[str] = mapped_column(Text, nullable=False)

    evaluation: Mapped[DispatchEvaluation] = relationship(back_populates="reason_items")


class DispatchEvaluationSource(Base):
    __tablename__ = "dispatch_evaluation_sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dispatch_evaluation_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("dispatch_evaluations.id"), nullable=False
    )
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)
    snapshot_id: Mapped[int | None] = mapped_column(Integer)
    freshness_seconds: Mapped[int | None] = mapped_column(Integer)
    used_fallback: Mapped[bool] = mapped_column(Boolean, default=False)

    evaluation: Mapped[DispatchEvaluation] = relationship(back_populates="source_links")
