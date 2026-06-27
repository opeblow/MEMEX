from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent import TaskExecution
from app.schemas.agent import TaskExecutionCreate, TaskExecutionUpdate


class TaskHistoryService:
    async def create_task(
        self,
        db: AsyncSession,
        project_id: str,
        agent_id: str,
        request: TaskExecutionCreate,
    ) -> TaskExecution:
        task = TaskExecution(
            project_id=project_id,
            agent_id=agent_id,
            workflow_id=request.workflow_id,
            parent_task_id=request.parent_task_id,
            name=request.name,
            input_data=request.input_data,
            metadata_=request.metadata,
            status="pending",
        )
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task

    async def get_task(self, db: AsyncSession, task_id: str) -> TaskExecution | None:
        return await TaskExecution.find_by_id(db, task_id)

    async def list_by_agent(
        self, db: AsyncSession, agent_id: str, limit: int = 50, offset: int = 0
    ) -> list[TaskExecution]:
        return await TaskExecution.find_by_agent(db, agent_id, limit, offset)

    async def list_by_workflow(
        self, db: AsyncSession, workflow_id: str
    ) -> list[TaskExecution]:
        return await TaskExecution.find_by_workflow(db, workflow_id)

    async def update_task(
        self, db: AsyncSession, task_id: str, request: TaskExecutionUpdate
    ) -> TaskExecution | None:
        task = await TaskExecution.find_by_id(db, task_id)
        if not task:
            return None
        update_data = request.model_dump(exclude_unset=True)
        now = datetime.now(UTC).isoformat()
        if "status" in update_data:
            if update_data["status"] == "running" and not task.started_at:
                task.started_at = now
            elif update_data["status"] in ("completed", "failed") and not task.completed_at:
                task.completed_at = now
                if task.started_at:
                    from datetime import datetime as dt
                    try:
                        start = dt.fromisoformat(task.started_at)
                        end = dt.fromisoformat(now)
                        task.duration_ms = int((end - start).total_seconds() * 1000)
                    except (ValueError, TypeError):
                        pass
        for key, value in update_data.items():
            if key != "started_at" and key != "completed_at" and key != "duration_ms":
                setattr(task, key, value)
        await db.commit()
        await db.refresh(task)
        return task

    async def start_task(self, db: AsyncSession, task_id: str) -> TaskExecution | None:
        return await self.update_task(
            db, task_id, TaskExecutionUpdate(status="running")
        )

    async def complete_task(
        self, db: AsyncSession, task_id: str, output_data: dict | None = None
    ) -> TaskExecution | None:
        return await self.update_task(
            db, task_id, TaskExecutionUpdate(status="completed", output_data=output_data)
        )

    async def fail_task(
        self, db: AsyncSession, task_id: str, error_message: str
    ) -> TaskExecution | None:
        return await self.update_task(
            db, task_id, TaskExecutionUpdate(status="failed", error_message=error_message)
        )


task_history_service = TaskHistoryService()
