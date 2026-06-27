from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class TrailStep(BaseModel):
    step: int
    name: str
    description: str
    data: dict[str, Any] = Field(default_factory=dict)
    memory_ids: list[str] = Field(default_factory=list)
    duration_ms: float = 0


class ConfidenceFactors(BaseModel):
    source_count: int = 0
    relationship_strength: float = 0
    recency_score: float = 0
    agreement_score: float = 0
    entity_consistency: float = 0
    graph_connectivity: float = 0


class MemoryConfidence(BaseModel):
    score: float
    factors: ConfidenceFactors
    label: str


class MemoryContribution(BaseModel):
    memory_id: str
    title: str | None = None
    relevance: float = 0
    evidence: str | None = None
    explanation: str | None = None


class RelationshipPath(BaseModel):
    from_entity: str
    to_entity: str
    relationship_type: str
    strength: float


class TimelinePath(BaseModel):
    event_type: str
    memory_id: str
    timestamp: datetime | None = None
    description: str | None = None


class Explanation(BaseModel):
    summary: str
    memories_used: list[MemoryContribution] = Field(default_factory=list)
    relationship_paths: list[RelationshipPath] = Field(default_factory=list)
    timeline_paths: list[TimelinePath] = Field(default_factory=list)
    confidence: MemoryConfidence | None = None


class ReasoningRequest(BaseModel):
    query: str
    project_id: str
    include_trail: bool = True
    include_explanation: bool = True
    top_k: int = 20


class ReasoningStep(BaseModel):
    step: int
    name: str
    description: str
    result: dict[str, Any] = Field(default_factory=dict)


class ReasoningResponse(BaseModel):
    answer: str
    trail_id: str | None = None
    explanation: Explanation | None = None
    trail: list[TrailStep] | None = None
    processing_time_ms: int = 0


class ReasoningStreamEvent(BaseModel):
    event: str
    data: dict[str, Any] = Field(default_factory=dict)
    content: str | None = None
