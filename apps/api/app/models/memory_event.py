from __future__ import annotations

from sqlalchemy import String, select
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDMixin


class MemoryEvent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "memory_events"
    __table_args__ = {"schema": "memex"}

    project_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    event_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    @classmethod
    async def find_by_project(
        cls, db: AsyncSession, project_id: str, limit: int = 50, offset: int = 0
    ) -> list[MemoryEvent]:
        result = await db.execute(
            select(cls)
            .where(cls.project_id == project_id)
            .order_by(cls.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())
