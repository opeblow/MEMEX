from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent import AgentObservabilityEvent
from app.schemas.agent import ObservabilityEventCreate


class AgentObservabilityService:
    async def record_event(
        self,
        db: AsyncSession,
        project_id: str,
        request: ObservabilityEventCreate,
    ) -> AgentObservabilityEvent:
        event = AgentObservabilityEvent(
            project_id=project_id,
            agent_id=request.agent_id,
            workflow_id=request.workflow_id,
            task_id=request.task_id,
            event_type=request.event_type,
            event_name=request.event_name,
            data=request.data,
            duration_ms=request.duration_ms,
            level=request.level or "info",
        )
        db.add(event)
        await db.commit()
        await db.refresh(event)
        return event

    async def list_by_project(
        self, db: AsyncSession, project_id: str, limit: int = 100, offset: int = 0
    ) -> list[AgentObservabilityEvent]:
        return await AgentObservabilityEvent.find_by_project(db, project_id, limit, offset)

    async def list_by_agent(
        self, db: AsyncSession, agent_id: str, limit: int = 100, offset: int = 0
    ) -> list[AgentObservabilityEvent]:
        return await AgentObservabilityEvent.find_by_agent(db, agent_id, limit, offset)

    async def list_by_type(
        self, db: AsyncSession, project_id: str, event_type: str, limit: int = 100
    ) -> list[AgentObservabilityEvent]:
        return await AgentObservabilityEvent.find_by_type(db, project_id, event_type, limit)


agent_observability_service = AgentObservabilityService()
