from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.source_import import ImportJob
from app.services.cognee_adapter import cognee_adapter
from app.services.entity_enrichment import entity_enrichment_service
from app.services.knowledge import knowledge_service
from app.services.memory_evolution import memory_evolution_service
from app.services.memory_index import memory_index
from app.services.memory_timeline import memory_timeline
from app.services.memory_versioning import versioning_service
from app.services.source_parser import source_parser_service
from app.services.source_registry import source_registry_service


class ImportPipelineService:
    async def create_job(
        self,
        db: AsyncSession,
        project_id: str,
        user_id: str,
        source_type: str,
        data: str | None = None,
        url: str | None = None,
        display_name: str | None = None,
        metadata: dict | None = None,
    ) -> ImportJob:
        source = None
        if url or source_type in ("github", "url"):
            source = await source_registry_service.get_or_create_source(
                db=db, project_id=project_id, user_id=user_id,
                source_type=source_type, url=url,
                display_name=display_name or url,
            )
        job = ImportJob(
            project_id=project_id,
            user_id=user_id,
            source_id=source.id if source else None,
            source_type=source_type,
            status="queued",
            metadata_=metadata or {},
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)
        return job

    async def run_import(
        self,
        db: AsyncSession,
        job: ImportJob,
        data: str | bytes | None = None,
    ) -> ImportJob:
        await self._update_job(db, job, "running", 0, "Validating source")
        try:
            parsed = await self._parse_source(db, job, data)
            await self._update_job(db, job, "running", 15, f"Parsed {len(parsed)} items")

            validated = await self._validate(parsed)
            await self._update_job(db, job, "running", 20, f"Validated {len(validated)} items")

            await self._update_job(db, job, "running", 25, "Extracting metadata")
            enriched = await self._extract_metadata(db, job, validated)

            job.total_items = len(enriched)
            await db.commit()

            memory_ids = []
            for i, item in enumerate(enriched):
                progress = 25 + int((i / max(len(enriched), 1)) * 65)
                await self._update_job(
                    db, job, "running", progress,
                    f"Importing item {i + 1}/{len(enriched)}",
                )
                mid = await self._import_item(db, job, item, i)
                if mid:
                    memory_ids.append(mid)

            await self._update_job(db, job, "running", 95, "Running evolution")
            await memory_evolution_service.evolve(
                db=db,
                project_id=job.project_id,
                new_tags=[f"source:{job.source_type}"],
            )

            await memory_timeline.record_event(
                db=db,
                project_id=job.project_id,
                user_id=job.user_id,
                event_type="import.completed",
                data={
                    "job_id": job.id,
                    "source_type": job.source_type,
                    "memory_count": len(memory_ids),
                },
            )

            job.memory_ids = memory_ids
            job.processed_items = len(memory_ids)
            job.status = "completed"
            job.progress_pct = 100
            job.current_step = "Complete"
            await db.commit()
            await db.refresh(job)
            await source_registry_service.increment_memory_count(db, job.source_id)
            return job

        except Exception as e:
            job.status = "failed"
            job.error_message = str(e)
            await db.commit()
            await db.refresh(job)
            raise

    async def _parse_source(
        self, db: AsyncSession, job: ImportJob, data: str | bytes | None
    ) -> list[dict[str, Any]]:
        st = job.source_type
        if st == "url" and job.source_id:
            source = await source_registry_service.get_source(db, job.source_id)
            if source and source.url:
                import httpx
                async with httpx.AsyncClient() as client:
                    resp = await client.get(source.url, timeout=30, follow_redirects=True)
                    resp.raise_for_status()
                    content_type = resp.headers.get("content-type", "")
                    if "text/html" in content_type:
                        return await source_parser_service.parse_url_content(source.url, resp.text)
                    return await source_parser_service.parse(
                        "plain_text", resp.text, title=source.url,
                    )
        if st == "github" and job.source_id:
            source = await source_registry_service.get_source(db, job.source_id)
            if source and source.url:
                return await source_parser_service.parse_github(source.url)
        if st == "pdf" and data:
            return await source_parser_service.parse_pdf(
                data if isinstance(data, bytes) else data.encode("utf-8"),
                filename=job.metadata_.get("filename", "document.pdf")
                    if job.metadata_ else "document.pdf",
            )
        if data is not None:
            text_data = data.decode("utf-8") if isinstance(data, bytes) else data
            title = job.metadata_.get("title") if job.metadata_ else None
            return await source_parser_service.parse(st, text_data, title=title)
        raise ValueError(f"No data provided for source type: {st}")

    async def _validate(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        valid = []
        for item in items:
            content = item.get("content", "")
            if content and len(content.strip()) > 10:
                valid.append(item)
        return valid

    async def _extract_metadata(
        self, db: AsyncSession, job: ImportJob, items: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        enriched = []
        for item in items:
            content = item.get("content", "")
            tags = await knowledge_service.generate_tags(content, max_tags=5)
            item["tags"] = tags
            enriched.append(item)
        return enriched

    async def _import_item(
        self, db: AsyncSession, job: ImportJob, item: dict[str, Any], index: int
    ) -> str | None:
        try:
            memory_id = str(uuid.uuid4())
            content = item.get("content", "")
            title = item.get("title", f"{job.source_type}_{index}")
            memory_type = item.get("memory_type", "text")
            tags = item.get("tags", [])

            cognee_result = await cognee_adapter.remember(
                user_id=job.user_id,
                project_id=job.project_id,
                data=content,
                file_bytes=None,
                filename=None,
                mime_type=None,
                session_id=None,
                memory_type=memory_type,
            )
            from app.models.memory import Memory
            memory = Memory(
                id=memory_id,
                project_id=job.project_id,
                user_id=job.user_id,
                cognee_data_id=cognee_result.get("cognee_data_id"),
                cognee_dataset_id=cognee_adapter._dataset_name(job.project_id),
                title=title,
                memory_type=memory_type,
                source=job.source_type,
                content_preview=(content[:300] + "...")
                    if content and len(content) > 300 else content,
                token_count=cognee_result.get("token_count", 0),
                chunk_count=cognee_result.get("chunk_count", 0),
                status=cognee_result.get("status", "indexed"),
                importance=0.5,
                tags=tags or None,
                metadata_={"import_job_id": job.id, "source_id": job.source_id}
                    if job.source_id else {"import_job_id": job.id},
            )
            db.add(memory)
            await db.commit()
            await db.refresh(memory)

            await versioning_service.snapshot_current(db, memory, "imported")

            await memory_index.index_memory(db, memory, content=content)

            await entity_enrichment_service.enrich_memory(
                db=db, project_id=job.project_id,
                memory_id=memory_id, content=content, title=title,
            )

            return memory_id
        except Exception:
            return None

    async def _update_job(
        self, db: AsyncSession, job: ImportJob, status: str,
        progress_pct: int, current_step: str | None = None,
    ):
        job.status = status
        job.progress_pct = progress_pct
        if current_step:
            job.current_step = current_step
        await db.commit()


import_pipeline_service = ImportPipelineService()
