from __future__ import annotations

from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDMixin


class MemoryCollection(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "memory_collections"
    __table_args__ = {"schema": "memex"}

    project_id: Mapped[str] = mapped_column(String(255), index=True)
    user_id: Mapped[str] = mapped_column(String(255), index=True)
    name: Mapped[str] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_shared: Mapped[bool] = mapped_column(Boolean, default=False)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True)

    @classmethod
    async def find_by_project(cls, db, project_id: str, limit: int = 50, offset: int = 0):
        from sqlalchemy import select
        result = await db.execute(
            select(cls)
            .where(cls.project_id == project_id)
            .order_by(cls.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    @classmethod
    async def find_by_id(cls, db, collection_id: str):
        return await db.get(cls, collection_id)


class MemoryCollectionItem(Base):
    __tablename__ = "memory_collection_items"
    __table_args__ = {"schema": "memex"}

    collection_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    memory_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    added_by: Mapped[str] = mapped_column(String(255))
    added_at: Mapped[str] = mapped_column(String(50))

    @classmethod
    async def find_by_collection(cls, db, collection_id: str):
        from sqlalchemy import select
        result = await db.execute(
            select(cls).where(cls.collection_id == collection_id)
        )
        return list(result.scalars().all())


class Comment(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "memory_comments"
    __table_args__ = {"schema": "memex"}

    memory_id: Mapped[str] = mapped_column(String(255), index=True)
    user_id: Mapped[str] = mapped_column(String(255), index=True)
    content: Mapped[str] = mapped_column(Text)
    parent_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)

    @classmethod
    async def find_by_memory(cls, db, memory_id: str):
        from sqlalchemy import select
        result = await db.execute(
            select(cls)
            .where(cls.memory_id == memory_id)
            .order_by(cls.created_at)
        )
        return list(result.scalars().all())

    @classmethod
    async def find_by_id(cls, db, comment_id: str):
        return await db.get(cls, comment_id)


class MemoryPermission(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "memory_permissions"
    __table_args__ = {"schema": "memex"}

    memory_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    collection_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    user_id: Mapped[str] = mapped_column(String(255), index=True)
    role: Mapped[str] = mapped_column(String(50))
    granted_by: Mapped[str | None] = mapped_column(String(255), nullable=True)

    @classmethod
    async def find_by_memory(cls, db, memory_id: str):
        from sqlalchemy import select
        result = await db.execute(
            select(cls).where(cls.memory_id == memory_id)
        )
        return list(result.scalars().all())

    @classmethod
    async def find_by_user(cls, db, user_id: str, memory_id: str | None = None):
        from sqlalchemy import select
        conditions = [cls.user_id == user_id]
        if memory_id:
            conditions.append(cls.memory_id == memory_id)
        result = await db.execute(select(cls).where(*conditions))
        return list(result.scalars().all())

    @classmethod
    async def find_by_id(cls, db, perm_id: str):
        return await db.get(cls, perm_id)


class ShareLink(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "share_links"
    __table_args__ = {"schema": "memex"}

    project_id: Mapped[str] = mapped_column(String(255), index=True)
    memory_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    collection_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    token: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    permission: Mapped[str] = mapped_column(String(50), default="viewer")
    expires_at: Mapped[str | None] = mapped_column(String(50), nullable=True)
    max_uses: Mapped[int | None] = mapped_column(Integer, nullable=True)
    use_count: Mapped[int] = mapped_column(Integer, default=0)
    created_by: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    @classmethod
    async def find_by_token(cls, db, token: str):
        from sqlalchemy import select
        result = await db.execute(select(cls).where(cls.token == token))
        return result.scalar_one_or_none()

    @classmethod
    async def find_by_project(cls, db, project_id: str, limit: int = 50, offset: int = 0):
        from sqlalchemy import select
        result = await db.execute(
            select(cls)
            .where(cls.project_id == project_id)
            .order_by(cls.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())


class Invitation(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "invitations"
    __table_args__ = {"schema": "memex"}

    workspace_id: Mapped[str] = mapped_column(String(255), index=True)
    invited_by: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), index=True)
    token: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    role: Mapped[str] = mapped_column(String(50), default="viewer")
    status: Mapped[str] = mapped_column(String(50), default="pending")
    expires_at: Mapped[str | None] = mapped_column(String(50), nullable=True)
    accepted_at: Mapped[str | None] = mapped_column(String(50), nullable=True)

    @classmethod
    async def find_by_token(cls, db, token: str):
        from sqlalchemy import select
        result = await db.execute(select(cls).where(cls.token == token))
        return result.scalar_one_or_none()

    @classmethod
    async def find_by_workspace(cls, db, workspace_id: str, limit: int = 50, offset: int = 0):
        from sqlalchemy import select
        result = await db.execute(
            select(cls)
            .where(cls.workspace_id == workspace_id)
            .order_by(cls.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    @classmethod
    async def find_by_email(cls, db, email: str):
        from sqlalchemy import select
        result = await db.execute(
            select(cls).where(cls.email == email, cls.status == "pending")
        )
        return list(result.scalars().all())


class AuditLog(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "audit_logs"
    __table_args__ = {"schema": "memex"}

    project_id: Mapped[str] = mapped_column(String(255), index=True)
    user_id: Mapped[str] = mapped_column(String(255), index=True)
    action: Mapped[str] = mapped_column(String(100))
    resource_type: Mapped[str] = mapped_column(String(100))
    resource_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    details: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(50), nullable=True)

    @classmethod
    async def find_by_project(cls, db, project_id: str, limit: int = 100, offset: int = 0):
        from sqlalchemy import select
        result = await db.execute(
            select(cls)
            .where(cls.project_id == project_id)
            .order_by(cls.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    @classmethod
    async def find_by_user(cls, db, user_id: str, limit: int = 50, offset: int = 0):
        from sqlalchemy import select
        result = await db.execute(
            select(cls)
            .where(cls.user_id == user_id)
            .order_by(cls.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    @classmethod
    async def find_by_resource(cls, db, resource_type: str, resource_id: str, limit: int = 50):
        from sqlalchemy import select
        result = await db.execute(
            select(cls)
            .where(cls.resource_type == resource_type, cls.resource_id == resource_id)
            .order_by(cls.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
