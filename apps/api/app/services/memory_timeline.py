from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger

from app.models.memory_event import MemoryEvent

logger = get_logger()


class MemoryTimeline:
    async def record_event(
        self,
        db: AsyncSession,
        project_id: str,
        user_id: str,
        event_type: str,
        data: dict | None = None,
    ) -> str:
        event_id = str(uuid.uuid4())
        event = MemoryEvent(
            id=event_id,
            project_id=project_id,
            user_id=user_id,
            event_type=event_type,
            event_data=data or {},
        )
        db.add(event)
        await db.commit()
        await db.refresh(event)
        return event_id

    async def get_events(
        self,
        db: AsyncSession,
        project_id: str,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        event_types: list[str] | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict]:
        conditions = [MemoryEvent.project_id == project_id]
        if from_date:
            conditions.append(MemoryEvent.created_at >= from_date)
        if to_date:
            conditions.append(MemoryEvent.created_at <= to_date)
        if event_types:
            conditions.append(MemoryEvent.event_type.in_(event_types))

        result = await db.execute(
            select(MemoryEvent)
            .where(*conditions)
            .order_by(MemoryEvent.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        events = list(result.scalars().all())
        return [
            {
                "id": e.id,
                "project_id": e.project_id,
                "user_id": e.user_id,
                "event_type": e.event_type,
                "data": e.event_data or {},
                "created_at": e.created_at.isoformat() if e.created_at else "",
            }
            for e in events
        ]

    async def get_timeline_summary(
        self, db: AsyncSession, project_id: str
    ) -> dict:
        total = await db.execute(
            select(MemoryEvent).where(MemoryEvent.project_id == project_id)
        )
        all_events = list(total.scalars().all())
        event_types: dict[str, int] = {}
        for e in all_events:
            event_types[e.event_type] = event_types.get(e.event_type, 0) + 1
        return {
            "total_events": len(all_events),
            "event_types": event_types,
            "project_id": project_id,
        }


memory_timeline = MemoryTimeline()
