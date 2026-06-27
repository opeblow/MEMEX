from __future__ import annotations

import time
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger

from app.models.memory import Memory
from app.services.knowledge import knowledge_service
from app.services.memory_serializer import memory_serializer

logger = get_logger()


class MemoryIndex:
    async def index_memory(
        self,
        db: AsyncSession,
        memory: Memory,
        content: str | None = None,
    ) -> Memory:
        start = time.monotonic()

        if content:
            preview = memory_serializer.content_preview(content)
            memory.content_preview = preview

            if not memory.tags or len(memory.tags) == 0:
                try:
                    tags = await knowledge_service.generate_tags(content)
                    if tags:
                        memory.tags = tags
                except Exception as e:
                    logger.warning("Tag generation failed during index", error=str(e))

        memory.updated_at = datetime.now(UTC)
        db.add(memory)
        await db.commit()
        await db.refresh(memory)

        elapsed = int((time.monotonic() - start) * 1000)
        logger.info(
            "Memory indexed",
            memory_id=memory.id,
            elapsed_ms=elapsed,
        )
        return memory

    async def reindex_memory(
        self,
        db: AsyncSession,
        memory_id: str,
        content: str | None = None,
    ) -> Memory | None:
        result = await db.execute(select(Memory).where(Memory.id == memory_id))
        memory = result.scalar_one_or_none()
        if not memory:
            return None
        return await self.index_memory(db, memory, content)

    async def batch_index(
        self,
        db: AsyncSession,
        memories: list[Memory],
    ) -> list[Memory]:
        results: list[Memory] = []
        for memory in memories:
            indexed = await self.index_memory(db, memory)
            results.append(indexed)
        return results


memory_index = MemoryIndex()
