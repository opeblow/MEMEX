from __future__ import annotations

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    workspace_id: str
    name: str
    slug: str
    description: str | None = None


class ProjectUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None


class ProjectResponse(BaseModel):
    id: str
    workspace_id: str
    name: str
    slug: str
    description: str | None = None
    created_at: str
    updated_at: str
