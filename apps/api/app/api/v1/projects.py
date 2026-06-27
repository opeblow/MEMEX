from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUserRequired, DBDep
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate

router = APIRouter()


@router.get("", response_model=list[ProjectResponse])
async def list_projects(user_id: CurrentUserRequired, db: DBDep) -> list[ProjectResponse]:
    projects = await Project.find_by_user_id(db, user_id)
    return [
        ProjectResponse(
            id=str(p.id),
            workspace_id=str(p.workspace_id),
            name=p.name,
            slug=p.slug,
            description=p.description,
            created_at=p.created_at.isoformat(),
            updated_at=p.updated_at.isoformat(),
        )
        for p in projects
    ]


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    user_id: CurrentUserRequired, db: DBDep, body: ProjectCreate
) -> ProjectResponse:
    project = await Project.create(
        db,
        workspace_id=body.workspace_id,
        name=body.name,
        slug=body.slug,
        description=body.description,
        owner_id=user_id,
    )
    return ProjectResponse(
        id=str(project.id),
        workspace_id=str(project.workspace_id),
        name=project.name,
        slug=project.slug,
        description=project.description,
        created_at=project.created_at.isoformat(),
        updated_at=project.updated_at.isoformat(),
    )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(user_id: CurrentUserRequired, db: DBDep, project_id: str) -> ProjectResponse:
    project = await Project.find_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return ProjectResponse(
        id=str(project.id),
        workspace_id=str(project.workspace_id),
        name=project.name,
        slug=project.slug,
        description=project.description,
        created_at=project.created_at.isoformat(),
        updated_at=project.updated_at.isoformat(),
    )


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    user_id: CurrentUserRequired, db: DBDep, project_id: str, body: ProjectUpdate
) -> ProjectResponse:
    project = await Project.update(db, project_id, **body.model_dump(exclude_unset=True))
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return ProjectResponse(
        id=str(project.id),
        workspace_id=str(project.workspace_id),
        name=project.name,
        slug=project.slug,
        description=project.description,
        created_at=project.created_at.isoformat(),
        updated_at=project.updated_at.isoformat(),
    )


@router.delete("/{project_id}")
async def delete_project(user_id: CurrentUserRequired, db: DBDep, project_id: str) -> dict:
    deleted = await Project.delete(db, project_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return {"status": "ok", "message": "Project deleted"}
