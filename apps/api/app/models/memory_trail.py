from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDMixin


class MemoryTrail(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "memory_trails"
    __table_args__ = {"schema": "memex"}

    project_id: Mapped[str] = mapped_column(String(255), index=True)
    user_id: Mapped[str] = mapped_column(String(255), index=True)
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    trail_steps: Mapped[list[dict[str, Any]] | None] = mapped_column(JSON, nullable=True)
    memory_ids: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    confidence_score: Mapped[float | None] = mapped_column(nullable=True)
    processing_time_ms: Mapped[int | None] = mapped_column(nullable=True)
    model_used: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="completed")

    @classmethod
    def find_by_id(cls, db, trail_id: str) -> MemoryTrail | None:
        from sqlalchemy import select
        result = db.execute(select(cls).where(cls.id == trail_id))
        return result.scalar_one_or_none()

    @classmethod
    def find_by_project(
        cls, db, project_id: str, limit: int = 50, offset: int = 0
    ) -> list[MemoryTrail]:
        from sqlalchemy import select
        result = db.execute(
            select(cls)
            .where(cls.project_id == project_id)
            .order_by(cls.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())
