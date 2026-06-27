from __future__ import annotations

from fastapi import APIRouter

from app.api.v1 import analytics, auth, graph, memory, profile, projects, timeline, workspace

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(memory.router, prefix="", tags=["memory"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(workspace.router, prefix="/workspaces", tags=["workspaces"])
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(graph.router, prefix="/graph", tags=["graph"])
api_router.include_router(timeline.router, prefix="", tags=["timeline"])
