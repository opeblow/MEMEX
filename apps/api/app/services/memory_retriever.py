from __future__ import annotations

import time
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger

from app.models.memory import Memory
from app.services.cognee_adapter import cognee_adapter
from app.services.memory_ranker import MemoryRanker, memory_ranker

logger = get_logger()


class MemoryRetriever:
    def __init__(self, ranker: MemoryRanker = memory_ranker):
        self.ranker = ranker

    async def semantic_search(
        self,
        db: AsyncSession,
        query: str,
        project_id: str,
        top_k: int = 15,
    ) -> list[dict]:
        result = await db.execute(
            select(Memory)
            .where(
                Memory.project_id == project_id,
                Memory.status.in_(["indexed", "archived"]),
            )
            .order_by(Memory.importance.desc())
            .limit(top_k * 2)
        )
        memories = list(result.scalars().all())

        query_lower = query.lower()
        scored: list[dict] = []
        for m in memories:
            score = 0.0
            if m.title and query_lower in m.title.lower():
                score += 0.4
            if m.content_preview and query_lower in m.content_preview.lower():
                score += 0.3
            if m.tags and any(query_lower in t.lower() for t in m.tags):
                score += 0.2
            score += m.importance * 0.1
            scored.append({
                "text": m.content_preview or "",
                "source": "vector",
                "memory_id": m.id,
                "chunk_id": None,
                "relevance_score": score,
                "evidence": None,
                "memory_type": m.memory_type,
                "importance": m.importance,
            })

        scored.sort(key=lambda x: x["relevance_score"], reverse=True)
        return scored[:top_k]

    async def graph_search(
        self,
        user_id: str,
        query: str,
        project_id: str,
        session_id: str | None = None,
        top_k: int = 15,
    ) -> list[dict]:
        cognee_result = await cognee_adapter.recall(
            user_id=user_id,
            query=query,
            project_id=project_id,
            session_id=session_id,
            top_k=top_k,
            only_context=True,
        )
        return cognee_result.get("sources", [])

    async def timeline_search(
        self,
        db: AsyncSession,
        project_id: str,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        top_k: int = 50,
    ) -> list[dict]:
        conditions = [
            Memory.project_id == project_id,
            Memory.status.in_(["indexed", "archived"]),
        ]
        if from_date:
            conditions.append(Memory.created_at >= from_date)
        if to_date:
            conditions.append(Memory.created_at <= to_date)

        result = await db.execute(
            select(Memory)
            .where(*conditions)
            .order_by(Memory.created_at.desc())
            .limit(top_k)
        )
        memories = list(result.scalars().all())
        return [
            {
                "text": m.content_preview or "",
                "source": "timeline",
                "memory_id": m.id,
                "chunk_id": None,
                "relevance_score": 1.0,
                "evidence": None,
                "memory_type": m.memory_type,
                "importance": m.importance,
                "created_at": m.created_at.isoformat() if m.created_at else "",
            }
            for m in memories
        ]

    async def source_search(
        self,
        db: AsyncSession,
        project_id: str,
        source: str | None = None,
        memory_type: str | None = None,
        top_k: int = 50,
    ) -> list[dict]:
        conditions = [
            Memory.project_id == project_id,
            Memory.status.in_(["indexed", "archived"]),
        ]
        if source:
            conditions.append(Memory.source == source)
        if memory_type:
            conditions.append(Memory.memory_type == memory_type)

        result = await db.execute(
            select(Memory)
            .where(*conditions)
            .order_by(Memory.created_at.desc())
            .limit(top_k)
        )
        memories = list(result.scalars().all())
        return [
            {
                "text": m.content_preview or "",
                "source": m.source or "unknown",
                "memory_id": m.id,
                "chunk_id": None,
                "relevance_score": 1.0,
                "evidence": None,
                "memory_type": m.memory_type,
                "importance": m.importance,
            }
            for m in memories
        ]

    async def entity_search(
        self,
        db: AsyncSession,
        project_id: str,
        entity_name: str,
        top_k: int = 20,
    ) -> list[dict]:
        from sqlalchemy import or_
        result = await db.execute(
            select(Memory)
            .where(
                Memory.project_id == project_id,
                Memory.status.in_(["indexed", "archived"]),
                or_(
                    Memory.content_preview.ilike(f"%{entity_name}%"),
                    Memory.title.ilike(f"%{entity_name}%"),
                ),
            )
            .order_by(Memory.importance.desc())
            .limit(top_k)
        )
        memories = list(result.scalars().all())
        return [
            {
                "text": m.content_preview or "",
                "source": "entity",
                "memory_id": m.id,
                "chunk_id": None,
                "relevance_score": 0.9,
                "evidence": f"Entity '{entity_name}' found in memory",
                "memory_type": m.memory_type,
                "importance": m.importance,
                "title": m.title,
                "created_at": m.created_at,
            }
            for m in memories
        ]

    async def tag_search(
        self,
        db: AsyncSession,
        project_id: str,
        tag: str,
        top_k: int = 20,
    ) -> list[dict]:
        result = await db.execute(
            select(Memory)
            .where(
                Memory.project_id == project_id,
                Memory.status.in_(["indexed", "archived"]),
                Memory.tags.any(tag),
            )
            .order_by(Memory.importance.desc())
            .limit(top_k)
        )
        memories = list(result.scalars().all())
        return [
            {
                "text": m.content_preview or "",
                "source": "tag",
                "memory_id": m.id,
                "chunk_id": None,
                "relevance_score": 0.85,
                "evidence": f"Tag '{tag}' matches memory",
                "memory_type": m.memory_type,
                "importance": m.importance,
                "title": m.title,
                "created_at": m.created_at,
            }
            for m in memories
        ]

    async def recent_search(
        self,
        db: AsyncSession,
        project_id: str,
        limit: int = 20,
    ) -> list[dict]:
        result = await db.execute(
            select(Memory)
            .where(
                Memory.project_id == project_id,
                Memory.status.in_(["indexed", "archived"]),
            )
            .order_by(Memory.created_at.desc())
            .limit(limit)
        )
        memories = list(result.scalars().all())
        return [
            {
                "text": m.content_preview or "",
                "source": "recent",
                "memory_id": m.id,
                "chunk_id": None,
                "relevance_score": 0.7,
                "evidence": None,
                "memory_type": m.memory_type,
                "importance": m.importance,
                "title": m.title,
                "created_at": m.created_at,
            }
            for m in memories
        ]

    async def frequently_referenced_search(
        self,
        db: AsyncSession,
        project_id: str,
        limit: int = 20,
    ) -> list[dict]:
        result = await db.execute(
            select(Memory)
            .where(
                Memory.project_id == project_id,
                Memory.status.in_(["indexed", "archived"]),
            )
            .order_by(Memory.importance.desc())
            .limit(limit)
        )
        memories = list(result.scalars().all())
        return [
            {
                "text": m.content_preview or "",
                "source": "frequently_referenced",
                "memory_id": m.id,
                "chunk_id": None,
                "relevance_score": m.importance,
                "evidence": None,
                "memory_type": m.memory_type,
                "importance": m.importance,
                "title": m.title,
                "created_at": m.created_at,
            }
            for m in memories
        ]

    async def multi_strategy_search(
        self,
        db: AsyncSession,
        user_id: str,
        query: str,
        project_id: str,
        top_k: int = 20,
    ) -> list[dict]:
        start = time.monotonic()
        semantic_results = await self.semantic_search(
            db=db, query=query, project_id=project_id, top_k=top_k
        )
        graph_results = await self.graph_search(
            user_id=user_id, query=query, project_id=project_id, top_k=top_k
        )
        recent_results = await self.recent_search(db=db, project_id=project_id, limit=10)
        freq_refs = await self.frequently_referenced_search(
            db=db, project_id=project_id, limit=10
        )
        combined = semantic_results + graph_results + recent_results + freq_refs
        seen: set[str] = set()
        unique: list[dict] = []
        for src in combined:
            mid = src.get("memory_id", "")
            if mid and mid not in seen:
                seen.add(mid)
                unique.append(src)
        ranked_sources = self.ranker.rank(unique, query)
        result = [
            {
                "text": r.text,
                "source": r.source,
                "memory_id": r.memory_id,
                "chunk_id": r.chunk_id,
                "relevance_score": r.relevance_score,
                "evidence": r.evidence,
                "explanation": r.explanation,
                "memory_type": r.get("memory_type") if isinstance(r, dict) else None,
                "importance": r.get("importance") if isinstance(r, dict) else None,
                "title": r.get("title") if isinstance(r, dict) else None,
                "created_at": r.get("created_at") if isinstance(r, dict) else None,
            }
            for r in ranked_sources
        ]
        elapsed = int((time.monotonic() - start) * 1000)
        logger.info(
            "Multi-strategy search complete",
            project_id=project_id,
            sources_count=len(result),
            elapsed_ms=elapsed,
        )
        return result

    async def hybrid_search(
        self,
        db: AsyncSession,
        user_id: str,
        query: str,
        project_id: str,
        session_id: str | None = None,
        session_only: bool = False,
        datasets: list[str] | None = None,
        query_type: str | None = None,
        top_k: int = 15,
        only_context: bool = False,
    ) -> dict:
        start = time.monotonic()

        semantic_results = await self.semantic_search(
            db=db, query=query, project_id=project_id, top_k=top_k
        )

        graph_results: list[dict] = []
        if not session_only:
            graph_results = await self.graph_search(
                user_id=user_id,
                query=query,
                project_id=project_id,
                session_id=session_id,
                top_k=top_k,
            )

        combined = semantic_results + graph_results
        seen = set()
        unique: list[dict] = []
        for src in combined:
            mid = src.get("memory_id", "")
            if mid and mid not in seen:
                seen.add(mid)
                unique.append(src)

        ranked = self.ranker.rank(unique, query)

        elapsed = int((time.monotonic() - start) * 1000)
        logger.info(
            "Hybrid search complete",
            project_id=project_id,
            sources_count=len(ranked),
            elapsed_ms=elapsed,
        )

        return {
            "sources": [
                {
                    "text": r.text,
                    "source": r.source,
                    "memory_id": r.memory_id,
                    "chunk_id": r.chunk_id,
                    "relevance_score": r.relevance_score,
                    "evidence": r.evidence,
                    "explanation": r.explanation,
                }
                for r in ranked
            ],
            "processing_time_ms": elapsed,
        }


memory_retriever = MemoryRetriever()
