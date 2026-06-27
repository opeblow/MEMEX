from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import Boolean, DateTime, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, UUIDMixin


class VerificationToken(Base, UUIDMixin):
    __tablename__ = "verification_tokens"
    __table_args__ = {"schema": "memex"}

    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False, default="email_verification")
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)

    @classmethod
    async def find_valid(
        cls, db: AsyncSession, token: str, token_type: str = "email_verification"
    ) -> VerificationToken | None:
        result = await db.execute(
            select(cls).where(
                cls.token == token,
                cls.type == token_type,
                not cls.is_used,
                cls.expires_at > datetime.now(UTC),
            )
        )
        return result.scalar_one_or_none()

    @classmethod
    async def create(
        cls,
        db: AsyncSession,
        user_id: str,
        token: str,
        token_type: str = "email_verification",
        expires_in_hours: int = 24,
    ) -> VerificationToken:
        vt = cls(
            user_id=user_id,
            token=token,
            type=token_type,
            expires_at=datetime.now(UTC) + timedelta(hours=expires_in_hours),
        )
        db.add(vt)
        await db.commit()
        await db.refresh(vt)
        return vt

    @classmethod
    async def mark_used(cls, db: AsyncSession, token_id: str) -> None:
        vt = await db.get(cls, token_id)
        if vt:
            vt.is_used = True
            vt.used_at = datetime.now(UTC)
            await db.commit()
