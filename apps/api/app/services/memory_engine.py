from __future__ import annotations

import time
import uuid

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger

from app.models.memory import Memory
from app.schemas.memory import (
    ForgetResponse,
    ImproveResponse,
    MemoryDetailResponse,
    RecallResponse,
    RememberResponse,
)
from app.services.cognee_adapter import cognee_adapter
from app.services.memory_index import memory_index
from app.services.memory_lifecycle import memory_lifecycle
from app.services.memory_retriever import memory_retriever
from app.services.memory_serializer import memory_serializer
from app.services.memory_timeline import memory_timeline
from app.services.memory_worker import memory_worker

logger = get_logger()


class MemoryEngine:
    async def remember(
        self,
        db: AsyncSession,
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

        memory_id = str(uuid.uuid4())

        parsed_tags: list[str] = []
        if tags:
            import json
            try:
                parsed_tags = json.loads(tags) if isinstance(tags, str) else tags
            except (json.JSONDecodeError, TypeError):
                parsed_tags = [tags] if isinstance(tags, str) else []

        file_bytes: bytes | None = None
        filename: str | None = None
        mime_type: str | None = None
        content: str | None = data

        if file:
            file_bytes = await file.read()
            filename = file.filename
            mime_type = file.content_type
            if not content and file_bytes:
                try:
                    content = file_bytes.decode("utf-8", errors="replace")
                except Exception:
                    content = None

        cognee_result = await cognee_adapter.remember(
            user_id=user_id,
            project_id=project_id,
            data=content or data,
            file_bytes=file_bytes,
            filename=filename,
            mime_type=mime_type,
            session_id=session_id,
            memory_type=memory_type,
        )

        memory = Memory(
            id=memory_id,
            project_id=project_id,
            user_id=user_id,
            session_id=session_id,
            cognee_data_id=cognee_result["cognee_data_id"],
            cognee_dataset_id=cognee_adapter._dataset_name(project_id),
            title=title,
            memory_type=memory_type or "text",
            source="direct_input" if data else "file_upload",
            source_url=None,
            file_path=filename,
            mime_type=mime_type,
            content_preview=(content[:300] + "...") if content and len(content) > 300 else content,
            size_bytes=len(file_bytes) if file_bytes else (len(data) if data else 0),
            token_count=cognee_result["token_count"],
            chunk_count=cognee_result["chunk_count"],
            status="processing" if run_in_background else cognee_result["status"],
            importance=0.5,
            tags=parsed_tags or None,
            metadata_={},
        )

        dataset_id = cognee_adapter._dataset_name(project_id)

        db.add(memory)
        await db.commit()
        await db.refresh(memory)

        await memory_timeline.record_event(
            db=db,
            project_id=project_id,
            user_id=user_id,
            event_type="memory.created",
            data={
                "memory_id": memory_id,
                "memory_type": memory_type or "text",
                "title": title,
            },
        )

        if not run_in_background:
            try:
                await memory_index.index_memory(db, memory, content=content)
            except Exception as e:
                logger.warning("Post-index failed", memory_id=memory_id, error=str(e))
        else:
            await memory_worker.enqueue(
                "index_memory",
                memory_id=memory_id,
                user_id=user_id,
                project_id=project_id,
            )

        elapsed = int((time.monotonic() - start) * 1000)

        return RememberResponse(
            memory_id=memory_id,
            dataset_id=dataset_id,
            chunk_count=cognee_result["chunk_count"],
            token_count=cognee_result["token_count"],
            processing_time_ms=elapsed,
            status=memory.status,
        )

    async def recall(
        self,
        db: AsyncSession,
        user_id: str,
        query: str,
        project_id: str,
        session_id: str | None = None,
        session_only: bool = False,
        datasets: list[str] | None = None,
        query_type: str | None = None,
        top_k: int = 15,
        only_context: bool = False,
        stream: bool = False,
    ) -> RecallResponse:
        if stream:
            return await self._recall_stream(
                user_id=user_id,
                query=query,
                project_id=project_id,
                session_id=session_id,
                top_k=top_k,
            )

        start = time.monotonic()

        result = await memory_retriever.hybrid_search(
            db=db,
            user_id=user_id,
            query=query,
            project_id=project_id,
            session_id=session_id,
            session_only=session_only,
            datasets=datasets,
            query_type=query_type,
            top_k=top_k,
            only_context=only_context,
        )

        await memory_timeline.record_event(
            db=db,
            project_id=project_id,
            user_id=user_id,
            event_type="memory.recalled",
            data={
                "query": query,
                "result_count": len(result["sources"]),
            },
        )

        answer = ""
        if not only_context and result["sources"]:
            context = "\n\n".join(
                s["text"] for s in result["sources"][:5] if s.get("text")
            )
            if context.strip():
                try:
                    from app.services.knowledge import knowledge_service
                    answer = await knowledge_service.summarize(
                        f"Query: {query}\n\nContext:\n{context}",
                        max_length=500,
                    )
                except Exception as e:
                    logger.warning("LLM answer generation failed", error=str(e))
                    answer = ""

        elapsed = int((time.monotonic() - start) * 1000)

        return RecallResponse(
            answer=answer,
            sources=[
                memory_serializer.recall_source_from_cognee(s)
                for s in result["sources"]
            ],
            processing_time_ms=elapsed,
        )

    async def _recall_stream(
        self,
        user_id: str,
        query: str,
        project_id: str,
        session_id: str | None = None,
        top_k: int = 15,
    ) -> RecallResponse:
        start = time.monotonic()
        sources: list[dict] = []
        async for token in cognee_adapter.recall_stream(
            user_id=user_id,
            query=query,
            project_id=project_id,
            session_id=session_id,
            top_k=top_k,
        ):
            if token.get("done"):
                sources = token.get("sources", [])
            else:
                pass
        elapsed = int((time.monotonic() - start) * 1000)
        return RecallResponse(
            answer="",
            sources=[
                memory_serializer.recall_source_from_cognee(s)
                for s in sources
            ],
            processing_time_ms=elapsed,
        )

    async def improve(
        self,
        db: AsyncSession,
        user_id: str,
        project_id: str,
        session_ids: list[str] | None = None,
        build_global_context_index: bool = False,
        run_in_background: bool = False,
    ) -> ImproveResponse:
        if run_in_background:
            await memory_worker.enqueue(
                "improve_memories",
                user_id=user_id,
                project_id=project_id,
                session_ids=session_ids,
                build_global_context_index=build_global_context_index,
            )
            return ImproveResponse(
                project_id=project_id,
                status="processing",
                processing_time_ms=0,
            )

        start = time.monotonic()

        improvement = await cognee_adapter.improve(
            user_id=user_id,
            project_id=project_id,
            session_ids=session_ids,
            build_global_context_index=build_global_context_index,
        )

        await memory_timeline.record_event(
            db=db,
            project_id=project_id,
            user_id=user_id,
            event_type="memory.improved",
            data=improvement,
        )

        elapsed = int((time.monotonic() - start) * 1000)

        return ImproveResponse(
            project_id=project_id,
            status="completed",
            processing_time_ms=elapsed,
        )

    async def forget(
        self,
        db: AsyncSession,
        user_id: str,
        project_id: str,
        data_id: str | None = None,
        dataset: str | None = None,
        everything: bool = False,
        memory_only: bool = False,
    ) -> ForgetResponse:
        cognee_result = await cognee_adapter.forget(
            user_id=user_id,
            project_id=project_id,
            data_id=data_id,
            dataset=dataset,
            everything=everything,
            memory_only=memory_only,
        )

        if everything:
            from sqlalchemy import delete as sa_delete
            await db.execute(
                sa_delete(Memory).where(
                    Memory.project_id == project_id,
                    Memory.user_id == user_id,
                )
            )
            await db.commit()
        elif data_id:
            await memory_lifecycle.hard_delete(db, data_id, user_id)

        await memory_timeline.record_event(
            db=db,
            project_id=project_id,
            user_id=user_id,
            event_type="memory.deleted",
            data={
                "data_id": data_id,
                "everything": everything,
                "memory_only": memory_only,
            },
        )

        return ForgetResponse(
            status="ok",
            deleted_data_ids=cognee_result["deleted_data_ids"],
            deleted_graph_nodes=cognee_result["deleted_graph_nodes"],
            deleted_vectors=cognee_result["deleted_vectors"],
        )

    async def get_memory(
        self, db: AsyncSession, memory_id: str
    ) -> MemoryDetailResponse | None:
        result = await db.execute(select(Memory).where(Memory.id == memory_id))
        memory = result.scalar_one_or_none()
        if not memory:
            return None
        return memory_serializer.memory_to_detail(memory)

    async def list_memories(
        self,
        db: AsyncSession,
        project_id: str,
        limit: int = 50,
        offset: int = 0,
    ) -> list[MemoryDetailResponse]:
        memories = await Memory.find_by_project(db, project_id, limit, offset)
        return [memory_serializer.memory_to_detail(m) for m in memories]

    async def search_memories(
        self,
        db: AsyncSession,
        user_id: str,
        project_id: str,
        query: str,
        limit: int = 20,
    ) -> list[MemoryDetailResponse]:
        result = await memory_retriever.hybrid_search(
            db=db,
            user_id=user_id,
            query=query,
            project_id=project_id,
            top_k=limit,
        )
        memory_ids = [s["memory_id"] for s in result["sources"]]
        if not memory_ids:
            return []
        from sqlalchemy import select as sa_select
        db_result = await db.execute(
            sa_select(Memory).where(Memory.id.in_(memory_ids))
        )
        memories = list(db_result.scalars().all())
        memory_map = {m.id: m for m in memories}
        ordered = [memory_map[mid] for mid in memory_ids if mid in memory_map]
        return [memory_serializer.memory_to_detail(m) for m in ordered]


memory_engine = MemoryEngine()
