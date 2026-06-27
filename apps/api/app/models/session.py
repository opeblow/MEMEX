from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, select
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDMixin


class Session(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "sessions"
    __table_args__ = {"schema": "memex"}

    project_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    cognee_session_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    @classmethod
    async def find_active(
        cls, db: AsyncSession, project_id: str, user_id: str
    ) -> Session | None:
        result = await db.execute(
            select(cls).where(
                cls.project_id == project_id,
                cls.user_id == user_id,
                cls.is_active,
            )
        )
        return result.scalar_one_or_none()
