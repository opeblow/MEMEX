from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entity import Entity, Relationship


class EntityStoreService:
    async def upsert_entity(
        self,
        db: AsyncSession,
        project_id: str,
        name: str,
        entity_type: str,
        description: str | None = None,
        metadata: dict | None = None,
    ) -> Entity:
        result = await db.execute(
            select(Entity).where(
                Entity.project_id == project_id,
                Entity.name == name,
                Entity.entity_type == entity_type,
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            if description:
                existing.description = description
            if metadata:
                existing.metadata_ = {**(existing.metadata_ or {}), **metadata}
            await db.commit()
            await db.refresh(existing)
            return existing
        entity = Entity(
            project_id=project_id,
            name=name,
            entity_type=entity_type,
            description=description,
            metadata_=metadata,
        )
        db.add(entity)
        await db.commit()
        await db.refresh(entity)
        return entity

    async def upsert_relationship(
        self,
        db: AsyncSession,
        project_id: str,
        source_entity_id: str,
        target_entity_id: str,
        relationship_type: str,
        strength: float = 0.5,
        metadata: dict | None = None,
    ) -> Relationship:
        result = await db.execute(
            select(Relationship).where(
                Relationship.project_id == project_id,
                Relationship.source_entity_id == source_entity_id,
                Relationship.target_entity_id == target_entity_id,
                Relationship.relationship_type == relationship_type,
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            existing.strength = min((existing.strength + strength) / 2, 1.0)
            if metadata:
                existing.metadata_ = {**(existing.metadata_ or {}), **metadata}
            await db.commit()
            await db.refresh(existing)
            return existing
        rel = Relationship(
            project_id=project_id,
            source_entity_id=source_entity_id,
            target_entity_id=target_entity_id,
            relationship_type=relationship_type,
            strength=strength,
            metadata_=metadata,
        )
        db.add(rel)
        await db.commit()
        await db.refresh(rel)
        return rel

    async def extract_and_store(
        self,
        db: AsyncSession,
        project_id: str,
        memory_id: str,
        content: str,
        entities: list[dict[str, Any]] | None = None,
    ) -> list[Entity]:
        from app.services.knowledge import knowledge_service
        extracted = entities or await knowledge_service.extract_entities(content)
        created = []
        for i, ent in enumerate(extracted):
            entity = await self.upsert_entity(
                db=db,
                project_id=project_id,
                name=ent.get("name", f"entity_{i}"),
                entity_type=ent.get("type", "unknown"),
                description=ent.get("description"),
                metadata={"memory_id": memory_id} if memory_id else None,
            )
            created.append(entity)
            for j in range(i):
                await self.upsert_relationship(
                    db=db,
                    project_id=project_id,
                    source_entity_id=entity.id,
                    target_entity_id=created[j].id,
                    relationship_type="co_occurs_with",
                    strength=0.3,
                    metadata={"memory_id": memory_id},
                )
        return created

    async def get_entities(
        self, db: AsyncSession, project_id: str, limit: int = 100, offset: int = 0
    ) -> list[Entity]:
        return await Entity.find_by_project(db, project_id, limit, offset)

    async def get_relationships(
        self, db: AsyncSession, project_id: str, limit: int = 200, offset: int = 0
    ) -> list[Relationship]:
        return await Relationship.find_by_project(db, project_id, limit, offset)


entity_store_service = EntityStoreService()
