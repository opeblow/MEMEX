from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from app.schemas.reasoning import Explanation, TrailStep


class MemoryTrailResponse(BaseModel):
    id: str
    project_id: str
    question: str
    answer: str | None = None
    trail_steps: list[TrailStep] | None = None
    memory_ids: list[str] | None = None
    confidence_score: float | None = None
    processing_time_ms: int | None = None
    explanation: Explanation | None = None
    created_at: str


class MemoryEvidenceResponse(BaseModel):
    memory_id: str
    content_preview: str | None = None
    source: str | None = None
    memory_type: str | None = None
    importance: float = 0
    tags: list[str] | None = None
    relationships: list[dict[str, Any]] = Field(default_factory=list)
    timeline_events: list[dict[str, Any]] = Field(default_factory=list)
    created_at: str | None = None
