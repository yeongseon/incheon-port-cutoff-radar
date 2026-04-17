from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import cache_get, source_cache_key
from app.engine.config import ENGINE_VERSION
from app.engine.risk import evaluate
from app.models.orm import (
    DispatchEvaluation,
    DispatchEvaluationSource,
    DispatchReasonItem,
)
from app.models.schemas import (
    DispatchJobInput,
    DispatchRiskResult,
    FreshnessStatus,
    ReasonItem,
    ResultStatus,
    ScenarioResult,
    SimulationInput,
    SimulationResult,
    SourceFreshness,
    Warning,
)
from app.repositories.dispatch_repo import save_evaluation


async def _fetch_snapshots(
    origin_zone_id: str, terminal_code: str
) -> tuple[dict[str, Any], list[SourceFreshness], list[Warning]]:
    sources: dict[str, Any] = {}
    freshness_list: list[SourceFreshness] = []
    warnings: list[Warning] = []

    source_keys = [
        ("terminal_congestion", source_cache_key("terminal_congestion", terminal_code)),
        ("terminal_operation", source_cache_key("terminal_operation", terminal_code)),
        ("gate_entry", source_cache_key("gate_entry", terminal_code)),
        ("traffic", source_cache_key("traffic", f"{origin_zone_id}:{terminal_code}")),
    ]

    for source_name, key in source_keys:
        data = await cache_get(key)
        if data is not None:
            sources[source_name] = data
            observed = data.get("observed_at")
            freshness_list.append(
                SourceFreshness(
                    source_name=source_name,
                    observed_at=observed,
                    status=FreshnessStatus.LIVE if observed else FreshnessStatus.CACHED,
                    freshness_seconds=None,
                )
            )
        else:
            sources[source_name] = None
            freshness_list.append(
                SourceFreshness(
                    source_name=source_name,
                    observed_at=None,
                    status=FreshnessStatus.UNAVAILABLE,
                    freshness_seconds=None,
                )
            )
            warnings.append(
                Warning(
                    code="SOURCE_UNAVAILABLE",
                    message=f"{source_name} data is currently unavailable. Using fallback defaults.",
                    affected_source=source_name,
                )
            )

    return sources, freshness_list, warnings


def _has_critical_failure(sources: dict[str, Any]) -> bool:
    return sources.get("traffic") is None and sources.get("terminal_congestion") is None


async def _persist_evaluation(
    db: AsyncSession | None,
    eval_id: str,
    job: DispatchJobInput,
    result_status: str,
    engine_result: dict[str, Any],
    now: datetime,
) -> None:
    if db is None:
        return
    try:
        evaluation = DispatchEvaluation(
            evaluation_id=eval_id,
            origin_zone_id=job.origin_zone_id,
            terminal_code=job.terminal_code,
            cut_off_at=job.cut_off_at,
            conservative_mode=job.conservative_mode,
            manual_buffer_minutes=job.manual_buffer_minutes,
            result_status=result_status,
            risk_score=engine_result["risk_score"],
            risk_level=engine_result["risk_level"],
            on_time_probability=engine_result["on_time_probability"],
            latest_safe_dispatch_at=engine_result["latest_safe_dispatch_at"],
            estimated_total_minutes=engine_result["estimated_total_minutes"],
            verdict=engine_result["verdict"],
            engine_version=engine_result["engine_version"],
        )

        reason_items = []
        for i, r in enumerate(engine_result["reason_items"]):
            reason_items.append(
                DispatchReasonItem(
                    code=r["code"],
                    label=r["label"],
                    contribution_percent=r["contribution_percent"],
                    impact_minutes=r["impact_minutes"],
                    direction=r["direction"],
                    display_order=i,
                    summary=r["summary"],
                )
            )

        fallbacks = engine_result.get("used_fallbacks", {})
        source_links = []
        for source_type in ["traffic", "congestion", "gate"]:
            source_links.append(
                DispatchEvaluationSource(
                    source_type=source_type,
                    used_fallback=fallbacks.get(source_type, False),
                )
            )

        await save_evaluation(db, evaluation, reason_items, source_links)
    except Exception:
        pass


async def evaluate_dispatch(
    job: DispatchJobInput, db: AsyncSession | None = None
) -> DispatchRiskResult:
    now = datetime.now(timezone.utc)
    eval_id = str(uuid.uuid4())
    sources, freshness_list, warnings = await _fetch_snapshots(
        job.origin_zone_id, job.terminal_code
    )

    if _has_critical_failure(sources):
        return DispatchRiskResult(
            evaluation_id=eval_id,
            result_status=ResultStatus.FAILED,
            risk_score=0,
            risk_level="LOW",
            on_time_probability=0.0,
            latest_safe_dispatch_at=None,
            estimated_total_minutes=0,
            verdict="Unable to evaluate — critical data sources unavailable.",
            reason_items=[],
            source_freshness=freshness_list,
            warnings=warnings,
            engine_version=ENGINE_VERSION,
            evaluated_at=now,
        )

    has_any_warning = len(warnings) > 0
    result_status = ResultStatus.DEGRADED if has_any_warning else ResultStatus.FULL

    engine_result = evaluate(
        origin_zone_id=job.origin_zone_id,
        terminal_code=job.terminal_code,
        cut_off_at=job.cut_off_at,
        now=now,
        conservative_mode=job.conservative_mode,
        manual_buffer_minutes=job.manual_buffer_minutes,
        traffic_snapshot=sources.get("traffic"),
        congestion_snapshot=sources.get("terminal_congestion"),
        gate_snapshot=sources.get("gate_entry"),
        operation_snapshot=sources.get("terminal_operation"),
    )

    await _persist_evaluation(db, eval_id, job, result_status.value, engine_result, now)

    reason_items = [ReasonItem(**r) for r in engine_result["reason_items"]]

    return DispatchRiskResult(
        evaluation_id=eval_id,
        result_status=result_status,
        risk_score=engine_result["risk_score"],
        risk_level=engine_result["risk_level"],
        on_time_probability=engine_result["on_time_probability"],
        latest_safe_dispatch_at=engine_result["latest_safe_dispatch_at"],
        estimated_total_minutes=engine_result["estimated_total_minutes"],
        verdict=engine_result["verdict"],
        reason_items=reason_items,
        source_freshness=freshness_list,
        warnings=warnings,
        engine_version=engine_result["engine_version"],
        evaluated_at=now,
    )


async def simulate_dispatch(sim: SimulationInput) -> SimulationResult:
    now = datetime.now(timezone.utc)
    sources, freshness_list, warnings = await _fetch_snapshots(
        sim.origin_zone_id, sim.terminal_code
    )

    scenarios: list[ScenarioResult] = []
    base_scenario: ScenarioResult | None = None

    for offset in sim.scenario_offsets_minutes:
        shifted_now = now + timedelta(minutes=offset)

        engine_result = evaluate(
            origin_zone_id=sim.origin_zone_id,
            terminal_code=sim.terminal_code,
            cut_off_at=sim.cut_off_at,
            now=shifted_now,
            traffic_snapshot=sources.get("traffic"),
            congestion_snapshot=sources.get("terminal_congestion"),
            gate_snapshot=sources.get("gate_entry"),
            operation_snapshot=sources.get("terminal_operation"),
        )

        scenario = ScenarioResult(
            offset_minutes=offset,
            dispatch_at=shifted_now,
            risk_score=engine_result["risk_score"],
            risk_level=engine_result["risk_level"],
            on_time_probability=engine_result["on_time_probability"],
            latest_safe_dispatch_at=engine_result["latest_safe_dispatch_at"],
            verdict=engine_result["verdict"],
        )

        if offset == 0:
            base_scenario = scenario
        scenarios.append(scenario)

    if base_scenario is None:
        base_scenario = scenarios[0]

    return SimulationResult(
        base_scenario=base_scenario,
        scenarios=scenarios,
        source_freshness=freshness_list,
        warnings=warnings,
        engine_version=ENGINE_VERSION,
        evaluated_at=now,
    )
