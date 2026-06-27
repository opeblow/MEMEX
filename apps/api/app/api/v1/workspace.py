from __future__ import annotations

import secrets
import string

from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUserRequired, DBDep
from app.models.project import Project
from app.schemas.workspace import WorkspaceCreate, WorkspaceResponse, WorkspaceUpdate

router = APIRouter()


def _generate_slug(name: str) -> str:
    base = name.lower().replace(" ", "-")
    safe = "".join(c for c in base if c in string.ascii_lowercase + string.digits + "-")
    suffix = secrets.token_hex(4)
    return f"{safe}-{suffix}"


@router.get("", response_model=list[WorkspaceResponse])
async def list_workspaces(user_id: CurrentUserRequired, db: DBDep) -> list[WorkspaceResponse]:
    from app.models.organization import Organization

    orgs = await Organization.find_by_owner(db, user_id)
    return [
        WorkspaceResponse(
            id=str(o.id),
            name=o.name,
            slug=o.slug,
            description=o.description,
            owner_id=o.owner_id,
            created_at=o.created_at.isoformat(),
            updated_at=o.updated_at.isoformat(),
        )
        for o in orgs
    ]


@router.post("", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    user_id: CurrentUserRequired, db: DBDep, body: WorkspaceCreate
) -> WorkspaceResponse:
    from app.models.organization import Organization
    from app.models.organization_member import OrganizationMember

    slug = _generate_slug(body.name)

    org = await Organization.create(
        db,
        name=body.name,
        slug=slug,
        description=body.company or None,
        owner_id=user_id,
    )

    await OrganizationMember.add_member(db, str(org.id), user_id, role="owner")

    await Project.create(
        db,
        workspace_id=str(org.id),
        name="Default",
        slug="default",
        description="Your default project",
        owner_id=user_id,
    )

    return WorkspaceResponse(
        id=str(org.id),
        name=org.name,
        slug=org.slug,
        description=org.description,
        owner_id=org.owner_id,
        created_at=org.created_at.isoformat(),
        updated_at=org.updated_at.isoformat(),
    )


@router.get("/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(
    user_id: CurrentUserRequired, db: DBDep, workspace_id: str
) -> WorkspaceResponse:
    from app.models.organization import Organization

    org = await Organization.find_by_id(db, workspace_id)
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")

    return WorkspaceResponse(
        id=str(org.id),
        name=org.name,
        slug=org.slug,
        description=org.description,
        owner_id=org.owner_id,
        created_at=org.created_at.isoformat(),
        updated_at=org.updated_at.isoformat(),
    )


@router.patch("/{workspace_id}", response_model=WorkspaceResponse)
async def update_workspace(
    user_id: CurrentUserRequired, db: DBDep, workspace_id: str, body: WorkspaceUpdate
) -> WorkspaceResponse:
    from app.models.organization import Organization

    org = await Organization.find_by_id(db, workspace_id)
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")

    if body.name is not None:
        org.name = body.name
    if body.description is not None:
        org.description = body.description

    await db.commit()
    await db.refresh(org)

    return WorkspaceResponse(
        id=str(org.id),
        name=org.name,
        slug=org.slug,
        description=org.description,
        owner_id=org.owner_id,
        created_at=org.created_at.isoformat(),
        updated_at=org.updated_at.isoformat(),
    )
