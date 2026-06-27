from __future__ import annotations

from pydantic import BaseModel


class AgentResponse(BaseModel):
    id: str
    project_id: str
    user_id: str
    name: str
    description: str | None = None
    agent_type: str = "custom"
    agent_config: dict | None = None
    capabilities: list[str] | None = None
    memory_scope: str = "workspace"
    permissions: dict | None = None
    status: str = "active"
    metadata: dict | None = None
    created_at: str
    updated_at: str


class AgentListResponse(BaseModel):
    agents: list[AgentResponse]
    total: int


class AgentCreate(BaseModel):
    name: str
    description: str | None = None
    agent_type: str = "custom"
    agent_config: dict | None = None
    capabilities: list[str] | None = None
    memory_scope: str = "workspace"
    permissions: dict | None = None


class AgentUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    agent_type: str | None = None
    agent_config: dict | None = None
    capabilities: list[str] | None = None
    memory_scope: str | None = None
    permissions: dict | None = None
    status: str | None = None


class WorkflowResponse(BaseModel):
    id: str
    project_id: str
    agent_id: str
    name: str
    description: str | None = None
    status: str = "queued"
    workflow_type: str = "manual"
    input_data: dict | None = None
    output_data: dict | None = None
    progress_pct: int = 0
    current_step: str | None = None
    error_message: str | None = None
    started_at: str | None = None
    completed_at: str | None = None
    metadata: dict | None = None
    created_at: str
    updated_at: str


class WorkflowListResponse(BaseModel):
    workflows: list[WorkflowResponse]
    total: int


class WorkflowCreate(BaseModel):
    agent_id: str
    name: str
    description: str | None = None
    workflow_type: str = "manual"
    input_data: dict | None = None
    metadata: dict | None = None


class WorkflowUpdate(BaseModel):
    status: str | None = None
    output_data: dict | None = None
    progress_pct: int | None = None
    current_step: str | None = None
    error_message: str | None = None


class TaskExecutionResponse(BaseModel):
    id: str
    project_id: str
    workflow_id: str | None = None
    agent_id: str
    parent_task_id: str | None = None
    name: str
    status: str = "pending"
    input_data: dict | None = None
    output_data: dict | None = None
    started_at: str | None = None
    completed_at: str | None = None
    duration_ms: int | None = None
    error_message: str | None = None
    metadata: dict | None = None
    created_at: str
    updated_at: str


class TaskExecutionListResponse(BaseModel):
    tasks: list[TaskExecutionResponse]
    total: int


class TaskExecutionCreate(BaseModel):
    workflow_id: str | None = None
    parent_task_id: str | None = None
    name: str
    input_data: dict | None = None
    metadata: dict | None = None


class TaskExecutionUpdate(BaseModel):
    status: str | None = None
    output_data: dict | None = None
    started_at: str | None = None
    completed_at: str | None = None
    duration_ms: int | None = None
    error_message: str | None = None


class DecisionResponse(BaseModel):
    id: str
    project_id: str
    agent_id: str
    workflow_id: str | None = None
    task_id: str | None = None
    decision_type: str
    input_context: dict | None = None
    reasoning: str | None = None
    outcome: dict | None = None
    confidence: float | None = None
    metadata: dict | None = None
    created_at: str
    updated_at: str


class DecisionListResponse(BaseModel):
    decisions: list[DecisionResponse]
    total: int


class DecisionCreate(BaseModel):
    agent_id: str
    workflow_id: str | None = None
    task_id: str | None = None
    decision_type: str
    input_context: dict | None = None
    reasoning: str | None = None
    outcome: dict | None = None
    confidence: float | None = None
    metadata: dict | None = None


class ObservabilityEventResponse(BaseModel):
    id: str
    project_id: str
    agent_id: str | None = None
    workflow_id: str | None = None
    task_id: str | None = None
    event_type: str
    event_name: str
    data: dict | None = None
    duration_ms: int | None = None
    level: str = "info"
    created_at: str
    updated_at: str


class ObservabilityEventListResponse(BaseModel):
    events: list[ObservabilityEventResponse]
    total: int


class ObservabilityEventCreate(BaseModel):
    agent_id: str | None = None
    workflow_id: str | None = None
    task_id: str | None = None
    event_type: str
    event_name: str
    data: dict | None = None
    duration_ms: int | None = None
    level: str = "info"


class HandoffRequest(BaseModel):
    from_agent_id: str
    to_agent_id: str
    workflow_id: str
    context: dict | None = None
    message: str | None = None


class HandoffResponse(BaseModel):
    handoff_id: str
    new_workflow_id: str
    status: str
    message: str
