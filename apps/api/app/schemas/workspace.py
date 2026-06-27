from __future__ import annotations

from pydantic import BaseModel


class WorkspaceCreate(BaseModel):
    name: str
    role: str = "individual"
    company: str | None = None
    primary_goal: str = "research"


class WorkspaceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class WorkspaceResponse(BaseModel):
    id: str
    name: str
    slug: str
    description: str | None = None
    owner_id: str
    settings: dict = {}
    created_at: str
    updated_at: str
