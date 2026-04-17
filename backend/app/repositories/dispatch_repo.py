from __future__ import annotations

from datetime import datetime
from typing import Sequence

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.orm import (
    DispatchEvaluation,
    DispatchEvaluationSource,
    DispatchReasonItem,
    SourceSnapshotGateEntry,
    SourceSnapshotTerminalCongestion,
    SourceSnapshotTerminalOperation,
    SourceSnapshotTraffic,
    Terminal,
)


async def get_terminals(db: AsyncSession, active_only: bool = True) -> Sequence[Terminal]:
    stmt = select(Terminal)
    if active_only:
        stmt = stmt.where(Terminal.is_active.is_(True))
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_terminal_by_code(db: AsyncSession, code: str) -> Terminal | None:
    stmt = select(Terminal).where(Terminal.terminal_code == code)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def save_evaluation(
    db: AsyncSession,
    evaluation: DispatchEvaluation,
    reason_items: list[DispatchReasonItem],
    source_links: list[DispatchEvaluationSource],
) -> DispatchEvaluation:
    db.add(evaluation)
    await db.flush()

    for item in reason_items:
        item.dispatch_evaluation_id = evaluation.id
        db.add(item)

    for link in source_links:
        link.dispatch_evaluation_id = evaluation.id
        db.add(link)

    await db.commit()
    await db.refresh(evaluation)
    return evaluation


async def get_latest_congestion(
    db: AsyncSession, terminal_code: str
) -> SourceSnapshotTerminalCongestion | None:
    stmt = (
        select(SourceSnapshotTerminalCongestion)
        .where(SourceSnapshotTerminalCongestion.terminal_code == terminal_code)
        .order_by(desc(SourceSnapshotTerminalCongestion.observed_at))
        .limit(1)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_latest_operation(
    db: AsyncSession, terminal_code: str
) -> SourceSnapshotTerminalOperation | None:
    stmt = (
        select(SourceSnapshotTerminalOperation)
        .where(SourceSnapshotTerminalOperation.terminal_code == terminal_code)
        .order_by(desc(SourceSnapshotTerminalOperation.observed_at))
        .limit(1)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_latest_gate_entry(
    db: AsyncSession, terminal_name: str
) -> SourceSnapshotGateEntry | None:
    stmt = (
        select(SourceSnapshotGateEntry)
        .where(SourceSnapshotGateEntry.terminal_name == terminal_name)
        .order_by(desc(SourceSnapshotGateEntry.observed_at))
        .limit(1)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_latest_traffic(db: AsyncSession, route_key: str) -> SourceSnapshotTraffic | None:
    stmt = (
        select(SourceSnapshotTraffic)
        .where(SourceSnapshotTraffic.route_key == route_key)
        .order_by(desc(SourceSnapshotTraffic.observed_at))
        .limit(1)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def save_congestion_snapshot(
    db: AsyncSession, snapshot: SourceSnapshotTerminalCongestion
) -> None:
    db.add(snapshot)
    await db.commit()


async def save_operation_snapshot(
    db: AsyncSession, snapshot: SourceSnapshotTerminalOperation
) -> None:
    db.add(snapshot)
    await db.commit()


async def save_gate_entry_snapshot(db: AsyncSession, snapshot: SourceSnapshotGateEntry) -> None:
    db.add(snapshot)
    await db.commit()


async def save_traffic_snapshot(db: AsyncSession, snapshot: SourceSnapshotTraffic) -> None:
    db.add(snapshot)
    await db.commit()


async def seed_terminals(db: AsyncSession) -> None:
    existing = await get_terminals(db, active_only=False)
    if existing:
        return

    terminals = [
        Terminal(terminal_code="ICT", terminal_name="Incheon Container Terminal"),
        Terminal(terminal_code="E1", terminal_name="E1 Container Terminal"),
        Terminal(terminal_code="SNCT", terminal_name="Sun Kwang New Container Terminal"),
        Terminal(terminal_code="HJIT", terminal_name="Hanjin Incheon Terminal"),
        Terminal(terminal_code="SGT", terminal_name="Sungmin Terminal"),
    ]
    for t in terminals:
        db.add(t)
    await db.commit()
