from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.entity_store import entity_store_service


class EntityEnrichmentService:
    ENTITY_TYPES = [
        "person", "project", "repository", "organization",
        "technology", "framework", "api", "meeting", "topic",
    ]

    async def enrich_memory(
        self,
        db: AsyncSession,
        project_id: str,
        memory_id: str,
        content: str,
        title: str | None = None,
    ) -> list[dict[str, Any]]:
        from app.services.knowledge import knowledge_service
        entities = await knowledge_service.extract_entities(content)
        enriched = []
        for ent in entities:
            ent_type = ent.get("type", "topic").lower()
            if ent_type not in self.ENTITY_TYPES:
                ent_type = "topic"
            entity = await entity_store_service.upsert_entity(
                db=db,
                project_id=project_id,
                name=ent.get("name", "unknown"),
                entity_type=ent_type,
                description=ent.get("description"),
                metadata={"memory_id": memory_id},
            )
            enriched.append(entity)
        for i in range(len(enriched)):
            for j in range(i + 1, len(enriched)):
                await entity_store_service.upsert_relationship(
                    db=db,
                    project_id=project_id,
                    source_entity_id=enriched[i].id,
                    target_entity_id=enriched[j].id,
                    relationship_type="co_occurs_with",
                    strength=0.3,
                    metadata={"memory_id": memory_id},
                )
        return [{"id": e.id, "name": e.name, "type": e.entity_type} for e in enriched]

    def classify_entity_type(self, name: str, context: str = "") -> str:
        lower = name.lower()
        if any(t in lower for t in ["corp", "inc", "ltd", "llc", "organization", "company"]):
            return "organization"
        if any(t in lower for t in ["repo", "repository"]):
            return "repository"
        if any(t in lower for t in ["api", "sdk", "library", "framework"]):
            return "api" if "api" in lower else "framework"
        if any(t in lower for t in ["meeting", "sync", "standup", "retro"]):
            return "meeting"
        if any(t in lower for t in ["project", "initiative"]):
            return "project"
        return "topic"


entity_enrichment_service = EntityEnrichmentService()
