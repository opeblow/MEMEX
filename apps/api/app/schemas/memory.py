from __future__ import annotations

from pydantic import BaseModel


class RememberRequest(BaseModel):
    project_id: str
    data: str | None = None
    session_id: str | None = None
    memory_type: str | None = None
    title: str | None = None
    tags: list[str] | None = None
    run_in_background: bool = False


class RememberResponse(BaseModel):
    memory_id: str
    dataset_id: str
    chunk_count: int = 0
    token_count: int = 0
    processing_time_ms: int = 0
    status: str = "processing"


class RecallRequest(BaseModel):
    query: str
    project_id: str
    session_id: str | None = None
    session_only: bool = False
    datasets: list[str] | None = None
    query_type: str | None = None
    top_k: int | None = 15
    only_context: bool = False
    stream: bool = False


class RecallSource(BaseModel):
    text: str
    source: str
    memory_id: str
    chunk_id: str | None = None
    relevance_score: float = 0.0
    evidence: str | None = None
    explanation: str | None = None


class RecallResponse(BaseModel):
    answer: str = ""
    sources: list[RecallSource] = []
    processing_time_ms: int = 0


class ImproveRequest(BaseModel):
    project_id: str
    session_ids: list[str] | None = None
    build_global_context_index: bool = False
    run_in_background: bool = False


class ImproveResponse(BaseModel):
    project_id: str
    status: str = "completed"
    nodes_enriched: int = 0
    edges_added: int = 0
    summaries_generated: int = 0
    processing_time_ms: int = 0


class ForgetRequest(BaseModel):
    project_id: str
    data_id: str | None = None
    dataset: str | None = None
    everything: bool = False
    memory_only: bool = False


class ForgetResponse(BaseModel):
    status: str = "ok"
    deleted_data_ids: list[str] = []
    deleted_graph_nodes: int = 0
    deleted_vectors: int = 0


class MemoryDetailResponse(BaseModel):
    id: str
    project_id: str
    user_id: str
    session_id: str | None = None
    title: str = ""
    memory_type: str = "text"
    status: str = "processing"
    source: str | None = None
    source_url: str | None = None
    file_path: str | None = None
    mime_type: str | None = None
    content_preview: str | None = None
    size_bytes: int | None = None
    token_count: int | None = None
    chunk_count: int | None = None
    importance: float = 0.5
    tags: list[str] = []
    metadata: dict = {}
    created_at: str = ""
    updated_at: str = ""


class MemoryListItem(BaseModel):
    id: str
    title: str = ""
    memory_type: str = "text"
    status: str = "processing"
    importance: float = 0.5
    tags: list[str] = []
    content_preview: str | None = None
    created_at: str = ""
    updated_at: str = ""


class SearchRequest(BaseModel):
    query: str
    project_id: str
    limit: int = 20


class SearchResponse(BaseModel):
    results: list[MemoryDetailResponse] = []
    total: int = 0
    processing_time_ms: int = 0


class MemoryUpdateRequest(BaseModel):
    title: str | None = None
    tags: list[str] | None = None
    importance: float | None = None


class TimelineEventResponse(BaseModel):
    id: str
    project_id: str
    user_id: str
    event_type: str
    data: dict = {}
    created_at: str = ""


class TimelineQueryRequest(BaseModel):
    project_id: str
    from_date: str | None = None
    to_date: str | None = None
    event_types: list[str] | None = None
    limit: int = 50
    offset: int = 0


class TimelineResponse(BaseModel):
    events: list[TimelineEventResponse] = []
    total: int = 0
    summary: dict = {}
