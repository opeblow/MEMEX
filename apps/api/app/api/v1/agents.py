from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.api.deps import CurrentUserRequired, DBDep
from app.models.agent import Agent, AgentObservabilityEvent, AgentWorkflow, Decision, TaskExecution
from app.schemas.agent import (
    AgentCreate,
    AgentListResponse,
    AgentResponse,
    AgentUpdate,
    DecisionCreate,
    DecisionListResponse,
    DecisionResponse,
    HandoffRequest,
    HandoffResponse,
    ObservabilityEventCreate,
    ObservabilityEventListResponse,
    ObservabilityEventResponse,
    TaskExecutionCreate,
    TaskExecutionListResponse,
    TaskExecutionResponse,
    TaskExecutionUpdate,
    WorkflowCreate,
    WorkflowListResponse,
    WorkflowResponse,
    WorkflowUpdate,
)
from app.services.agent_collaboration import agent_collaboration_service
from app.services.agent_decision_history import decision_history_service
from app.services.agent_observability import agent_observability_service
from app.services.agent_registry import agent_registry_service
from app.services.agent_task_history import task_history_service
from app.services.agent_workflow import agent_workflow_service

router = APIRouter()


def _agent_to_response(a: Agent) -> AgentResponse:
    return AgentResponse(
        id=a.id,
        project_id=a.project_id,
        user_id=a.user_id,
        name=a.name,
        description=a.description,
        agent_type=a.agent_type,
        agent_config=a.model_config,
        capabilities=a.capabilities,
        memory_scope=a.memory_scope,
        permissions=a.permissions,
        status=a.status,
        metadata=a.metadata_,
        created_at=a.created_at.isoformat() if a.created_at else "",
        updated_at=a.updated_at.isoformat() if a.updated_at else "",
    )


def _workflow_to_response(w: AgentWorkflow) -> WorkflowResponse:
    return WorkflowResponse(
        id=w.id,
        project_id=w.project_id,
        agent_id=w.agent_id,
        name=w.name,
        description=w.description,
        status=w.status,
        workflow_type=w.workflow_type,
        input_data=w.input_data,
        output_data=w.output_data,
        progress_pct=w.progress_pct or 0,
        current_step=w.current_step,
        error_message=w.error_message,
        started_at=w.started_at,
        completed_at=w.completed_at,
        metadata=w.metadata_,
        created_at=w.created_at.isoformat() if w.created_at else "",
        updated_at=w.updated_at.isoformat() if w.updated_at else "",
    )


def _task_to_response(t: TaskExecution) -> TaskExecutionResponse:
    return TaskExecutionResponse(
        id=t.id,
        project_id=t.project_id,
        workflow_id=t.workflow_id,
        agent_id=t.agent_id,
        parent_task_id=t.parent_task_id,
        name=t.name,
        status=t.status,
        input_data=t.input_data,
        output_data=t.output_data,
        started_at=t.started_at,
        completed_at=t.completed_at,
        duration_ms=t.duration_ms,
        error_message=t.error_message,
        metadata=t.metadata_,
        created_at=t.created_at.isoformat() if t.created_at else "",
        updated_at=t.updated_at.isoformat() if t.updated_at else "",
    )


def _decision_to_response(d: Decision) -> DecisionResponse:
    return DecisionResponse(
        id=d.id,
        project_id=d.project_id,
        agent_id=d.agent_id,
        workflow_id=d.workflow_id,
        task_id=d.task_id,
        decision_type=d.decision_type,
        input_context=d.input_context,
        reasoning=d.reasoning,
        outcome=d.outcome,
        confidence=d.confidence,
        metadata=d.metadata_,
        created_at=d.created_at.isoformat() if d.created_at else "",
        updated_at=d.updated_at.isoformat() if d.updated_at else "",
    )


def _observability_to_response(e: AgentObservabilityEvent) -> ObservabilityEventResponse:
    return ObservabilityEventResponse(
        id=e.id,
        project_id=e.project_id,
        agent_id=e.agent_id,
        workflow_id=e.workflow_id,
        task_id=e.task_id,
        event_type=e.event_type,
        event_name=e.event_name,
        data=e.data,
        duration_ms=e.duration_ms,
        level=e.level,
        created_at=e.created_at.isoformat() if e.created_at else "",
        updated_at=e.updated_at.isoformat() if e.updated_at else "",
    )


@router.post("/agents", response_model=AgentResponse)
async def create_agent(db: DBDep, user: CurrentUserRequired, request: AgentCreate, project_id: str):
    agent = await agent_registry_service.create_agent(
        db=db, project_id=project_id, user_id=user, request=request
    )
    return _agent_to_response(agent)


@router.get("/agents", response_model=AgentListResponse)
async def list_agents(
    db: DBDep,
    user: CurrentUserRequired,
    project_id: str,
    limit: int = 50,
    offset: int = 0,
):
    agents = await agent_registry_service.list_agents(db, project_id, limit, offset)
    return AgentListResponse(
        agents=[_agent_to_response(a) for a in agents],
        total=len(agents),
    )


@router.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(db: DBDep, agent_id: str):
    agent = await agent_registry_service.get_agent(db, agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return _agent_to_response(agent)


@router.patch("/agents/{agent_id}", response_model=AgentResponse)
async def update_agent(db: DBDep, agent_id: str, request: AgentUpdate):
    agent = await agent_registry_service.update_agent(db, agent_id, request)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return _agent_to_response(agent)


@router.delete("/agents/{agent_id}")
async def delete_agent(db: DBDep, user: CurrentUserRequired, agent_id: str):
    deleted = await agent_registry_service.delete_agent(db, agent_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"status": "deleted", "agent_id": agent_id}


@router.post("/agents/{agent_id}/workflows", response_model=WorkflowResponse)
async def create_workflow(
    db: DBDep,
    user: CurrentUserRequired,
    agent_id: str,
    request: WorkflowCreate,
    project_id: str,
):
    agent = await agent_registry_service.get_agent(db, agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    workflow = await agent_workflow_service.create_workflow(
        db=db, project_id=project_id, agent_id=agent_id, request=request
    )
    return _workflow_to_response(workflow)


@router.get("/workflows", response_model=WorkflowListResponse)
async def list_workflows(
    db: DBDep,
    user: CurrentUserRequired,
    project_id: str,
    limit: int = 50,
    offset: int = 0,
):
    workflows = await agent_workflow_service.list_workflows(db, project_id, limit, offset)
    return WorkflowListResponse(
        workflows=[_workflow_to_response(w) for w in workflows],
        total=len(workflows),
    )


@router.get("/workflows/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(db: DBDep, workflow_id: str):
    workflow = await agent_workflow_service.get_workflow(db, workflow_id)
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return _workflow_to_response(workflow)


@router.patch("/workflows/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(db: DBDep, workflow_id: str, request: WorkflowUpdate):
    workflow = await agent_workflow_service.update_workflow(db, workflow_id, request)
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return _workflow_to_response(workflow)


@router.delete("/workflows/{workflow_id}")
async def delete_workflow(db: DBDep, user: CurrentUserRequired, workflow_id: str):
    deleted = await agent_workflow_service.delete_workflow(db, workflow_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return {"status": "deleted", "workflow_id": workflow_id}


@router.get("/agents/{agent_id}/tasks", response_model=TaskExecutionListResponse)
async def list_agent_tasks(
    db: DBDep,
    agent_id: str,
    limit: int = 50,
    offset: int = 0,
):
    tasks = await task_history_service.list_by_agent(db, agent_id, limit, offset)
    return TaskExecutionListResponse(
        tasks=[_task_to_response(t) for t in tasks],
        total=len(tasks),
    )


@router.get("/workflows/{workflow_id}/tasks", response_model=TaskExecutionListResponse)
async def list_workflow_tasks(db: DBDep, workflow_id: str):
    tasks = await task_history_service.list_by_workflow(db, workflow_id)
    return TaskExecutionListResponse(
        tasks=[_task_to_response(t) for t in tasks],
        total=len(tasks),
    )


@router.post("/agents/{agent_id}/tasks", response_model=TaskExecutionResponse)
async def create_task(
    db: DBDep,
    user: CurrentUserRequired,
    agent_id: str,
    project_id: str,
    request: TaskExecutionCreate,
):
    task = await task_history_service.create_task(
        db=db, project_id=project_id, agent_id=agent_id, request=request
    )
    return _task_to_response(task)


@router.patch("/tasks/{task_id}", response_model=TaskExecutionResponse)
async def update_task(db: DBDep, task_id: str, request: TaskExecutionUpdate):
    task = await task_history_service.update_task(db, task_id, request)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return _task_to_response(task)


@router.get("/tasks/{task_id}", response_model=TaskExecutionResponse)
async def get_task(db: DBDep, task_id: str):
    task = await task_history_service.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return _task_to_response(task)


@router.post("/decisions", response_model=DecisionResponse)
async def record_decision(
    db: DBDep,
    user: CurrentUserRequired,
    project_id: str,
    request: DecisionCreate,
):
    decision = await decision_history_service.record_decision(
        db=db, project_id=project_id, request=request
    )
    return _decision_to_response(decision)


@router.get("/agents/{agent_id}/decisions", response_model=DecisionListResponse)
async def list_agent_decisions(
    db: DBDep,
    agent_id: str,
    limit: int = 50,
    offset: int = 0,
):
    decisions = await decision_history_service.list_by_agent(db, agent_id, limit, offset)
    return DecisionListResponse(
        decisions=[_decision_to_response(d) for d in decisions],
        total=len(decisions),
    )


@router.get("/workflows/{workflow_id}/decisions", response_model=DecisionListResponse)
async def list_workflow_decisions(db: DBDep, workflow_id: str):
    decisions = await decision_history_service.list_by_workflow(db, workflow_id)
    return DecisionListResponse(
        decisions=[_decision_to_response(d) for d in decisions],
        total=len(decisions),
    )


@router.get("/decisions/{decision_id}", response_model=DecisionResponse)
async def get_decision(db: DBDep, decision_id: str):
    decision = await decision_history_service.get_decision(db, decision_id)
    if decision is None:
        raise HTTPException(status_code=404, detail="Decision not found")
    return _decision_to_response(decision)


@router.post("/observability/events", response_model=ObservabilityEventResponse)
async def record_observability_event(
    db: DBDep,
    user: CurrentUserRequired,
    project_id: str,
    request: ObservabilityEventCreate,
):
    event = await agent_observability_service.record_event(
        db=db, project_id=project_id, request=request
    )
    return _observability_to_response(event)


@router.get("/observability/events", response_model=ObservabilityEventListResponse)
async def list_observability_events(
    db: DBDep,
    user: CurrentUserRequired,
    project_id: str,
    agent_id: str | None = None,
    event_type: str | None = None,
    limit: int = 100,
    offset: int = 0,
):
    if agent_id:
        events = await agent_observability_service.list_by_agent(db, agent_id, limit, offset)
    elif event_type:
        events = await agent_observability_service.list_by_type(db, project_id, event_type, limit)
    else:
        events = await agent_observability_service.list_by_project(db, project_id, limit, offset)
    return ObservabilityEventListResponse(
        events=[_observability_to_response(e) for e in events],
        total=len(events),
    )


@router.get("/observability/events/{event_id}", response_model=ObservabilityEventResponse)
async def get_observability_event(db: DBDep, event_id: str):
    from app.models.agent import AgentObservabilityEvent
    event = await db.get(AgentObservabilityEvent, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return _observability_to_response(event)


@router.post("/agents/handoff", response_model=HandoffResponse)
async def handoff_workflow(
    db: DBDep,
    user: CurrentUserRequired,
    project_id: str,
    request: HandoffRequest,
):
    try:
        result = await agent_collaboration_service.handoff(
            db=db, project_id=project_id, request=request
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
