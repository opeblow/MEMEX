from __future__ import annotations

import secrets
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.collaboration import (
    Comment,
    Invitation,
    MemoryCollection,
    MemoryCollectionItem,
    MemoryPermission,
    ShareLink,
)
from app.models.organization_member import OrganizationMember
from app.schemas.collaboration import (
    CommentCreate,
    CommentUpdate,
    InvitationCreate,
    MemoryCollectionCreate,
    MemoryCollectionUpdate,
    MemoryPermissionCreate,
    MemoryPermissionUpdate,
    ShareLinkCreate,
)
from app.services.audit import audit_service


def _now() -> str:
    return datetime.now(UTC).isoformat()


class RoleService:
    ROLES = ["viewer", "editor", "admin", "owner"]

    def has_access(self, user_role: str | None, required_role: str) -> bool:
        if not user_role:
            return False
        hierarchy = {"viewer": 0, "editor": 1, "admin": 2, "owner": 3}
        return hierarchy.get(user_role, -1) >= hierarchy.get(required_role, 0)

    async def get_user_role(
        self, db: AsyncSession, user_id: str, workspace_id: str
    ) -> str | None:
        result = await db.execute(
            select(OrganizationMember).where(
                OrganizationMember.organization_id == workspace_id,
                OrganizationMember.user_id == user_id,
            )
        )
        member = result.scalar_one_or_none()
        return member.role if member else None

    async def get_memory_permission(
        self, db: AsyncSession, user_id: str, memory_id: str
    ) -> str | None:
        result = await db.execute(
            select(MemoryPermission).where(
                MemoryPermission.memory_id == memory_id,
                MemoryPermission.user_id == user_id,
            )
        )
        perm = result.scalar_one_or_none()
        return perm.role if perm else None

    async def require_role(
        self, db: AsyncSession, user_id: str, workspace_id: str, required_role: str
    ) -> bool:
        role = await self.get_user_role(db, user_id, workspace_id)
        return self.has_access(role, required_role)


role_service = RoleService()


class CollectionService:
    async def create(
        self,
        db: AsyncSession,
        project_id: str,
        user_id: str,
        request: MemoryCollectionCreate,
    ) -> MemoryCollection:
        collection = MemoryCollection(
            project_id=project_id,
            user_id=user_id,
            name=request.name,
            description=request.description,
            is_shared=request.is_shared or False,
            metadata_=request.metadata,
        )
        db.add(collection)
        await db.commit()
        await db.refresh(collection)

        await audit_service.record(
            db=db,
            project_id=project_id,
            user_id=user_id,
            action="collection.created",
            resource_type="collection",
            resource_id=collection.id,
            details={"name": collection.name},
        )
        return collection

    async def get(self, db: AsyncSession, collection_id: str) -> MemoryCollection | None:
        return await MemoryCollection.find_by_id(db, collection_id)

    async def list_by_project(
        self, db: AsyncSession, project_id: str, limit: int = 50, offset: int = 0
    ) -> list[MemoryCollection]:
        return await MemoryCollection.find_by_project(db, project_id, limit, offset)

    async def update(
        self, db: AsyncSession, collection_id: str, request: MemoryCollectionUpdate
    ) -> MemoryCollection | None:
        collection = await MemoryCollection.find_by_id(db, collection_id)
        if not collection:
            return None
        update_data = request.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if key == "metadata":
                collection.metadata_ = value
            else:
                setattr(collection, key, value)
        await db.commit()
        await db.refresh(collection)
        return collection

    async def delete(self, db: AsyncSession, collection_id: str) -> bool:
        collection = await MemoryCollection.find_by_id(db, collection_id)
        if not collection:
            return False
        await db.execute(
            MemoryCollectionItem.__table__.delete().where(
                MemoryCollectionItem.collection_id == collection_id
            )
        )
        await db.delete(collection)
        await db.commit()
        return True

    async def add_memory(
        self, db: AsyncSession, collection_id: str, memory_id: str, added_by: str
    ) -> bool:
        existing = await db.execute(
            select(MemoryCollectionItem).where(
                MemoryCollectionItem.collection_id == collection_id,
                MemoryCollectionItem.memory_id == memory_id,
            )
        )
        if existing.scalar_one_or_none():
            return False
        item = MemoryCollectionItem(
            collection_id=collection_id,
            memory_id=memory_id,
            added_by=added_by,
            added_at=_now(),
        )
        db.add(item)
        await db.commit()
        return True

    async def remove_memory(
        self, db: AsyncSession, collection_id: str, memory_id: str
    ) -> bool:
        result = await db.execute(
            select(MemoryCollectionItem).where(
                MemoryCollectionItem.collection_id == collection_id,
                MemoryCollectionItem.memory_id == memory_id,
            )
        )
        item = result.scalar_one_or_none()
        if not item:
            return False
        await db.delete(item)
        await db.commit()
        return True

    async def list_memories(
        self, db: AsyncSession, collection_id: str
    ) -> list[MemoryCollectionItem]:
        return await MemoryCollectionItem.find_by_collection(db, collection_id)

    async def get_memory_count(self, db: AsyncSession, collection_id: str) -> int:
        items = await MemoryCollectionItem.find_by_collection(db, collection_id)
        return len(items)


collection_service = CollectionService()


class CommentService:
    async def create(
        self, db: AsyncSession, memory_id: str, user_id: str, request: CommentCreate
    ) -> Comment:
        comment = Comment(
            memory_id=memory_id,
            user_id=user_id,
            content=request.content,
            parent_id=request.parent_id,
        )
        db.add(comment)
        await db.commit()
        await db.refresh(comment)

        await audit_service.record(
            db=db,
            project_id="",
            user_id=user_id,
            action="comment.created",
            resource_type="comment",
            resource_id=comment.id,
            details={"memory_id": memory_id, "content_preview": request.content[:100]},
        )
        return comment

    async def list_by_memory(self, db: AsyncSession, memory_id: str) -> list[Comment]:
        return await Comment.find_by_memory(db, memory_id)

    async def update(
        self, db: AsyncSession, comment_id: str, user_id: str, request: CommentUpdate
    ) -> Comment | None:
        comment = await Comment.find_by_id(db, comment_id)
        if not comment or comment.user_id != user_id:
            return None
        comment.content = request.content
        await db.commit()
        await db.refresh(comment)
        return comment

    async def delete(self, db: AsyncSession, comment_id: str, user_id: str) -> bool:
        comment = await Comment.find_by_id(db, comment_id)
        if not comment or comment.user_id != user_id:
            return False
        await db.delete(comment)
        await db.commit()
        return True


comment_service = CommentService()


class PermissionService:
    async def grant(
        self, db: AsyncSession, user_id: str, request: MemoryPermissionCreate
    ) -> MemoryPermission:
        perm = MemoryPermission(
            memory_id=request.memory_id,
            collection_id=request.collection_id,
            user_id=request.user_id,
            role=request.role,
            granted_by=user_id,
        )
        db.add(perm)
        await db.commit()
        await db.refresh(perm)
        return perm

    async def update(
        self, db: AsyncSession, perm_id: str, request: MemoryPermissionUpdate
    ) -> MemoryPermission | None:
        perm = await MemoryPermission.find_by_id(db, perm_id)
        if not perm:
            return None
        perm.role = request.role
        await db.commit()
        await db.refresh(perm)
        return perm

    async def revoke(self, db: AsyncSession, perm_id: str) -> bool:
        perm = await MemoryPermission.find_by_id(db, perm_id)
        if not perm:
            return False
        await db.delete(perm)
        await db.commit()
        return True

    async def list_by_memory(self, db: AsyncSession, memory_id: str) -> list[MemoryPermission]:
        return await MemoryPermission.find_by_memory(db, memory_id)


permission_service = PermissionService()


class ShareLinkService:
    async def create(
        self, db: AsyncSession, project_id: str, user_id: str, request: ShareLinkCreate
    ) -> ShareLink:
        token = secrets.token_urlsafe(32)
        link = ShareLink(
            project_id=project_id,
            memory_id=request.memory_id,
            collection_id=request.collection_id,
            token=token,
            permission=request.permission,
            expires_at=request.expires_at,
            max_uses=request.max_uses,
            created_by=user_id,
        )
        db.add(link)
        await db.commit()
        await db.refresh(link)
        return link

    async def get_by_token(self, db: AsyncSession, token: str) -> ShareLink | None:
        return await ShareLink.find_by_token(db, token)

    async def use_link(self, db: AsyncSession, link: ShareLink) -> bool:
        if not link.is_active:
            return False
        if link.expires_at and _now() > link.expires_at:
            link.is_active = False
            await db.commit()
            return False
        if link.max_uses and link.use_count >= link.max_uses:
            link.is_active = False
            await db.commit()
            return False
        link.use_count += 1
        await db.commit()
        return True

    async def deactivate(self, db: AsyncSession, link_id: str) -> bool:
        link = await db.get(ShareLink, link_id)
        if not link:
            return False
        link.is_active = False
        await db.commit()
        return True

    async def list_by_project(
        self, db: AsyncSession, project_id: str, limit: int = 50, offset: int = 0
    ) -> list[ShareLink]:
        return await ShareLink.find_by_project(db, project_id, limit, offset)


share_link_service = ShareLinkService()


class InviteService:
    async def create(
        self,
        db: AsyncSession,
        workspace_id: str,
        invited_by: str,
        request: InvitationCreate,
    ) -> Invitation:
        token = secrets.token_urlsafe(24)
        invitation = Invitation(
            workspace_id=workspace_id,
            invited_by=invited_by,
            email=request.email,
            token=token,
            role=request.role,
            status="pending",
        )
        db.add(invitation)
        await db.commit()
        await db.refresh(invitation)

        try:
            from app.services.email import email_service
            await email_service._send(
                to=request.email,
                subject="You've been invited to MEMEX",
                html=(
                    "<p>You've been invited to join a MEMEX workspace."
                    f" Click <a href='{settings.app_url}/invite?token={token}'>"
                    "here</a> to accept.</p>"
                ),
            )
        except Exception:
            pass

        return invitation

    async def accept(self, db: AsyncSession, token: str, user_id: str) -> Invitation | None:
        invitation = await Invitation.find_by_token(db, token)
        if not invitation or invitation.status != "pending":
            return None
        if invitation.expires_at and _now() > invitation.expires_at:
            invitation.status = "expired"
            await db.commit()
            return None

        existing = await db.execute(
            select(OrganizationMember).where(
                OrganizationMember.organization_id == invitation.workspace_id,
                OrganizationMember.user_id == user_id,
            )
        )
        if not existing.scalar_one_or_none():
            await OrganizationMember.add_member(
                db, invitation.workspace_id, user_id, role=invitation.role
            )

        invitation.status = "accepted"
        invitation.accepted_at = _now()
        await db.commit()
        await db.refresh(invitation)
        return invitation

    async def list_by_workspace(
        self, db: AsyncSession, workspace_id: str, limit: int = 50, offset: int = 0
    ) -> list[Invitation]:
        return await Invitation.find_by_workspace(db, workspace_id, limit, offset)

    async def cancel(self, db: AsyncSession, invitation_id: str) -> bool:
        invitation = await db.get(Invitation, invitation_id)
        if not invitation:
            return False
        invitation.status = "cancelled"
        await db.commit()
        return True


invite_service = InviteService()
