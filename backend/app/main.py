from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.scheduler.ingestion import ingest_all_sources


@asynccontextmanager
async def lifespan(application: FastAPI):
    try:
        await ingest_all_sources()
    except Exception:
        pass
    yield


app = FastAPI(
    title="Incheon Port Cut-off Risk Radar",
    version="0.1.0",
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
