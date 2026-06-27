from __future__ import annotations

from pydantic import BaseModel


class SourceResponse(BaseModel):
    id: str
    project_id: str
    source_type: str
    display_name: str | None = None
    url: str | None = None
    file_path: str | None = None
    mime_type: str | None = None
    size_bytes: int | None = None
    metadata: dict | None = None
    memory_count: int = 0
    last_import_at: str | None = None
    created_at: str
    updated_at: str


class SourceListResponse(BaseModel):
    sources: list[SourceResponse]
    total: int


class ImportJobResponse(BaseModel):
    id: str
    project_id: str
    source_id: str | None = None
    source_type: str
    status: str
    progress_pct: int = 0
    current_step: str | None = None
    error_message: str | None = None
    total_items: int = 0
    processed_items: int = 0
    memory_ids: list[str] | None = None
    metadata: dict | None = None
    created_at: str
    updated_at: str


class ImportJobListResponse(BaseModel):
    jobs: list[ImportJobResponse]
    total: int


class ImportRequest(BaseModel):
    project_id: str
    source_type: str
    data: str | None = None
    url: str | None = None
    display_name: str | None = None
    metadata: dict | None = None


class ImportResponse(BaseModel):
    job_id: str
    source_id: str | None = None
    status: str
    message: str


class MemoryVersionResponse(BaseModel):
    id: str
    memory_id: str
    version_type: str
    content_preview: str | None = None
    title: str | None = None
    tags: list[str] | None = None
    importance: float = 0.5
    metadata: dict | None = None
    created_at: str


class ImportProgressEvent(BaseModel):
    job_id: str
    status: str
    progress_pct: int
    current_step: str | None = None
    error_message: str | None = None
    memory_id: str | None = None
