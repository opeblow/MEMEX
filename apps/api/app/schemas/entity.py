from __future__ import annotations

from pydantic import BaseModel, Field


class EntityResponse(BaseModel):
    id: str
    name: str
    entity_type: str
    description: str | None = None
    metadata: dict | None = None
    created_at: str
    updated_at: str


class RelationshipResponse(BaseModel):
    id: str
    source_entity_id: str
    target_entity_id: str
    relationship_type: str
    strength: float
    metadata: dict | None = None
    created_at: str


class EntityListResponse(BaseModel):
    entities: list[EntityResponse]
    total: int


class RelationshipListResponse(BaseModel):
    relationships: list[RelationshipResponse]
    total: int


class EntityDetailResponse(EntityResponse):
    relationships: list[RelationshipResponse] = Field(default_factory=list)
