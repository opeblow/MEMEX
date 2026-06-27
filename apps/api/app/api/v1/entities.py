from __future__ import annotations

from fastapi import APIRouter, Query

from app.api.deps import CurrentUserRequired, DBDep
from app.models.entity import Entity
from app.schemas.entity import (
    EntityListResponse,
    EntityResponse,
    RelationshipListResponse,
    RelationshipResponse,
)
from app.services.entity_store import entity_store_service

router = APIRouter()


@router.get("/entities", response_model=EntityListResponse)
async def list_entities(
    db: DBDep,
    user: CurrentUserRequired,
    project_id: str = Query(..., description="Project ID"),
    entity_type: str | None = Query(None, description="Filter by entity type"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    if entity_type:
        entities = await Entity.find_by_type(db, project_id, entity_type, limit)
    else:
        entities = await entity_store_service.get_entities(db, project_id, limit, offset)
    return EntityListResponse(
        entities=[
            EntityResponse(
                id=e.id,
                name=e.name,
                entity_type=e.entity_type,
                description=e.description,
                metadata=e.metadata_,
                created_at=e.created_at.isoformat() if e.created_at else "",
                updated_at=e.updated_at.isoformat() if e.updated_at else "",
            )
            for e in entities
        ],
        total=len(entities),
    )


@router.get("/relationships", response_model=RelationshipListResponse)
async def list_relationships(
    db: DBDep,
    user: CurrentUserRequired,
    project_id: str = Query(..., description="Project ID"),
    limit: int = Query(200, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    relationships = await entity_store_service.get_relationships(db, project_id, limit, offset)
    return RelationshipListResponse(
        relationships=[
            RelationshipResponse(
                id=r.id,
                source_entity_id=r.source_entity_id,
                target_entity_id=r.target_entity_id,
                relationship_type=r.relationship_type,
                strength=r.strength,
                metadata=r.metadata_,
                created_at=r.created_at.isoformat() if r.created_at else "",
            )
            for r in relationships
        ],
        total=len(relationships),
    )


@router.get("/entities/search", response_model=EntityListResponse)
async def search_entities(
    db: DBDep,
    user: CurrentUserRequired,
    project_id: str = Query(...),
    query: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
):
    entities = await Entity.search(db, project_id, query, limit)
    return EntityListResponse(
        entities=[
            EntityResponse(
                id=e.id,
                name=e.name,
                entity_type=e.entity_type,
                description=e.description,
                metadata=e.metadata_,
                created_at=e.created_at.isoformat() if e.created_at else "",
                updated_at=e.updated_at.isoformat() if e.updated_at else "",
            )
            for e in entities
        ],
        total=len(entities),
    )
