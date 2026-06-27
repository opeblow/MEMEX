from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.memory_trail import MemoryTrail
from app.schemas.reasoning import (
    Explanation,
    MemoryConfidence,
    MemoryContribution,
    RelationshipPath,
    TimelinePath,
    TrailStep,
)
from app.schemas.trail import MemoryEvidenceResponse, MemoryTrailResponse


class TrailService:
    async def create_trail(
        self,
        db: AsyncSession,
        project_id: str,
        user_id: str,
        question: str,
        answer: str | None = None,
        trail_steps: list[dict[str, Any]] | None = None,
        memory_ids: list[str] | None = None,
        confidence_score: float | None = None,
        processing_time_ms: int | None = None,
        model_used: str | None = None,
    ) -> MemoryTrail:
        trail = MemoryTrail(
            project_id=project_id,
            user_id=user_id,
            question=question,
            answer=answer,
            trail_steps=trail_steps or [],
            memory_ids=memory_ids or [],
            confidence_score=confidence_score,
            processing_time_ms=processing_time_ms,
            model_used=model_used,
        )
        db.add(trail)
        await db.commit()
        await db.refresh(trail)
        return trail

    async def get_trail(self, db: AsyncSession, trail_id: str) -> MemoryTrailResponse | None:
        trail = await db.get(MemoryTrail, trail_id)
        if trail is None:
            return None
        return self._to_response(trail)

    async def list_trails(
        self, db: AsyncSession, project_id: str, limit: int = 50, offset: int = 0
    ) -> list[MemoryTrailResponse]:
        result = await db.execute(
            select(MemoryTrail)
            .where(MemoryTrail.project_id == project_id)
            .order_by(MemoryTrail.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        trails = list(result.scalars().all())
        return [self._to_response(t) for t in trails]

    async def get_evidence(
        self,
        db: AsyncSession,
        memory_id: str,
        relationships: list[dict[str, Any]] | None = None,
        timeline_events: list[dict[str, Any]] | None = None,
    ) -> MemoryEvidenceResponse | None:
        from app.models.memory import Memory
        memory = await db.get(Memory, memory_id)
        if memory is None:
            return None
        return MemoryEvidenceResponse(
            memory_id=memory.id,
            content_preview=memory.content_preview,
            source=memory.source,
            memory_type=memory.memory_type,
            importance=memory.importance,
            tags=memory.tags,
            relationships=relationships or [],
            timeline_events=timeline_events or [],
            created_at=memory.created_at.isoformat() if memory.created_at else None,
        )

    def _to_response(self, trail: MemoryTrail) -> MemoryTrailResponse:
        trail_steps = None
        if trail.trail_steps:
            trail_steps = [TrailStep(**s) if isinstance(s, dict) else s for s in trail.trail_steps]
        return MemoryTrailResponse(
            id=trail.id,
            project_id=trail.project_id,
            question=trail.question,
            answer=trail.answer,
            trail_steps=trail_steps,
            memory_ids=trail.memory_ids,
            confidence_score=trail.confidence_score,
            processing_time_ms=trail.processing_time_ms,
            created_at=trail.created_at.isoformat() if trail.created_at else "",
        )

    def build_explanation(
        self,
        summary: str,
        memory_contributions: list[MemoryContribution],
        relationship_paths: list[RelationshipPath] | None = None,
        timeline_paths: list[TimelinePath] | None = None,
        confidence: MemoryConfidence | None = None,
    ) -> Explanation:
        return Explanation(
            summary=summary,
            memories_used=memory_contributions,
            relationship_paths=relationship_paths or [],
            timeline_paths=timeline_paths or [],
            confidence=confidence,
        )


trail_service = TrailService()
