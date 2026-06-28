from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.collaboration import AuditLog


class AuditService:
    async def record(
        self,
        db: AsyncSession,
        project_id: str,
        user_id: str,
        action: str,
        resource_type: str,
        resource_id: str | None = None,
        details: dict | None = None,
        ip_address: str | None = None,
    ) -> AuditLog:
        log = AuditLog(
            project_id=project_id,
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
        )
        db.add(log)
        await db.commit()
        await db.refresh(log)
        return log

    async def find_by_project(
        self, db: AsyncSession, project_id: str, limit: int = 100, offset: int = 0
    ) -> list[AuditLog]:
        return await AuditLog.find_by_project(db, project_id, limit, offset)

    async def find_by_resource(
        self, db: AsyncSession, resource_type: str, resource_id: str, limit: int = 50
    ) -> list[AuditLog]:
        return await AuditLog.find_by_resource(db, resource_type, resource_id, limit)

    async def get_activity_feed(
        self, db: AsyncSession, project_id: str, limit: int = 50, offset: int = 0
    ) -> list[dict]:
        logs = await AuditLog.find_by_project(db, project_id, limit, offset)
        items = []
        for log in logs:
            user_name = None
            try:
                from app.models.user import User
                result = await db.execute(select(User).where(User.id == log.user_id))
                user = result.scalar_one_or_none()
                if user:
                    user_name = user.display_name
            except Exception:
                pass
            items.append({
                "id": log.id,
                "user_id": log.user_id,
                "user_name": user_name,
                "action": log.action,
                "resource_type": log.resource_type,
                "resource_id": log.resource_id,
                "details": log.details or {},
                "created_at": log.created_at.isoformat() if log.created_at else "",
            })
        return items


audit_service = AuditService()
