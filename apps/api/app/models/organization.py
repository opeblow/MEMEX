from __future__ import annotations

from sqlalchemy import String, Text, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDMixin


class Organization(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "organizations"
    __table_args__ = {"schema": "memex"}

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    avatar_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)

    @classmethod
    async def find_by_id(cls, db: AsyncSession, org_id: str) -> Organization | None:
        result = await db.execute(select(cls).where(cls.id == org_id))
        return result.scalar_one_or_none()

    @classmethod
    async def find_by_owner(
        cls, db: AsyncSession, owner_id: str
    ) -> list[Organization]:
        result = await db.execute(
            select(cls).where(cls.owner_id == owner_id).order_by(cls.created_at.desc())
        )
        return list(result.scalars().all())

    @classmethod
    async def create(
        cls,
        db: AsyncSession,
        name: str,
        slug: str,
        description: str | None,
        owner_id: str,
        avatar_url: str | None = None,
    ) -> Organization:
        org = cls(
            name=name,
            slug=slug,
            description=description,
            owner_id=owner_id,
            avatar_url=avatar_url,
        )
        db.add(org)
        await db.commit()
        await db.refresh(org)
        return org
