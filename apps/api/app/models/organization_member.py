from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class OrganizationMember(Base):
    __tablename__ = "organization_members"
    __table_args__ = {"schema": "memex"}

    organization_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="member")
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    @classmethod
    async def find_by_user(
        cls, db: AsyncSession, user_id: str
    ) -> list[OrganizationMember]:
        result = await db.execute(
            select(cls).where(cls.user_id == user_id)
        )
        return list(result.scalars().all())

    @classmethod
    async def add_member(
        cls,
        db: AsyncSession,
        organization_id: str,
        user_id: str,
        role: str = "member",
    ) -> OrganizationMember:
        member = cls(
            organization_id=organization_id,
            user_id=user_id,
            role=role,
            joined_at=datetime.now(UTC),
        )
        db.add(member)
        await db.commit()
        await db.refresh(member)
        return member
