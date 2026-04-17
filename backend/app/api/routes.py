from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    DispatchJobInput,
    DispatchRiskResult,
    HealthStatus,
    SimulationInput,
    SimulationResult,
    TerminalInfo,
)
from app.services.dispatch_service import evaluate_dispatch, simulate_dispatch

router = APIRouter(prefix="/api/v1")

SUPPORTED_TERMINALS = [
    TerminalInfo(terminal_code="ICT", terminal_name="Incheon Container Terminal", is_active=True),
    TerminalInfo(terminal_code="E1", terminal_name="E1 Container Terminal", is_active=True),
    TerminalInfo(
        terminal_code="SNCT", terminal_name="Sun Kwang New Container Terminal", is_active=True
    ),
    TerminalInfo(terminal_code="HJIT", terminal_name="Hanjin Incheon Terminal", is_active=True),
    TerminalInfo(terminal_code="SGT", terminal_name="Sungmin Terminal", is_active=True),
]

VALID_TERMINAL_CODES = {t.terminal_code for t in SUPPORTED_TERMINALS}


@router.post("/risk/evaluate", response_model=DispatchRiskResult)
async def risk_evaluate(job: DispatchJobInput) -> DispatchRiskResult:
    if job.terminal_code not in VALID_TERMINAL_CODES:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported terminal: {job.terminal_code}. Supported: {sorted(VALID_TERMINAL_CODES)}",
        )
    return await evaluate_dispatch(job)


@router.post("/risk/simulate", response_model=SimulationResult)
async def risk_simulate(sim: SimulationInput) -> SimulationResult:
    if sim.terminal_code not in VALID_TERMINAL_CODES:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported terminal: {sim.terminal_code}.",
        )
    return await simulate_dispatch(sim)


@router.get("/terminals", response_model=list[TerminalInfo])
async def list_terminals() -> list[TerminalInfo]:
    return [t for t in SUPPORTED_TERMINALS if t.is_active]


@router.get("/health", response_model=HealthStatus)
async def health_check() -> HealthStatus:
    db_status = "ok"
    redis_status = "ok"

    try:
        from app.cache import redis_client

        await redis_client.ping()
    except Exception:
        redis_status = "unavailable"

    return HealthStatus(
        status="ok" if redis_status == "ok" else "degraded",
        version="0.1.0",
        database=db_status,
        redis=redis_status,
    )
