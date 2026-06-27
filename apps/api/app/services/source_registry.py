from __future__ import annotations

from datetime import UTC

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.source_import import Source


class SourceRegistryService:
    async def register(
        self,
        db: AsyncSession,
        project_id: str,
        user_id: str,
        source_type: str,
        display_name: str | None = None,
        url: str | None = None,
        file_path: str | None = None,
        mime_type: str | None = None,
        size_bytes: int | None = None,
        metadata: dict | None = None,
    ) -> Source:
        source = Source(
            project_id=project_id,
            user_id=user_id,
            source_type=source_type,
            display_name=display_name,
            url=url,
            file_path=file_path,
            mime_type=mime_type,
            size_bytes=size_bytes,
            metadata_=metadata,
        )
        db.add(source)
        await db.commit()
        await db.refresh(source)
        return source

    async def get_source(self, db: AsyncSession, source_id: str) -> Source | None:
        return await db.get(Source, source_id)

    async def list_sources(
        self, db: AsyncSession, project_id: str, limit: int = 50, offset: int = 0
    ) -> list[Source]:
        return await Source.find_by_project(db, project_id, limit, offset)

    async def increment_memory_count(self, db: AsyncSession, source_id: str):
        source = await db.get(Source, source_id)
        if source:
            source.memory_count = (source.memory_count or 0) + 1
            from datetime import datetime
            source.last_import_at = datetime.now(UTC).isoformat()
            await db.commit()

    async def get_or_create_source(
        self,
        db: AsyncSession,
        project_id: str,
        user_id: str,
        source_type: str,
        url: str | None = None,
        display_name: str | None = None,
    ) -> Source:
        if url:
            result = await db.execute(
                select(Source).where(
                    Source.project_id == project_id,
                    Source.url == url,
                    Source.source_type == source_type,
                )
            )
            existing = result.scalar_one_or_none()
            if existing:
                return existing
        return await self.register(
            db=db,
            project_id=project_id,
            user_id=user_id,
            source_type=source_type,
            display_name=display_name or url or source_type,
            url=url,
        )


source_registry_service = SourceRegistryService()
