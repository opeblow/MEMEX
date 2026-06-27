from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.memory import Memory
from app.models.memory_event import MemoryEvent


class TimelineIntelligenceService:
    async def what_changed(
        self,
        db: AsyncSession,
        project_id: str,
        entity_name: str | None = None,
        since_days: int = 30,
    ) -> list[dict[str, Any]]:
        since = datetime.now(UTC) - timedelta(days=since_days)
        query = (
            select(Memory)
            .where(
                Memory.project_id == project_id,
                Memory.created_at >= since,
                Memory.status.in_(["indexed", "archived"]),
            )
            .order_by(Memory.created_at.desc())
        )
        result = await db.execute(query)
        memories = list(result.scalars().all())
        changes = []
        for m in memories:
            if entity_name and entity_name.lower() not in (m.content_preview or "").lower():
                if not m.tags or entity_name.lower() not in [t.lower() for t in m.tags]:
                    continue
            changes.append({
                "memory_id": m.id,
                "title": m.title,
                "memory_type": m.memory_type,
                "content_preview": m.content_preview,
                "tags": m.tags,
                "timestamp": m.created_at.isoformat() if m.created_at else None,
            })
        return changes

    async def what_happened_before(
        self,
        db: AsyncSession,
        project_id: str,
        memory_id: str,
        lookback_days: int = 30,
    ) -> list[dict[str, Any]]:
        result = await db.execute(select(Memory).where(Memory.id == memory_id))
        target = result.scalar_one_or_none()
        if target is None or target.created_at is None:
            return []
        since = target.created_at - timedelta(days=lookback_days)
        query = (
            select(Memory)
            .where(
                Memory.project_id == project_id,
                Memory.created_at >= since,
                Memory.created_at < target.created_at,
                Memory.status.in_(["indexed", "archived"]),
            )
            .order_by(Memory.created_at.desc())
        )
        result = await db.execute(query)
        return [
            {
                "memory_id": m.id,
                "title": m.title,
                "memory_type": m.memory_type,
                "content_preview": m.content_preview,
                "timestamp": m.created_at.isoformat() if m.created_at else None,
            }
            for m in list(result.scalars().all())
        ]

    async def influences(
        self,
        db: AsyncSession,
        project_id: str,
        memory_id: str,
        max_hops: int = 2,
    ) -> list[dict[str, Any]]:
        from app.services.memory_retriever import memory_retriever
        result = await db.execute(select(Memory).where(Memory.id == memory_id))
        target = result.scalar_one_or_none()
        if target is None:
            return []
        query_text = target.content_preview or target.title or ""
        search_results = await memory_retriever.hybrid_search(
            db=db,
            user_id="system",
            query=query_text,
            project_id=project_id,
            top_k=20,
        )
        return [
            {
                "memory_id": m.get("memory_id"),
                "title": m.get("title"),
                "relevance_score": m.get("relevance_score"),
                "explanation": m.get("explanation"),
            }
            for m in search_results
            if m.get("memory_id") != memory_id
        ][:10]

    async def timeline_context(
        self,
        db: AsyncSession,
        project_id: str,
        days: int = 7,
    ) -> dict[str, Any]:
        since = datetime.now(UTC) - timedelta(days=days)
        events_query = (
            select(MemoryEvent)
            .where(
                MemoryEvent.project_id == project_id,
                MemoryEvent.created_at >= since,
            )
            .order_by(MemoryEvent.created_at.desc())
        )
        events_result = await db.execute(events_query)
        events = list(events_result.scalars().all())
        memories_query = (
            select(Memory)
            .where(
                Memory.project_id == project_id,
                Memory.created_at >= since,
                Memory.status.in_(["indexed", "archived"]),
            )
            .order_by(Memory.created_at.desc())
        )
        memories_result = await db.execute(memories_query)
        memories = list(memories_result.scalars().all())
        return {
            "event_count": len(events),
            "memory_count": len(memories),
            "events": [
                {
                    "id": e.id,
                    "event_type": e.event_type,
                    "data": e.event_data,
                    "timestamp": e.created_at.isoformat() if e.created_at else None,
                }
                for e in events
            ],
            "recent_memories": [
                {
                    "id": m.id,
                    "title": m.title,
                    "type": m.memory_type,
                    "timestamp": m.created_at.isoformat() if m.created_at else None,
                }
                for m in memories
            ],
        }


timeline_intelligence_service = TimelineIntelligenceService()
