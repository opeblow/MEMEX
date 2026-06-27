from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger

from app.models.memory import Memory

logger = get_logger()


class MemoryLifecycle:
    async def soft_delete(
        self, db: AsyncSession, memory_id: str, user_id: str
    ) -> bool:
        result = await db.execute(
            update(Memory)
            .where(Memory.id == memory_id, Memory.user_id == user_id)
            .values(status="deleted")
        )
        await db.commit()
        return result.rowcount > 0

    async def hard_delete(
        self, db: AsyncSession, memory_id: str, user_id: str
    ) -> bool:
        result = await db.execute(
            delete(Memory).where(
                Memory.id == memory_id, Memory.user_id == user_id
            )
        )
        await db.commit()
        return result.rowcount > 0

    async def archive(
        self, db: AsyncSession, memory_id: str, user_id: str
    ) -> bool:
        result = await db.execute(
            update(Memory)
            .where(Memory.id == memory_id, Memory.user_id == user_id)
            .values(status="archived")
        )
        await db.commit()
        return result.rowcount > 0

    async def restore(
        self, db: AsyncSession, memory_id: str, user_id: str
    ) -> bool:
        result = await db.execute(
            update(Memory)
            .where(Memory.id == memory_id, Memory.user_id == user_id)
            .values(status="indexed")
        )
        await db.commit()
        return result.rowcount > 0

    async def expire_memories(
        self, db: AsyncSession, project_id: str, older_than_days: int = 90
    ) -> int:
        cutoff = datetime.now(UTC) - timedelta(days=older_than_days)
        result = await db.execute(
            update(Memory)
            .where(
                Memory.project_id == project_id,
                Memory.created_at < cutoff,
                Memory.status.in_(["indexed", "processing"]),
            )
            .values(status="archived")
        )
        await db.commit()
        count = result.rowcount
        if count:
            logger.info(
                "Memories expired",
                project_id=project_id,
                count=count,
                older_than_days=older_than_days,
            )
        return count

    async def prune_project(
        self, db: AsyncSession, project_id: str
    ) -> int:
        result = await db.execute(
            delete(Memory).where(
                Memory.project_id == project_id,
                Memory.status == "deleted",
            )
        )
        await db.commit()
        count = result.rowcount
        if count:
            logger.info("Pruned deleted memories", project_id=project_id, count=count)
        return count

    async def compress_memory(
        self, db: AsyncSession, memory_id: str
    ) -> bool:
        result = await db.execute(select(Memory).where(Memory.id == memory_id))
        memory = result.scalar_one_or_none()
        if not memory:
            return False

        if memory.content_preview and len(memory.content_preview) > 500:
            memory.content_preview = memory.content_preview[:500]
            memory.metadata_ = {
                **(memory.metadata_ or {}),
                "compressed": True,
                "compressed_at": datetime.now(UTC).isoformat(),
            }
            db.add(memory)
            await db.commit()
            logger.info("Memory compressed", memory_id=memory_id)

        return True


memory_lifecycle = MemoryLifecycle()
