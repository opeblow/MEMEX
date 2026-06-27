from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent import AgentWorkflow
from app.schemas.agent import WorkflowCreate, WorkflowUpdate


class AgentWorkflowService:
    async def create_workflow(
        self,
        db: AsyncSession,
        project_id: str,
        agent_id: str,
        request: WorkflowCreate,
    ) -> AgentWorkflow:
        workflow = AgentWorkflow(
            project_id=project_id,
            agent_id=agent_id,
            name=request.name,
            description=request.description,
            workflow_type=request.workflow_type or "manual",
            input_data=request.input_data,
            metadata_=request.metadata,
            status="queued",
        )
        db.add(workflow)
        await db.commit()
        await db.refresh(workflow)
        return workflow

    async def get_workflow(self, db: AsyncSession, workflow_id: str) -> AgentWorkflow | None:
        return await AgentWorkflow.find_by_id(db, workflow_id)

    async def list_workflows(
        self, db: AsyncSession, project_id: str, limit: int = 50, offset: int = 0
    ) -> list[AgentWorkflow]:
        return await AgentWorkflow.find_by_project(db, project_id, limit, offset)

    async def update_workflow(
        self, db: AsyncSession, workflow_id: str, request: WorkflowUpdate
    ) -> AgentWorkflow | None:
        workflow = await AgentWorkflow.find_by_id(db, workflow_id)
        if not workflow:
            return None
        update_data = request.model_dump(exclude_unset=True)
        if "status" in update_data:
            now = datetime.now(UTC).isoformat()
            if update_data["status"] == "running" and not workflow.started_at:
                workflow.started_at = now
            elif update_data["status"] in ("completed", "failed") and not workflow.completed_at:
                workflow.completed_at = now
        for key, value in update_data.items():
            setattr(workflow, key, value)
        await db.commit()
        await db.refresh(workflow)
        return workflow

    async def delete_workflow(self, db: AsyncSession, workflow_id: str) -> bool:
        workflow = await AgentWorkflow.find_by_id(db, workflow_id)
        if not workflow:
            return False
        await db.delete(workflow)
        await db.commit()
        return True

    async def start_workflow(self, db: AsyncSession, workflow_id: str) -> AgentWorkflow | None:
        return await self.update_workflow(
            db, workflow_id, WorkflowUpdate(status="running")
        )

    async def complete_workflow(
        self, db: AsyncSession, workflow_id: str, output_data: dict | None = None
    ) -> AgentWorkflow | None:
        return await self.update_workflow(
            db, workflow_id, WorkflowUpdate(
                status="completed", output_data=output_data, progress_pct=100,
            )
        )

    async def fail_workflow(
        self, db: AsyncSession, workflow_id: str, error_message: str
    ) -> AgentWorkflow | None:
        return await self.update_workflow(
            db, workflow_id, WorkflowUpdate(status="failed", error_message=error_message)
        )


agent_workflow_service = AgentWorkflowService()
