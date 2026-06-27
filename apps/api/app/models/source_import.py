from __future__ import annotations

from sqlalchemy import BigInteger, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDMixin


class Source(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "sources"
    __table_args__ = {"schema": "memex"}

    project_id: Mapped[str] = mapped_column(String(255), index=True)
    user_id: Mapped[str] = mapped_column(String(255), index=True)
    source_type: Mapped[str] = mapped_column(String(100))
    display_name: Mapped[str | None] = mapped_column(String(500))
    url: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    size_bytes: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True)
    memory_count: Mapped[int] = mapped_column(Integer, default=0)
    last_import_at: Mapped[str | None] = mapped_column(String(50), nullable=True)

    @classmethod
    async def find_by_project(cls, db, project_id: str, limit: int = 50, offset: int = 0):
        from sqlalchemy import select
        result = await db.execute(
            select(cls)
            .where(cls.project_id == project_id)
            .order_by(cls.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    @classmethod
    async def find_by_id(cls, db, source_id: str):
        return await db.get(cls, source_id)


class ImportJob(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "import_jobs"
    __table_args__ = {"schema": "memex"}

    project_id: Mapped[str] = mapped_column(String(255), index=True)
    user_id: Mapped[str] = mapped_column(String(255), index=True)
    source_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_type: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(50), default="queued")
    progress_pct: Mapped[int] = mapped_column(Integer, default=0)
    current_step: Mapped[str | None] = mapped_column(String(100), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    total_items: Mapped[int] = mapped_column(Integer, default=0)
    processed_items: Mapped[int] = mapped_column(Integer, default=0)
    memory_ids: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True)

    @classmethod
    async def find_by_project(cls, db, project_id: str, limit: int = 50, offset: int = 0):
        from sqlalchemy import select
        result = await db.execute(
            select(cls)
            .where(cls.project_id == project_id)
            .order_by(cls.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    @classmethod
    async def find_by_id(cls, db, job_id: str):
        return await db.get(cls, job_id)


class MemoryVersion(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "memory_versions"
    __table_args__ = {"schema": "memex"}

    memory_id: Mapped[str] = mapped_column(String(255), index=True)
    project_id: Mapped[str] = mapped_column(String(255), index=True)
    version_type: Mapped[str] = mapped_column(String(50))
    content_preview: Mapped[str | None] = mapped_column(Text, nullable=True)
    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    tags: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)
    importance: Mapped[float] = mapped_column(Float, default=0.5)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True)

    @classmethod
    async def find_by_memory(cls, db, memory_id: str):
        from sqlalchemy import select
        result = await db.execute(
            select(cls)
            .where(cls.memory_id == memory_id)
            .order_by(cls.created_at.desc())
        )
        return list(result.scalars().all())
