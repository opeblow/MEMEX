from __future__ import annotations

from sqlalchemy import Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDMixin


class Agent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "agents"
    __table_args__ = {"schema": "memex"}

    project_id: Mapped[str] = mapped_column(String(255), index=True)
    user_id: Mapped[str] = mapped_column(String(255), index=True)
    name: Mapped[str] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    agent_type: Mapped[str] = mapped_column(String(100), default="custom")
    model_config: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    capabilities: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)
    memory_scope: Mapped[str] = mapped_column(String(50), default="workspace")
    permissions: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active")
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True)

    @classmethod
    async def find_by_project(cls, db, project_id: str, limit: int = 50, offset: int = 0):
        from sqlalchemy import select
        result = await db.execute(
            select(cls)
            .where(cls.project_id == project_id)
            .order_by(cls.name)
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    @classmethod
    async def find_by_id(cls, db, agent_id: str):
        return await db.get(cls, agent_id)


class AgentWorkflow(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "agent_workflows"
    __table_args__ = {"schema": "memex"}

    project_id: Mapped[str] = mapped_column(String(255), index=True)
    agent_id: Mapped[str] = mapped_column(String(255), index=True)
    name: Mapped[str] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="queued")
    workflow_type: Mapped[str] = mapped_column(String(100), default="manual")
    input_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    output_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    progress_pct: Mapped[int] = mapped_column(Integer, default=0)
    current_step: Mapped[str | None] = mapped_column(String(200), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[str | None] = mapped_column(String(50), nullable=True)
    completed_at: Mapped[str | None] = mapped_column(String(50), nullable=True)
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
    async def find_by_id(cls, db, workflow_id: str):
        return await db.get(cls, workflow_id)


class TaskExecution(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "task_executions"
    __table_args__ = {"schema": "memex"}

    project_id: Mapped[str] = mapped_column(String(255), index=True)
    workflow_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    agent_id: Mapped[str] = mapped_column(String(255), index=True)
    parent_task_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(50), default="pending")
    input_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    output_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    started_at: Mapped[str | None] = mapped_column(String(50), nullable=True)
    completed_at: Mapped[str | None] = mapped_column(String(50), nullable=True)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True)

    @classmethod
    async def find_by_agent(cls, db, agent_id: str, limit: int = 50, offset: int = 0):
        from sqlalchemy import select
        result = await db.execute(
            select(cls)
            .where(cls.agent_id == agent_id)
            .order_by(cls.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    @classmethod
    async def find_by_workflow(cls, db, workflow_id: str):
        from sqlalchemy import select
        result = await db.execute(
            select(cls)
            .where(cls.workflow_id == workflow_id)
            .order_by(cls.created_at)
        )
        return list(result.scalars().all())

    @classmethod
    async def find_by_id(cls, db, task_id: str):
        return await db.get(cls, task_id)


class Decision(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "agent_decisions"
    __table_args__ = {"schema": "memex"}

    project_id: Mapped[str] = mapped_column(String(255), index=True)
    agent_id: Mapped[str] = mapped_column(String(255), index=True)
    workflow_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    task_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    decision_type: Mapped[str] = mapped_column(String(100))
    input_context: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)
    outcome: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True)

    @classmethod
    async def find_by_agent(cls, db, agent_id: str, limit: int = 50, offset: int = 0):
        from sqlalchemy import select
        result = await db.execute(
            select(cls)
            .where(cls.agent_id == agent_id)
            .order_by(cls.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    @classmethod
    async def find_by_workflow(cls, db, workflow_id: str):
        from sqlalchemy import select
        result = await db.execute(
            select(cls)
            .where(cls.workflow_id == workflow_id)
            .order_by(cls.created_at.desc())
        )
        return list(result.scalars().all())

    @classmethod
    async def find_by_id(cls, db, decision_id: str):
        return await db.get(cls, decision_id)


class AgentObservabilityEvent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "agent_observability_events"
    __table_args__ = {"schema": "memex"}

    project_id: Mapped[str] = mapped_column(String(255), index=True)
    agent_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    workflow_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    task_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    event_type: Mapped[str] = mapped_column(String(50), index=True)
    event_name: Mapped[str] = mapped_column(String(200))
    data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    level: Mapped[str] = mapped_column(String(20), default="info")

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
    async def find_by_agent(cls, db, agent_id: str, limit: int = 100, offset: int = 0):
        from sqlalchemy import select
        result = await db.execute(
            select(cls)
            .where(cls.agent_id == agent_id)
            .order_by(cls.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    @classmethod
    async def find_by_type(cls, db, project_id: str, event_type: str, limit: int = 100):
        from sqlalchemy import select
        result = await db.execute(
            select(cls)
            .where(cls.project_id == project_id, cls.event_type == event_type)
            .order_by(cls.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
