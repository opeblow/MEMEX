from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entity import Entity, Relationship
from app.models.memory import Memory
from app.models.memory_event import MemoryEvent


class SeedService:
    async def load_demo_data(self, db: AsyncSession, user_id: str) -> dict:
        from app.models.organization import Organization
        from app.models.organization_member import OrganizationMember
        from app.models.project import Project

        org = await Organization.create(
            db=db, name="Demo Mindscape", slug="demo-mindscape",
            description="A demo workspace showcasing MEMEX memory capabilities",
            owner_id=user_id,
        )
        await OrganizationMember.add_member(
            db=db, organization_id=org.id, user_id=user_id, role="admin",
        )

        project = await Project.create(
            db=db, workspace_id=org.id, name="Demo Project",
            slug="demo-project",
            description="Example memories across topics and time",
            owner_id=user_id,
        )

        project_id = project.id
        now = datetime.now(UTC)

        previews = {
            "quantum": (
                "Explored fundamentals of quantum computing including superposition,"
                " entanglement, and quantum gates. Qubits differ from classical bits"
                " by existing in multiple states simultaneously."
            ),
            "roadmap": (
                "Quarterly roadmap planning session. Key decisions: prioritize"
                " performance optimization in April, launch new dashboard in May,"
                " begin ML integration research in June."
            ),
            "brainstorm": (
                "Had an idea for a memory visualization feature that uses constellation"
                " patterns to show relationships between concepts. Could make abstract"
                " connections more intuitive."
            ),
            "transformers": (
                "Deep dive into transformer neural networks. Self-attention mechanism"
                " allows model to weigh importance of different parts of input."
                " Multi-head attention runs multiple attention operations in parallel."
            ),
            "bugfix": (
                "Fixed O(n) search bottleneck by adding database indexes on memory type"
                " and timestamp columns. Query time reduced from 2.3s to 45ms."
                " PR merged after code review."
            ),
            "design_review": (
                "Reviewed the 3D memory universe prototype. Feedback: reduce node"
                " overlap, add type-based color coding, improve label readability."
                " Motion designer will refine animations."
            ),
            "article": (
                "Saved an article about persistent memory in AI systems. Key insight:"
                " long-term memory is the missing piece in current LLM architectures."
                " Vector databases + knowledge graphs = promising direction."
            ),
            "interview": (
                "Interviewed Sarah for senior backend role. Strong system design skills,"
                " built similar memory systems before. Good culture fit."
                " Recommend moving to onsite round."
            ),
            "reflection": (
                "Chose Event Sourcing over CRUD for memory operations. Benefits: full"
                " audit trail, time travel queries, better collaboration support."
                " Downside: more complex initial setup but pays off long-term."
            ),
            "experiment": (
                "Prototyped graph traversal for memory recall. Walking relationship"
                " edges finds connected memories 40% faster than vector search alone."
                " Hybrid approach gives best results."
            ),
            "reading": (
                "Books to explore: 'The Knowledge Graph' by Tommaso, 'Designing"
                " Data-Intensive Applications' by Kleppmann, 'Building LLM Apps'"
                " by O'Reilly. Focus on memory and retrieval."
            ),
            "retro": (
                "Sprint 12 retro: Team morale is good. Velocity stable at 28 points."
                " Areas to improve: code review turnaround time, clearer acceptance"
                " criteria. Action items assigned."
            ),
            "rust": (
                "Started learning Rust for systems programming. Ownership model is"
                " challenging but powerful. Built a simple CLI tool for file"
                " organization as practice project."
            ),
            "pipeline": (
                "Designed the new ingestion pipeline architecture. Source connectors"
                " -> Parser Registry -> Enrichment Layer -> Vector Store + Graph DB."
                " Supports pluggable parsers."
            ),
        }

        memories_data = [
            # (title, type, preview, importance, tags, days_ago)
            ("Quantum Computing Overview", "research",
             previews["quantum"], 0.9, ["quantum", "computing", "research"], 14),
            ("Meeting Notes: Product Roadmap Q2", "meeting",
             previews["roadmap"], 0.85, ["meeting", "product", "roadmap"], 12),
            ("Coffee Shop Brainstorming", "idea",
             previews["brainstorm"], 0.7, ["idea", "visualization", "ux"], 11),
            ("Understanding Transformer Architectures", "research",
             previews["transformers"], 0.88, ["ai", "deep-learning", "research"], 10),
            ("Bug Fix: Memory Search Performance", "code",
             previews["bugfix"], 0.75, ["code", "performance", "bugfix"], 9),
            ("Design Review: Memory Universe 3D", "design",
             previews["design_review"], 0.78, ["design", "3d", "ux"], 8),
            ("Article: The Future of AI Memory", "text",
             previews["article"], 0.82, ["ai", "article", "knowledge"], 7),
            ("Interview Notes: Senior Engineer Candidate", "meeting",
             previews["interview"], 0.6, ["recruiting", "meeting"], 6),
            ("Reflection: Project Architecture Decision", "reflection",
             previews["reflection"], 0.83, ["architecture", "decision"], 5),
            ("Experiment: Graph-Based Memory Retrieval", "research",
             previews["experiment"], 0.87, ["research", "graph", "experiment"], 4),
            ("Reading List: Knowledge Management", "text",
             previews["reading"], 0.55, ["reading", "books", "knowledge"], 3),
            ("Sprint Retrospective Notes", "meeting",
             previews["retro"], 0.72, ["sprint", "retro", "team"], 2),
            ("Personal Note: Learning Rust", "reflection",
             previews["rust"], 0.45, ["learning", "rust", "personal"], 1),
            ("Architecture Diagram: Data Pipeline v2", "design",
             previews["pipeline"], 0.8, ["architecture", "design", "pipeline"], 0),
        ]

        memories = []
        for title, mem_type, preview, importance, tags, days_ago in memories_data:
            created = now - timedelta(days=days_ago, hours=hash(title) % 12)
            memory = Memory(
                id=str(uuid4()),
                project_id=project_id,
                user_id=user_id,
                title=title,
                memory_type=mem_type,
                content_preview=preview,
                importance=importance,
                tags=tags,
                status="active",
                source="manual",
                metadata_={"demo": True, "original_day": days_ago},
                created_at=created,
                updated_at=created,
            )
            db.add(memory)
            memories.append(memory)

            # Memory events showing evolution
            if days_ago > 0 and days_ago % 3 == 0:
                event = MemoryEvent(
                    id=str(uuid4()),
                    project_id=project_id,
                    user_id=user_id,
                    event_type="memory.created",
                    event_data={"memory_id": memory.id, "title": title},
                    created_at=created,
                )
                db.add(event)

        db.add(MemoryEvent(
            id=str(uuid4()), project_id=project_id, user_id=user_id,
            event_type="memory.improved",
            event_data={"memory_id": memories[0].id, "importance_boost": 0.1},
            created_at=now - timedelta(hours=6),
        ))
        db.add(MemoryEvent(
            id=str(uuid4()), project_id=project_id, user_id=user_id,
            event_type="memory.recalled",
            event_data={"memory_id": memories[2].id},
            created_at=now - timedelta(hours=2),
        ))
        db.add(MemoryEvent(
            id=str(uuid4()), project_id=project_id, user_id=user_id,
            event_type="session.start",
            event_data={"label": "Demo exploration session"},
            created_at=now - timedelta(minutes=30),
        ))

        # Entities
        entities_data = [
            ("Quantum Computing", "concept", "Computing paradigm using quantum mechanics"),
            ("Transformer Architecture", "concept",
             "Neural network architecture for sequence data"),
            ("Knowledge Graphs", "concept",
             "Graph-structured knowledge representation"),
            ("Vector Databases", "concept",
             "Databases optimized for vector similarity search"),
            ("Product Roadmap", "project", "Q2 product development roadmap"),
            ("Memory Universe", "feature", "3D visualization of memory relationships"),
            ("Data Pipeline v2", "project", "Next-gen ingestion and processing pipeline"),
            ("Rust Programming", "skill", "Systems programming language"),
            ("Event Sourcing", "pattern",
             "Architectural pattern for state change tracking"),
            ("Sarah Chen", "person", "Senior backend engineer candidate"),
        ]

        entities = []
        for name, entity_type, description in entities_data:
            entity = Entity(
                id=str(uuid4()), project_id=project_id, name=name,
                entity_type=entity_type, description=description,
            )
            db.add(entity)
            entities.append(entity)

        # Relationships
        relationships_data = [
            (entities[0].id, entities[2].id, "related_to", 0.6),
            (entities[1].id, entities[3].id, "related_to", 0.7),
            (entities[2].id, entities[3].id, "complements", 0.8),
            (entities[4].id, entities[5].id, "includes", 0.5),
            (entities[4].id, entities[6].id, "includes", 0.6),
            (entities[5].id, entities[6].id, "related_to", 0.4),
            (entities[7].id, entities[8].id, "studied_with", 0.3),
            (entities[0].id, entities[1].id, "related_to", 0.4),
            (entities[2].id, entities[9].id, "area_of_expertise", 0.7),
        ]

        for src, tgt, rel_type, strength in relationships_data:
            rel = Relationship(
                id=str(uuid4()), project_id=project_id,
                source_entity_id=src, target_entity_id=tgt,
                relationship_type=rel_type, strength=strength,
            )
            db.add(rel)

        await db.commit()

        # Refresh to get valid data back
        for m in memories:
            await db.refresh(m)
        for e in entities:
            await db.refresh(e)

        return {
            "workspace_id": org.id,
            "project_id": project_id,
            "memories_created": len(memories),
            "entities_created": len(entities),
            "relationships_created": len(relationships_data),
        }


seed_service = SeedService()
