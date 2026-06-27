from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.memory import Memory


class MemoryEvolutionService:
    async def evolve(
        self,
        db: AsyncSession,
        project_id: str,
        new_content: str,
        new_tags: list[str] | None = None,
    ) -> dict[str, Any]:
        result = await db.execute(
            select(Memory)
            .where(
                Memory.project_id == project_id,
                Memory.status.in_(["indexed", "archived"]),
            )
            .order_by(Memory.importance.desc())
            .limit(20)
        )
        existing = list(result.scalars().all())
        strengthened = 0
        duplicates_found = 0
        from app.services.memory_versioning import versioning_service
        for memory in existing:
            if memory.content_preview and self._is_related(new_content, memory.content_preview):
                memory.importance = min((memory.importance or 0.5) + 0.05, 1.0)
                if new_tags:
                    merged = list(set((memory.tags or []) + new_tags))
                    memory.tags = merged
                await versioning_service.record_version(
                    db=db,
                    memory_id=memory.id,
                    project_id=project_id,
                    version_type="merged",
                    content_preview=memory.content_preview,
                    title=memory.title,
                    tags=memory.tags,
                    importance=memory.importance,
                    metadata={"strengthened": True},
                )
                strengthened += 1
            if self._is_duplicate(new_content, memory.content_preview):
                duplicates_found += 1
        await db.commit()
        return {
            "strengthened": strengthened,
            "duplicates_found": duplicates_found,
        }

    def _is_related(self, new: str, existing: str) -> bool:
        new_words = set(new.lower().split())
        existing_words = set(existing.lower().split())
        if not new_words or not existing_words:
            return False
        overlap = len(new_words & existing_words)
        return overlap / min(len(new_words), len(existing_words)) > 0.15

    def _is_duplicate(self, new: str, existing: str) -> bool:
        if not new or not existing:
            return False
        new_norm = " ".join(new.lower().split())
        existing_norm = " ".join(existing.lower().split())
        return new_norm == existing_norm or (
            len(new_norm) > 50 and new_norm[:50] == existing_norm[:50]
        )


memory_evolution_service = MemoryEvolutionService()
