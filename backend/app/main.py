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
        logger.warning("Initial ingestion failed: %s", e)

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
            logger.warning("Periodic ingestion failed: %s", e)


app = FastAPI(
    title="Incheon Port Cut-off Risk Radar",
    version="0.1.0",
    description="Decision-support API for inbound container cut-off risk at Incheon Port",
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
