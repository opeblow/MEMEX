from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent import Agent, AgentWorkflow
from app.schemas.agent import HandoffRequest, HandoffResponse


class AgentCollaborationService:
    async def handoff(
        self,
        db: AsyncSession,
        project_id: str,
        request: HandoffRequest,
    ) -> HandoffResponse:
        from_agent = await Agent.find_by_id(db, request.from_agent_id)
        if not from_agent:
            raise ValueError(f"Source agent {request.from_agent_id} not found")

        to_agent = await Agent.find_by_id(db, request.to_agent_id)
        if not to_agent:
            raise ValueError(f"Target agent {request.to_agent_id} not found")

        source_workflow = await AgentWorkflow.find_by_id(db, request.workflow_id)
        if not source_workflow:
            raise ValueError(f"Workflow {request.workflow_id} not found")

        context = {
            "handoff_from": request.from_agent_id,
            "handoff_from_agent": from_agent.name,
            "handoff_message": request.message or "",
            "original_workflow_id": request.workflow_id,
            "original_workflow_name": source_workflow.name,
            "source_input": source_workflow.input_data,
            "source_output": source_workflow.output_data,
            "handoff_context": request.context or {},
            "handoff_timestamp": datetime.now(UTC).isoformat(),
        }

        new_workflow = AgentWorkflow(
            project_id=project_id,
            agent_id=request.to_agent_id,
            name=f"Handoff: {source_workflow.name}",
            description=f"Handoff from {from_agent.name}: {request.message or 'No message'}",
            workflow_type="handoff",
            input_data=context,
            status="queued",
        )
        db.add(new_workflow)
        await db.commit()
        await db.refresh(new_workflow)

        source_workflow.metadata_ = {
            **(source_workflow.metadata_ or {}),
            "handed_off_to": request.to_agent_id,
            "handed_off_to_agent": to_agent.name,
            "handoff_workflow_id": new_workflow.id,
        }
        await db.commit()

        return HandoffResponse(
            handoff_id=str(datetime.now(UTC).timestamp()),
            new_workflow_id=new_workflow.id,
            status="handed_off",
            message=f"Workflow handed off from {from_agent.name} to {to_agent.name}",
        )


agent_collaboration_service = AgentCollaborationService()
