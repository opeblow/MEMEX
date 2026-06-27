from __future__ import annotations

from fastapi import APIRouter

from app.api.deps import CurrentUserRequired

router = APIRouter()


@router.get("/summary/{project_id}")
async def get_project_summary(user_id: CurrentUserRequired, project_id: str) -> dict:
    return {
        "project_id": project_id,
        "total_memories": 0,
        "total_chunks": 0,
        "total_graph_nodes": 0,
        "total_graph_edges": 0,
        "recent_activity": [],
    }


@router.get("/activity")
async def get_activity(user_id: CurrentUserRequired) -> dict:
    return {
        "events": [],
    }
