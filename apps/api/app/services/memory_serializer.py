from __future__ import annotations

from app.models.memory import Memory
from app.schemas.memory import (
    MemoryDetailResponse,
    MemoryListItem,
    RecallSource,
)


class MemorySerializer:
    @staticmethod
    def memory_to_detail(memory: Memory) -> MemoryDetailResponse:
        return MemoryDetailResponse(
            id=memory.id,
            project_id=memory.project_id,
            user_id=memory.user_id,
            session_id=memory.session_id,
            title=memory.title or "",
            memory_type=memory.memory_type,
            status=memory.status,
            source=memory.source,
            source_url=memory.source_url,
            file_path=memory.file_path,
            mime_type=memory.mime_type,
            content_preview=memory.content_preview,
            size_bytes=memory.size_bytes,
            token_count=memory.token_count,
            chunk_count=memory.chunk_count,
            importance=memory.importance,
            tags=memory.tags or [],
            metadata=memory.metadata_ or {},
            created_at=memory.created_at.isoformat() if memory.created_at else "",
            updated_at=memory.updated_at.isoformat() if memory.updated_at else "",
        )

    @staticmethod
    def memory_to_list_item(memory: Memory) -> MemoryListItem:
        return MemoryListItem(
            id=memory.id,
            title=memory.title or "",
            memory_type=memory.memory_type,
            status=memory.status,
            importance=memory.importance,
            tags=memory.tags or [],
            content_preview=memory.content_preview,
            created_at=memory.created_at.isoformat() if memory.created_at else "",
            updated_at=memory.updated_at.isoformat() if memory.updated_at else "",
        )

    @staticmethod
    def recall_source_from_cognee(source: dict) -> RecallSource:
        return RecallSource(
            text=source.get("text", ""),
            source=source.get("source", "graph"),
            memory_id=source.get("memory_id", ""),
            chunk_id=source.get("chunk_id"),
            relevance_score=source.get("relevance_score", 0.0),
            evidence=source.get("evidence"),
        )

    @staticmethod
    def content_preview(text: str | None, max_length: int = 300) -> str:
        if not text:
            return ""
        return text[:max_length] + ("..." if len(text) > max_length else "")


memory_serializer = MemorySerializer()
