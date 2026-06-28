from __future__ import annotations

import json
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.collaboration import MemoryCollectionItem
from app.models.memory import Memory


class ExportService:
    async def export_collection(
        self, db: AsyncSession, collection_id: str, format: str = "json"
    ) -> str | bytes:
        items = await MemoryCollectionItem.find_by_collection(db, collection_id)
        memory_ids = [item.memory_id for item in items]
        if not memory_ids:
            return "[]" if format == "json" else ""

        result = await db.execute(
            select(Memory).where(Memory.id.in_(memory_ids))
        )
        memories = list(result.scalars().all())

        if format == "json":
            return json.dumps(
                [
                    {
                        "id": m.id,
                        "title": m.title,
                        "content_preview": m.content_preview,
                        "memory_type": m.memory_type,
                        "source": m.source,
                        "tags": m.tags,
                        "importance": m.importance,
                        "created_at": m.created_at.isoformat() if m.created_at else "",
                        "metadata": m.metadata_,
                    }
                    for m in memories
                ],
                indent=2,
                default=str,
            )

        if format == "markdown":
            now_str = datetime.now(UTC).isoformat()
            lines = ["# Memory Collection Export\n", f"*Exported {now_str}*\n"]
            for m in memories:
                lines.append(f"## {m.title or 'Untitled'}")
                lines.append(f"- **Type:** {m.memory_type}")
                lines.append(f"- **Importance:** {m.importance}")
                if m.tags:
                    lines.append(f"- **Tags:** {', '.join(m.tags)}")
                if m.content_preview:
                    lines.append(f"\n{m.content_preview}\n")
                lines.append("---\n")
            return "\n".join(lines)

        if format == "csv":
            import csv as csv_lib
            import io

            output = io.StringIO()
            writer = csv_lib.writer(output)
            cols = ["id", "title", "type", "source", "tags", "importance", "created_at", "preview"]
            writer.writerow(cols)
            for m in memories:
                writer.writerow([
                    m.id,
                    m.title or "",
                    m.memory_type,
                    m.source or "",
                    ",".join(m.tags) if m.tags else "",
                    m.importance,
                    m.created_at.isoformat() if m.created_at else "",
                    (m.content_preview or "")[:200],
                ])
            return output.getvalue()

        return "[]"

    async def export_project_memories(
        self, db: AsyncSession, project_id: str, format: str = "json"
    ) -> str | bytes:
        result = await db.execute(
            select(Memory)
            .where(Memory.project_id == project_id)
            .order_by(Memory.created_at.desc())
        )
        memories = list(result.scalars().all())

        if format == "json":
            return json.dumps(
                [
                    {
                        "id": m.id,
                        "title": m.title,
                        "content_preview": m.content_preview,
                        "memory_type": m.memory_type,
                        "source": m.source,
                        "tags": m.tags,
                        "importance": m.importance,
                        "created_at": m.created_at.isoformat() if m.created_at else "",
                        "metadata": m.metadata_,
                    }
                    for m in memories
                ],
                indent=2,
                default=str,
            )

        if format == "markdown":
            now_str = datetime.now(UTC).isoformat()
            lines = ["# Project Memory Export\n", f"*Exported {now_str}*\n"]
            for m in memories:
                lines.append(f"## {m.title or 'Untitled'}")
                lines.append(f"- **Type:** {m.memory_type}")
                lines.append(f"- **Importance:** {m.importance}")
                if m.tags:
                    lines.append(f"- **Tags:** {', '.join(m.tags)}")
                if m.content_preview:
                    lines.append(f"\n{m.content_preview}\n")
                lines.append("---\n")
            return "\n".join(lines)

        return "[]"


export_service = ExportService()
