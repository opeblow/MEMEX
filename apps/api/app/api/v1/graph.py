from __future__ import annotations

from fastapi import APIRouter

from app.api.deps import CurrentUserRequired
from app.schemas.graph import GraphSnapshot, NeighborhoodRequest

router = APIRouter()


@router.post("/neighborhood", response_model=GraphSnapshot)
async def get_neighborhood(
    user_id: CurrentUserRequired,
    body: NeighborhoodRequest,
) -> GraphSnapshot:
    return GraphSnapshot(nodes=[], edges=[])


@router.get("/snapshot/{project_id}", response_model=GraphSnapshot)
async def get_graph_snapshot(
    user_id: CurrentUserRequired,
    project_id: str,
) -> GraphSnapshot:
    return GraphSnapshot(nodes=[], edges=[])
