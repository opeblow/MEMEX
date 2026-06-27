from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from structlog import get_logger

from app.api.router import api_router
from app.config import settings
from app.database.session import check_database_health, engine

logger = get_logger()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    logger.info("Starting MEMEX API", version=settings.app_version)
    async with engine.begin() as conn:
        await conn.run_sync(lambda _: None)
    yield
    await engine.dispose()
    logger.info("Shutting down MEMEX API")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal error occurred",
            },
        },
    )


app.include_router(api_router, prefix="/api/v1/memex")


@app.get("/health")
async def health_check() -> dict[str, str | bool]:
    db_healthy = await check_database_health()
    return {
        "status": "ok" if db_healthy else "degraded",
        "version": settings.app_version,
        "database": "connected" if db_healthy else "disconnected",
    }
