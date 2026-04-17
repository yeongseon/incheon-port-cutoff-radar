from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.middleware import rate_limit, verify_api_key
from app.database import get_db
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
    TerminalInfo(terminal_code="ICT", terminal_name="인천컨테이너터미널", is_active=True),
    TerminalInfo(terminal_code="E1", terminal_name="E1컨테이너터미널", is_active=True),
    TerminalInfo(terminal_code="SNCT", terminal_name="선광신컨테이너터미널", is_active=True),
    TerminalInfo(terminal_code="HJIT", terminal_name="한진인천터미널", is_active=True),
    TerminalInfo(terminal_code="SGT", terminal_name="성민터미널", is_active=True),
]

VALID_TERMINAL_CODES = {t.terminal_code for t in SUPPORTED_TERMINALS}


@router.post(
    "/risk/evaluate",
    response_model=DispatchRiskResult,
    dependencies=[Depends(rate_limit), Depends(verify_api_key)],
)
async def risk_evaluate(
    job: DispatchJobInput,
    db: AsyncSession = Depends(get_db),
) -> DispatchRiskResult:
    """단일 반입 작업의 리스크를 평가합니다."""
    if job.terminal_code not in VALID_TERMINAL_CODES:
        raise HTTPException(
            status_code=422,
            detail=f"지원하지 않는 터미널: {job.terminal_code}. 지원 목록: {sorted(VALID_TERMINAL_CODES)}",
        )
    return await evaluate_dispatch(job, db=db)


@router.post(
    "/risk/simulate",
    response_model=SimulationResult,
    dependencies=[Depends(rate_limit), Depends(verify_api_key)],
)
async def risk_simulate(sim: SimulationInput) -> SimulationResult:
    """출발 시각별 what-if 시뮬레이션을 실행합니다."""
    if sim.terminal_code not in VALID_TERMINAL_CODES:
        raise HTTPException(
            status_code=422,
            detail=f"지원하지 않는 터미널: {sim.terminal_code}.",
        )
    return await simulate_dispatch(sim)


@router.get("/terminals", response_model=list[TerminalInfo])
async def list_terminals() -> list[TerminalInfo]:
    """지원하는 인천항 터미널 목록을 반환합니다."""
    return [t for t in SUPPORTED_TERMINALS if t.is_active]


@router.get("/health", response_model=HealthStatus)
async def health_check() -> HealthStatus:
    """서비스 상태 확인 엔드포인트."""
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
