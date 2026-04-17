import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import settings
from app.scheduler.ingestion import ingest_all_sources

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI):
    try:
        await ingest_all_sources()
    except Exception as e:
        logger.warning("초기 데이터 수집 실패: %s", e)

    ingestion_task = asyncio.create_task(_periodic_ingestion())
    yield
    ingestion_task.cancel()
    try:
        await ingestion_task
    except asyncio.CancelledError:
        pass


async def _periodic_ingestion() -> None:
    while True:
        await asyncio.sleep(settings.ingestion_interval_seconds)
        try:
            await ingest_all_sources()
        except Exception as e:
            logger.warning("주기적 데이터 수집 실패: %s", e)


app = FastAPI(
    title="인천항 Cut-off 리스크 레이더",
    version="0.1.0",
    description="인천항 반입 컨테이너의 cut-off 리스크를 평가하는 의사결정 지원 API",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
