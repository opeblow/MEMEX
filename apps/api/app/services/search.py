from __future__ import annotations

import time

from structlog import get_logger

from app.schemas.memory import RecallResponse

logger = get_logger()


class SearchService:
    async def recall(
        self,
        user_id: str,
        query: str,
        project_id: str,
        session_id: str | None = None,
        datasets: list[str] | None = None,
        query_type: str | None = None,
        top_k: int = 15,
        only_context: bool = False,
        stream: bool = False,
    ) -> RecallResponse:
        start = time.monotonic()

        elapsed = int((time.monotonic() - start) * 1000)

        logger.info(
            "Recall completed",
            user_id=user_id,
            project_id=project_id,
            elapsed_ms=elapsed,
        )

        return RecallResponse(
            answer="",
            sources=[],
            processing_time_ms=elapsed,
        )

    async def recall_stream(
        self,
        user_id: str,
        query: str,
        project_id: str,
        session_id: str | None = None,
    ):
        start = time.monotonic()
        yield {"token": "", "done": False}
        elapsed = int((time.monotonic() - start) * 1000)
        yield {"token": "", "done": True, "processing_time_ms": elapsed}
