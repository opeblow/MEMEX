from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.memory import Memory
from app.models.source_import import MemoryVersion


class VersioningService:
    async def record_version(
        self,
        db: AsyncSession,
        memory_id: str,
        project_id: str,
        version_type: str,
        content_preview: str | None = None,
        title: str | None = None,
        tags: list[str] | None = None,
        importance: float = 0.5,
        metadata: dict | None = None,
    ) -> MemoryVersion:
        version = MemoryVersion(
            memory_id=memory_id,
            project_id=project_id,
            version_type=version_type,
            content_preview=content_preview,
            title=title,
            tags=tags,
            importance=importance,
            metadata_=metadata,
        )
        db.add(version)
        await db.commit()
        await db.refresh(version)
        return version

    async def get_versions(self, db: AsyncSession, memory_id: str) -> list[MemoryVersion]:
        return await MemoryVersion.find_by_memory(db, memory_id)

    async def snapshot_current(
        self, db: AsyncSession, memory: Memory, version_type: str = "original",
    ):
        return await self.record_version(
            db=db,
            memory_id=memory.id,
            project_id=memory.project_id,
            version_type=version_type,
            content_preview=memory.content_preview,
            title=memory.title,
            tags=memory.tags,
            importance=memory.importance,
            metadata={"source": memory.source, "memory_type": memory.memory_type},
        )

    async def update_memory(
        self,
        db: AsyncSession,
        memory_id: str,
        content_preview: str | None = None,
        title: str | None = None,
        tags: list[str] | None = None,
        importance: float | None = None,
    ) -> Memory | None:
        memory = await db.get(Memory, memory_id)
        if memory is None:
            return None
        await self.snapshot_current(db, memory, "updated")
        if content_preview is not None:
            memory.content_preview = content_preview
        if title is not None:
            memory.title = title
        if tags is not None:
            memory.tags = tags
        if importance is not None:
            memory.importance = importance
        await db.commit()
        await db.refresh(memory)
        return memory


versioning_service = VersioningService()
