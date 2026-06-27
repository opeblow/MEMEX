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
