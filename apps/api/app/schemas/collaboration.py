from __future__ import annotations

from pydantic import BaseModel


class MemoryCollectionResponse(BaseModel):
    id: str
    project_id: str
    user_id: str
    name: str
    description: str | None = None
    is_shared: bool = False
    metadata: dict | None = None
    memory_count: int = 0
    created_at: str
    updated_at: str


class MemoryCollectionListResponse(BaseModel):
    collections: list[MemoryCollectionResponse]
    total: int


class MemoryCollectionCreate(BaseModel):
    name: str
    description: str | None = None
    is_shared: bool = False
    metadata: dict | None = None


class MemoryCollectionUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_shared: bool | None = None
    metadata: dict | None = None


class CollectionItemAdd(BaseModel):
    memory_id: str


class CollectionItemRemove(BaseModel):
    memory_id: str


class CommentResponse(BaseModel):
    id: str
    memory_id: str
    user_id: str
    content: str
    parent_id: str | None = None
    user_name: str | None = None
    created_at: str
    updated_at: str


class CommentListResponse(BaseModel):
    comments: list[CommentResponse]
    total: int


class CommentCreate(BaseModel):
    content: str
    parent_id: str | None = None


class CommentUpdate(BaseModel):
    content: str


class MemoryPermissionResponse(BaseModel):
    id: str
    memory_id: str | None = None
    collection_id: str | None = None
    user_id: str
    role: str
    granted_by: str | None = None
    created_at: str
    updated_at: str


class MemoryPermissionListResponse(BaseModel):
    permissions: list[MemoryPermissionResponse]
    total: int


class MemoryPermissionCreate(BaseModel):
    memory_id: str | None = None
    collection_id: str | None = None
    user_id: str
    role: str


class MemoryPermissionUpdate(BaseModel):
    role: str


class ShareLinkResponse(BaseModel):
    id: str
    project_id: str
    memory_id: str | None = None
    collection_id: str | None = None
    token: str
    permission: str = "viewer"
    url: str = ""
    expires_at: str | None = None
    max_uses: int | None = None
    use_count: int = 0
    created_by: str
    is_active: bool = True
    created_at: str
    updated_at: str


class ShareLinkListResponse(BaseModel):
    links: list[ShareLinkResponse]
    total: int


class ShareLinkCreate(BaseModel):
    memory_id: str | None = None
    collection_id: str | None = None
    permission: str = "viewer"
    expires_at: str | None = None
    max_uses: int | None = None


class InvitationResponse(BaseModel):
    id: str
    workspace_id: str
    invited_by: str
    email: str
    token: str
    role: str = "viewer"
    status: str = "pending"
    expires_at: str | None = None
    accepted_at: str | None = None
    created_at: str
    updated_at: str


class InvitationListResponse(BaseModel):
    invitations: list[InvitationResponse]
    total: int


class InvitationCreate(BaseModel):
    email: str
    role: str = "viewer"


class InvitationAccept(BaseModel):
    token: str


class AuditLogResponse(BaseModel):
    id: str
    project_id: str
    user_id: str
    action: str
    resource_type: str
    resource_id: str | None = None
    details: dict | None = None
    ip_address: str | None = None
    created_at: str
    updated_at: str


class AuditLogListResponse(BaseModel):
    logs: list[AuditLogResponse]
    total: int


class ActivityFeedItem(BaseModel):
    id: str
    user_id: str
    user_name: str | None = None
    action: str
    resource_type: str
    resource_id: str | None = None
    details: dict | None = None
    created_at: str
