from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, Request
from sqlalchemy import select
from starlette.responses import Response

from app.api.deps import CurrentUserRequired, DBDep
from app.models.collaboration import (
    Comment,
    Invitation,
    MemoryCollection,
    MemoryPermission,
    ShareLink,
)
from app.models.organization import Organization
from app.models.organization_member import OrganizationMember
from app.schemas.collaboration import (
    AuditLogListResponse,
    AuditLogResponse,
    CollectionItemAdd,
    CollectionItemRemove,
    CommentCreate,
    CommentListResponse,
    CommentResponse,
    CommentUpdate,
    InvitationAccept,
    InvitationCreate,
    InvitationListResponse,
    InvitationResponse,
    MemoryCollectionCreate,
    MemoryCollectionListResponse,
    MemoryCollectionResponse,
    MemoryCollectionUpdate,
    MemoryPermissionCreate,
    MemoryPermissionListResponse,
    MemoryPermissionResponse,
    MemoryPermissionUpdate,
    ShareLinkCreate,
    ShareLinkListResponse,
    ShareLinkResponse,
)
from app.services.audit import audit_service
from app.services.collaboration import (
    collection_service,
    comment_service,
    invite_service,
    permission_service,
    role_service,
    share_link_service,
)
from app.services.export import export_service

router = APIRouter()


def _collection_to_response(c: MemoryCollection, memory_count: int = 0) -> MemoryCollectionResponse:
    return MemoryCollectionResponse(
        id=c.id,
        project_id=c.project_id,
        user_id=c.user_id,
        name=c.name,
        description=c.description,
        is_shared=c.is_shared or False,
        metadata=c.metadata_,
        memory_count=memory_count,
        created_at=c.created_at.isoformat() if c.created_at else "",
        updated_at=c.updated_at.isoformat() if c.updated_at else "",
    )


def _comment_to_response(c: Comment) -> CommentResponse:
    return CommentResponse(
        id=c.id,
        memory_id=c.memory_id,
        user_id=c.user_id,
        content=c.content,
        parent_id=c.parent_id,
        created_at=c.created_at.isoformat() if c.created_at else "",
        updated_at=c.updated_at.isoformat() if c.updated_at else "",
    )


def _permission_to_response(p: MemoryPermission) -> MemoryPermissionResponse:
    return MemoryPermissionResponse(
        id=p.id,
        memory_id=p.memory_id,
        collection_id=p.collection_id,
        user_id=p.user_id,
        role=p.role,
        granted_by=p.granted_by,
        created_at=p.created_at.isoformat() if p.created_at else "",
        updated_at=p.updated_at.isoformat() if p.updated_at else "",
    )


def _share_link_to_response(link: ShareLink) -> ShareLinkResponse:
    from app.config import settings
    return ShareLinkResponse(
        id=link.id,
        project_id=link.project_id,
        memory_id=link.memory_id,
        collection_id=link.collection_id,
        token=link.token,
        permission=link.permission,
        url=f"{settings.app_url}/share/{link.token}",
        expires_at=link.expires_at,
        max_uses=link.max_uses,
        use_count=link.use_count or 0,
        created_by=link.created_by,
        is_active=link.is_active,
        created_at=link.created_at.isoformat() if link.created_at else "",
        updated_at=link.updated_at.isoformat() if link.updated_at else "",
    )


def _invitation_to_response(i: Invitation) -> InvitationResponse:
    return InvitationResponse(
        id=i.id,
        workspace_id=i.workspace_id,
        invited_by=i.invited_by,
        email=i.email,
        token=i.token,
        role=i.role,
        status=i.status,
        expires_at=i.expires_at,
        accepted_at=i.accepted_at,
        created_at=i.created_at.isoformat() if i.created_at else "",
        updated_at=i.updated_at.isoformat() if i.updated_at else "",
    )


def _audit_log_to_response(log_entry: any) -> AuditLogResponse:
    return AuditLogResponse(
        id=log_entry.id,
        project_id=log_entry.project_id,
        user_id=log_entry.user_id,
        action=log_entry.action,
        resource_type=log_entry.resource_type,
        resource_id=log_entry.resource_id,
        details=log_entry.details,
        ip_address=log_entry.ip_address,
        created_at=log_entry.created_at.isoformat() if log_entry.created_at else "",
        updated_at=log_entry.updated_at.isoformat() if log_entry.updated_at else "",
    )


@router.get("/workspaces/{workspace_id}/members")
async def list_workspace_members(db: DBDep, workspace_id: str):
    org = await Organization.find_by_id(db, workspace_id)
    if not org:
        raise HTTPException(status_code=404, detail="Workspace not found")
    from sqlalchemy import select as sa_select

    from app.models.user import User
    result = await db.execute(
        sa_select(OrganizationMember, User.display_name, User.email)
        .join(User, OrganizationMember.user_id == User.id)
        .where(OrganizationMember.organization_id == workspace_id)
    )
    rows = result.all()
    members = []
    for member, display_name, email in rows:
        members.append({
            "user_id": member.user_id,
            "display_name": display_name,
            "email": email,
            "role": member.role,
            "joined_at": member.joined_at.isoformat() if member.joined_at else "",
        })
    return {"members": members, "total": len(members)}


@router.patch("/workspaces/{workspace_id}/members/{user_id}/role")
async def update_member_role(
    db: DBDep,
    user: CurrentUserRequired,
    workspace_id: str,
    target_user_id: str,
    role: str = Query(...),
):
    can_admin = await role_service.require_role(db, user, workspace_id, "admin")
    if not can_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    if role not in ("viewer", "editor", "admin", "owner"):
        raise HTTPException(status_code=400, detail="Invalid role")
    result = await db.execute(
        select(OrganizationMember).where(
            OrganizationMember.organization_id == workspace_id,
            OrganizationMember.user_id == target_user_id,
        )
    )
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    if member.role == "owner":
        raise HTTPException(status_code=400, detail="Cannot change owner role")
    member.role = role
    await db.commit()
    return {"status": "updated", "user_id": target_user_id, "role": role}


@router.delete("/workspaces/{workspace_id}/members/{user_id}")
async def remove_member(
    db: DBDep,
    user: CurrentUserRequired,
    workspace_id: str,
    target_user_id: str,
):
    can_admin = await role_service.require_role(db, user, workspace_id, "admin")
    if not can_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    result = await db.execute(
        select(OrganizationMember).where(
            OrganizationMember.organization_id == workspace_id,
            OrganizationMember.user_id == target_user_id,
        )
    )
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    await db.delete(member)
    await db.commit()
    return {"status": "removed"}


@router.get("/workspaces/{workspace_id}/activity")
async def workspace_activity(
    db: DBDep,
    workspace_id: str,
    limit: int = 50,
    offset: int = 0,
):
    items = await audit_service.get_activity_feed(db, workspace_id, limit, offset)
    return {"activities": items, "total": len(items)}


@router.post("/collections", response_model=MemoryCollectionResponse)
async def create_collection(
    db: DBDep,
    user: CurrentUserRequired,
    request: MemoryCollectionCreate,
    project_id: str,
):
    collection = await collection_service.create(
        db=db, project_id=project_id, user_id=user, request=request
    )
    return _collection_to_response(collection)


@router.get("/collections", response_model=MemoryCollectionListResponse)
async def list_collections(
    db: DBDep,
    user: CurrentUserRequired,
    project_id: str,
    limit: int = 50,
    offset: int = 0,
):
    collections = await collection_service.list_by_project(db, project_id, limit, offset)
    result = []
    for c in collections:
        count = await collection_service.get_memory_count(db, c.id)
        result.append(_collection_to_response(c, count))
    return MemoryCollectionListResponse(collections=result, total=len(result))


@router.get("/collections/{collection_id}", response_model=MemoryCollectionResponse)
async def get_collection(db: DBDep, collection_id: str):
    collection = await collection_service.get(db, collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    count = await collection_service.get_memory_count(db, collection_id)
    return _collection_to_response(collection, count)


@router.patch("/collections/{collection_id}", response_model=MemoryCollectionResponse)
async def update_collection(db: DBDep, collection_id: str, request: MemoryCollectionUpdate):
    collection = await collection_service.update(db, collection_id, request)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    count = await collection_service.get_memory_count(db, collection_id)
    return _collection_to_response(collection, count)


@router.delete("/collections/{collection_id}")
async def delete_collection(db: DBDep, user: CurrentUserRequired, collection_id: str):
    deleted = await collection_service.delete(db, collection_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Collection not found")
    return {"status": "deleted"}


@router.post("/collections/{collection_id}/memories")
async def add_memory_to_collection(
    db: DBDep,
    user: CurrentUserRequired,
    collection_id: str,
    request: CollectionItemAdd,
):
    added = await collection_service.add_memory(
        db, collection_id, request.memory_id, added_by=user
    )
    if not added:
        return {"status": "already_exists"}
    return {"status": "added"}


@router.delete("/collections/{collection_id}/memories")
async def remove_memory_from_collection(
    db: DBDep,
    user: CurrentUserRequired,
    collection_id: str,
    request: CollectionItemRemove,
):
    removed = await collection_service.remove_memory(db, collection_id, request.memory_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Memory not in collection")
    return {"status": "removed"}


@router.get("/collections/{collection_id}/memories")
async def list_collection_memories(db: DBDep, collection_id: str):
    items = await collection_service.list_memories(db, collection_id)
    from sqlalchemy import select as sa_select

    from app.models.memory import Memory
    memory_ids = [item.memory_id for item in items]
    if not memory_ids:
        return {"memories": [], "total": 0}
    result = await db.execute(
        sa_select(Memory).where(Memory.id.in_(memory_ids))
    )
    memories = list(result.scalars().all())
    from app.services.memory_serializer import memory_serializer
    return {
        "memories": [memory_serializer.memory_to_detail(m) for m in memories],
        "total": len(memories),
        "collection_id": collection_id,
    }


@router.post("/memories/{memory_id}/comments", response_model=CommentResponse)
async def create_comment(
    db: DBDep,
    user: CurrentUserRequired,
    memory_id: str,
    request: CommentCreate,
):
    comment = await comment_service.create(
        db=db, memory_id=memory_id, user_id=user, request=request
    )
    resp = _comment_to_response(comment)
    try:
        from app.models.user import User
        u = await db.get(User, user)
        if u:
            resp.user_name = u.display_name
    except Exception:
        pass
    return resp


@router.get("/memories/{memory_id}/comments", response_model=CommentListResponse)
async def list_comments(db: DBDep, memory_id: str):
    comments = await comment_service.list_by_memory(db, memory_id)
    result = []
    for c in comments:
        resp = _comment_to_response(c)
        try:
            from app.models.user import User
            u = await db.get(User, c.user_id)
            if u:
                resp.user_name = u.display_name
        except Exception:
            pass
        result.append(resp)
    return CommentListResponse(comments=result, total=len(result))


@router.patch("/comments/{comment_id}", response_model=CommentResponse)
async def update_comment(
    db: DBDep,
    user: CurrentUserRequired,
    comment_id: str,
    request: CommentUpdate,
):
    comment = await comment_service.update(db, comment_id, user, request)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or not authorized")
    return _comment_to_response(comment)


@router.delete("/comments/{comment_id}")
async def delete_comment(db: DBDep, user: CurrentUserRequired, comment_id: str):
    deleted = await comment_service.delete(db, comment_id, user)
    if not deleted:
        raise HTTPException(status_code=404, detail="Comment not found or not authorized")
    return {"status": "deleted"}


@router.post("/permissions", response_model=MemoryPermissionResponse)
async def grant_permission(
    db: DBDep,
    user: CurrentUserRequired,
    request: MemoryPermissionCreate,
):
    perm = await permission_service.grant(db=db, user_id=user, request=request)
    return _permission_to_response(perm)


@router.get("/permissions/{memory_id}", response_model=MemoryPermissionListResponse)
async def list_permissions(db: DBDep, memory_id: str):
    perms = await permission_service.list_by_memory(db, memory_id)
    return MemoryPermissionListResponse(
        permissions=[_permission_to_response(p) for p in perms],
        total=len(perms),
    )


@router.patch("/permissions/{perm_id}", response_model=MemoryPermissionResponse)
async def update_permission(db: DBDep, perm_id: str, request: MemoryPermissionUpdate):
    perm = await permission_service.update(db, perm_id, request)
    if not perm:
        raise HTTPException(status_code=404, detail="Permission not found")
    return _permission_to_response(perm)


@router.delete("/permissions/{perm_id}")
async def revoke_permission(db: DBDep, user: CurrentUserRequired, perm_id: str):
    revoked = await permission_service.revoke(db, perm_id)
    if not revoked:
        raise HTTPException(status_code=404, detail="Permission not found")
    return {"status": "revoked"}


@router.post("/share-links", response_model=ShareLinkResponse)
async def create_share_link(
    db: DBDep,
    user: CurrentUserRequired,
    project_id: str,
    request: ShareLinkCreate,
):
    link = await share_link_service.create(
        db=db, project_id=project_id, user_id=user, request=request
    )
    return _share_link_to_response(link)


@router.get("/share-links", response_model=ShareLinkListResponse)
async def list_share_links(
    db: DBDep,
    user: CurrentUserRequired,
    project_id: str,
    limit: int = 50,
    offset: int = 0,
):
    links = await share_link_service.list_by_project(db, project_id, limit, offset)
    return ShareLinkListResponse(
        links=[_share_link_to_response(lk) for lk in links],
        total=len(links),
    )


@router.delete("/share-links/{link_id}")
async def delete_share_link(db: DBDep, user: CurrentUserRequired, link_id: str):
    deactivated = await share_link_service.deactivate(db, link_id)
    if not deactivated:
        raise HTTPException(status_code=404, detail="Share link not found")
    return {"status": "deactivated"}


@router.get("/share/{token}")
async def access_shared_content(db: DBDep, token: str, request: Request):
    link = await share_link_service.get_by_token(db, token)
    if not link or not link.is_active:
        raise HTTPException(status_code=404, detail="Share link not found or inactive")
    valid = await share_link_service.use_link(db, link)
    if not valid:
        raise HTTPException(status_code=410, detail="Share link expired or max uses reached")

    from app.models.memory import Memory
    if link.memory_id:
        memory = await db.get(Memory, link.memory_id)
        if not memory:
            raise HTTPException(status_code=404, detail="Memory not found")
        from app.services.memory_serializer import memory_serializer
        return {"type": "memory", "data": memory_serializer.memory_to_detail(memory)}

    if link.collection_id:
        items = await collection_service.list_memories(db, link.collection_id)
        memory_ids = [item.memory_id for item in items]
        if memory_ids:
            from sqlalchemy import select as sa_select
            result = await db.execute(
                sa_select(Memory).where(Memory.id.in_(memory_ids))
            )
            memories = list(result.scalars().all())
            from app.services.memory_serializer import memory_serializer
            return {
                "type": "collection",
                "data": [memory_serializer.memory_to_detail(m) for m in memories],
            }
        return {"type": "collection", "data": []}

    raise HTTPException(status_code=404, detail="No content found")


@router.post("/workspaces/{workspace_id}/invitations", response_model=InvitationResponse)
async def create_invitation(
    db: DBDep,
    user: CurrentUserRequired,
    workspace_id: str,
    request: InvitationCreate,
):
    can_admin = await role_service.require_role(db, user, workspace_id, "admin")
    if not can_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    invitation = await invite_service.create(
        db=db, workspace_id=workspace_id, invited_by=user, request=request
    )
    return _invitation_to_response(invitation)


@router.get("/workspaces/{workspace_id}/invitations", response_model=InvitationListResponse)
async def list_invitations(
    db: DBDep,
    user: CurrentUserRequired,
    workspace_id: str,
    limit: int = 50,
    offset: int = 0,
):
    can_view = await role_service.require_role(db, user, workspace_id, "viewer")
    if not can_view:
        raise HTTPException(status_code=403, detail="Not authorized")
    invitations = await invite_service.list_by_workspace(db, workspace_id, limit, offset)
    return InvitationListResponse(
        invitations=[_invitation_to_response(i) for i in invitations],
        total=len(invitations),
    )


@router.post("/invitations/accept")
async def accept_invitation(
    db: DBDep,
    user: CurrentUserRequired,
    request: InvitationAccept,
):
    invitation = await invite_service.accept(db, request.token, user)
    if not invitation:
        raise HTTPException(status_code=400, detail="Invalid or expired invitation")
    return {"status": "accepted", "workspace_id": invitation.workspace_id, "role": invitation.role}


@router.delete("/invitations/{invitation_id}")
async def cancel_invitation(db: DBDep, user: CurrentUserRequired, invitation_id: str):
    cancelled = await invite_service.cancel(db, invitation_id)
    if not cancelled:
        raise HTTPException(status_code=404, detail="Invitation not found")
    return {"status": "cancelled"}


@router.get("/audit-logs", response_model=AuditLogListResponse)
async def list_audit_logs(
    db: DBDep,
    user: CurrentUserRequired,
    project_id: str,
    resource_type: str | None = None,
    resource_id: str | None = None,
    limit: int = 100,
    offset: int = 0,
):
    if resource_type and resource_id:
        logs = await audit_service.find_by_resource(db, resource_type, resource_id, limit)
    else:
        logs = await audit_service.find_by_project(db, project_id, limit, offset)
    return AuditLogListResponse(
        logs=[_audit_log_to_response(lg) for lg in logs],
        total=len(logs),
    )


@router.get("/activity-feed")
async def get_activity_feed(
    db: DBDep,
    user: CurrentUserRequired,
    project_id: str,
    limit: int = 50,
    offset: int = 0,
):
    items = await audit_service.get_activity_feed(db, project_id, limit, offset)
    return {"activities": items, "total": len(items)}


@router.get("/workspaces/{workspace_id}/export")
async def export_project(
    db: DBDep,
    user: CurrentUserRequired,
    workspace_id: str,
    format: str = Query("json", regex="^(json|markdown|csv)$"),
):
    return {"message": "Export initiated", "workspace_id": workspace_id, "format": format}


@router.get("/export/collections/{collection_id}")
async def export_collection(
    db: DBDep,
    user: CurrentUserRequired,
    collection_id: str,
    format: str = Query("json", regex="^(json|markdown|csv)$"),
):
    collection = await collection_service.get(db, collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    content = await export_service.export_collection(db, collection_id, format)
    media_type = {
        "json": "application/json",
        "markdown": "text/markdown",
        "csv": "text/csv",
    }.get(format, "application/json")
    return Response(content=content, media_type=media_type)


@router.get("/export/projects/{project_id}")
async def export_project_memories(
    db: DBDep,
    user: CurrentUserRequired,
    project_id: str,
    format: str = Query("json", regex="^(json|markdown)$"),
):
    content = await export_service.export_project_memories(db, project_id, format)
    media_type = {
        "json": "application/json",
        "markdown": "text/markdown",
    }.get(format, "application/json")
    return Response(content=content, media_type=media_type)
