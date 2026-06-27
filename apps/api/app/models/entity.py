from __future__ import annotations

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDMixin


class Entity(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "entities"
    __table_args__ = {"schema": "memex"}

    project_id: Mapped[str] = mapped_column(String(255), index=True)
    name: Mapped[str] = mapped_column(String(500))
    entity_type: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    @classmethod
    def find_by_project(cls, db, project_id: str, limit: int = 100, offset: int = 0):
        from sqlalchemy import select
        result = db.execute(
            select(cls)
            .where(cls.project_id == project_id)
            .order_by(cls.name)
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    @classmethod
    def find_by_type(cls, db, project_id: str, entity_type: str, limit: int = 100):
        from sqlalchemy import select
        result = db.execute(
            select(cls)
            .where(cls.project_id == project_id, cls.entity_type == entity_type)
            .order_by(cls.name)
            .limit(limit)
        )
        return list(result.scalars().all())

    @classmethod
    def search(cls, db, project_id: str, query: str, limit: int = 20):
        from sqlalchemy import select
        result = db.execute(
            select(cls)
            .where(cls.project_id == project_id, cls.name.ilike(f"%{query}%"))
            .order_by(cls.name)
            .limit(limit)
        )
        return list(result.scalars().all())


class Relationship(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "relationships"
    __table_args__ = {"schema": "memex"}

    project_id: Mapped[str] = mapped_column(String(255), index=True)
    source_entity_id: Mapped[str] = mapped_column(String(255), index=True)
    target_entity_id: Mapped[str] = mapped_column(String(255), index=True)
    relationship_type: Mapped[str] = mapped_column(String(100))
    strength: Mapped[float] = mapped_column(default=0.5)
    metadata_: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    @classmethod
    def find_by_entity(cls, db, entity_id: str, limit: int = 100):
        from sqlalchemy import or_, select
        result = db.execute(
            select(cls)
            .where(or_(cls.source_entity_id == entity_id, cls.target_entity_id == entity_id))
            .order_by(cls.strength.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    @classmethod
    def find_by_project(cls, db, project_id: str, limit: int = 200, offset: int = 0):
        from sqlalchemy import select
        result = db.execute(
            select(cls)
            .where(cls.project_id == project_id)
            .order_by(cls.strength.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())
