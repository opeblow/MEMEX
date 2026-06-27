from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDMixin


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"
    __table_args__ = {"schema": "memex"}

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    auth_provider: Mapped[str] = mapped_column(String(50), default="email")
    auth_provider_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(50), default="user")
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_onboarded: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    @classmethod
    async def find_by_email(cls, db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(cls).where(cls.email == email))
        return result.scalar_one_or_none()

    @classmethod
    async def find_by_id(cls, db: AsyncSession, user_id: str) -> User | None:
        result = await db.execute(select(cls).where(cls.id == user_id))
        return result.scalar_one_or_none()

    @classmethod
    async def create(
        cls,
        db: AsyncSession,
        email: str,
        hashed_password: str,
        display_name: str,
    ) -> User:
        user = cls(
            email=email,
            hashed_password=hashed_password,
            display_name=display_name,
            auth_provider="email",
            last_login_at=datetime.now(UTC),
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @classmethod
    async def create_google_user(
        cls,
        db: AsyncSession,
        email: str,
        display_name: str,
        google_id: str,
        avatar_url: str | None = None,
    ) -> User:
        user = cls(
            email=email,
            display_name=display_name,
            auth_provider="google",
            auth_provider_id=google_id,
            avatar_url=avatar_url,
            email_verified=True,
            last_login_at=datetime.now(UTC),
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
