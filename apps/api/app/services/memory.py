from __future__ import annotations

import time
import uuid

from fastapi import UploadFile
from structlog import get_logger

from app.schemas.memory import (
    ForgetResponse,
    ImproveResponse,
    RememberResponse,
)

logger = get_logger()


class MemoryService:
    async def remember(
        self,
        user_id: str,
        project_id: str,
        data: str | None = None,
        file: UploadFile | None = None,
        session_id: str | None = None,
        memory_type: str | None = None,
        title: str | None = None,
        tags: str | None = None,
        run_in_background: bool = False,
    ) -> RememberResponse:
        start = time.monotonic()

        dataset_id = str(uuid.uuid4())
        memory_id = str(uuid.uuid4())

        # TODO: Phase 2 — call cognee.remember()
        # import cognee
        # await cognee.remember(
        #     data=data or file,
        #     dataset_name=f"project_{project_id}",
        #     session_id=session_id,
        # )

        elapsed = int((time.monotonic() - start) * 1000)

        logger.info(
            "Memory ingested",
            user_id=user_id,
            project_id=project_id,
            memory_id=memory_id,
            dataset_id=dataset_id,
            elapsed_ms=elapsed,
        )

        return RememberResponse(
            memory_id=memory_id,
            dataset_id=dataset_id,
            chunk_count=0,
            token_count=0,
            processing_time_ms=elapsed,
            status="indexed" if not run_in_background else "processing",
        )

    async def improve(
        self,
        user_id: str,
        project_id: str,
        session_ids: list[str] | None = None,
        build_global_context_index: bool = False,
        run_in_background: bool = False,
    ) -> ImproveResponse:
        start = time.monotonic()

        # TODO: Phase 2 — call cognee.improve()

        elapsed = int((time.monotonic() - start) * 1000)

        logger.info(
            "Improvement completed",
            user_id=user_id,
            project_id=project_id,
            elapsed_ms=elapsed,
        )

        return ImproveResponse(
            project_id=project_id,
            status="completed",
            processing_time_ms=elapsed,
        )

    async def forget(
        self,
        user_id: str,
        project_id: str,
        data_id: str | None = None,
        dataset: str | None = None,
        everything: bool = False,
        memory_only: bool = False,
    ) -> ForgetResponse:
        start = time.monotonic()

        # TODO: Phase 2 — call cognee.forget()

        elapsed = int((time.monotonic() - start) * 1000)

        logger.info(
            "Memory deleted",
            user_id=user_id,
            project_id=project_id,
            data_id=data_id,
            elapsed_ms=elapsed,
        )

        return ForgetResponse(
            status="ok",
            deleted_data_ids=[data_id] if data_id else [],
            deleted_graph_nodes=0,
            deleted_vectors=0,
        )
