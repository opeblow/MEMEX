from __future__ import annotations

from sqlalchemy import String, Text, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDMixin


class Project(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "projects"
    __table_args__ = {"schema": "memex"}

    workspace_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    cognee_dataset_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    owner_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    @classmethod
    async def find_by_id(cls, db: AsyncSession, project_id: str) -> Project | None:
        result = await db.execute(select(cls).where(cls.id == project_id))
        return result.scalar_one_or_none()

    @classmethod
    async def find_by_user_id(cls, db: AsyncSession, user_id: str) -> list[Project]:
        result = await db.execute(
            select(cls).where(cls.owner_id == user_id).order_by(cls.created_at.desc())
        )
        return list(result.scalars().all())

    @classmethod
    async def create(
        cls,
        db: AsyncSession,
        workspace_id: str,
        name: str,
        slug: str,
        description: str | None,
        owner_id: str,
    ) -> Project:
        project = cls(
            workspace_id=workspace_id,
            name=name,
            slug=slug,
            description=description,
            owner_id=owner_id,
        )
        db.add(project)
        await db.commit()
        await db.refresh(project)
        return project

    @classmethod
    async def update(
        cls, db: AsyncSession, project_id: str, **kwargs
    ) -> Project | None:
        project = await cls.find_by_id(db, project_id)
        if not project:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(project, key, value)
        await db.commit()
        await db.refresh(project)
        return project

    @classmethod
    async def delete(cls, db: AsyncSession, project_id: str) -> bool:
        project = await cls.find_by_id(db, project_id)
        if not project:
            return False
        await db.delete(project)
        await db.commit()
        return True
