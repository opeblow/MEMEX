from __future__ import annotations

from sqlalchemy import BigInteger, Float, Integer, String, Text, select
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDMixin


class Memory(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "memories"
    __table_args__ = {"schema": "memex"}

    project_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    session_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cognee_data_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cognee_dataset_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    memory_type: Mapped[str] = mapped_column(String(50), nullable=False, default="text")
    source: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    content_preview: Mapped[str | None] = mapped_column(Text, nullable=True)
    size_bytes: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    token_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    chunk_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="processing")
    importance: Mapped[float] = mapped_column(Float, default=0.5)
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True)

    @classmethod
    async def find_by_id(cls, db: AsyncSession, memory_id: str) -> Memory | None:
        result = await db.execute(select(cls).where(cls.id == memory_id))
        return result.scalar_one_or_none()

    @classmethod
    async def find_by_project(
        cls, db: AsyncSession, project_id: str, limit: int = 50, offset: int = 0
    ) -> list[Memory]:
        result = await db.execute(
            select(cls)
            .where(cls.project_id == project_id)
            .order_by(cls.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())
