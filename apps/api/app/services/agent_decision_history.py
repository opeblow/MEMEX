from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent import Decision
from app.schemas.agent import DecisionCreate


class DecisionHistoryService:
    async def record_decision(
        self,
        db: AsyncSession,
        project_id: str,
        request: DecisionCreate,
    ) -> Decision:
        decision = Decision(
            project_id=project_id,
            agent_id=request.agent_id,
            workflow_id=request.workflow_id,
            task_id=request.task_id,
            decision_type=request.decision_type,
            input_context=request.input_context,
            reasoning=request.reasoning,
            outcome=request.outcome,
            confidence=request.confidence,
            metadata_=request.metadata,
        )
        db.add(decision)
        await db.commit()
        await db.refresh(decision)
        return decision

    async def get_decision(self, db: AsyncSession, decision_id: str) -> Decision | None:
        return await Decision.find_by_id(db, decision_id)

    async def list_by_agent(
        self, db: AsyncSession, agent_id: str, limit: int = 50, offset: int = 0
    ) -> list[Decision]:
        return await Decision.find_by_agent(db, agent_id, limit, offset)

    async def list_by_workflow(
        self, db: AsyncSession, workflow_id: str
    ) -> list[Decision]:
        return await Decision.find_by_workflow(db, workflow_id)


decision_history_service = DecisionHistoryService()
