from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncGenerator

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from starlette.responses import StreamingResponse

from app.api.deps import CurrentUserRequired, DBDep
from app.models.source_import import ImportJob, Source
from app.schemas.source_import import (
    ImportJobListResponse,
    ImportJobResponse,
    ImportRequest,
    ImportResponse,
    SourceListResponse,
    SourceResponse,
)
from app.services.background_import import background_import_service
from app.services.import_pipeline import import_pipeline_service
from app.services.source_registry import source_registry_service

router = APIRouter()


def _source_to_response(s: Source) -> SourceResponse:
    return SourceResponse(
        id=s.id,
        project_id=s.project_id,
        source_type=s.source_type,
        display_name=s.display_name,
        url=s.url,
        file_path=s.file_path,
        mime_type=s.mime_type,
        size_bytes=s.size_bytes,
        metadata=s.metadata_,
        memory_count=s.memory_count or 0,
        last_import_at=s.last_import_at,
        created_at=s.created_at.isoformat() if s.created_at else "",
        updated_at=s.updated_at.isoformat() if s.updated_at else "",
    )


def _job_to_response(j: ImportJob) -> ImportJobResponse:
    return ImportJobResponse(
        id=j.id,
        project_id=j.project_id,
        source_id=j.source_id,
        source_type=j.source_type,
        status=j.status,
        progress_pct=j.progress_pct or 0,
        current_step=j.current_step,
        error_message=j.error_message,
        total_items=j.total_items or 0,
        processed_items=j.processed_items or 0,
        memory_ids=j.memory_ids,
        metadata=j.metadata_,
        created_at=j.created_at.isoformat() if j.created_at else "",
        updated_at=j.updated_at.isoformat() if j.updated_at else "",
    )


async def get_db():
    from app.database.session import get_session
    async for session in get_session():
        yield session


@router.post("/imports", response_model=ImportResponse)
async def create_import(
    db: DBDep,
    user: CurrentUserRequired,
    request: ImportRequest,
):
    job = await import_pipeline_service.create_job(
        db=db,
        project_id=request.project_id,
        user_id=user,
        source_type=request.source_type,
        data=request.data,
        url=request.url,
        display_name=request.display_name,
        metadata=request.metadata,
    )

    data_bytes = request.data.encode("utf-8") if request.data else None
    await background_import_service.start_import(get_db, job, data_bytes)

    return ImportResponse(
        job_id=job.id,
        source_id=job.source_id,
        status="queued",
        message=f"Import {request.source_type} queued",
    )


@router.post("/imports/upload")
async def upload_import(
    db: DBDep,
    user: CurrentUserRequired,
    file: UploadFile = File(...),
    project_id: str = Form(...),
    source_type: str | None = Form(None),
):
    file_bytes = await file.read()
    detected_type = source_type or _detect_source_type(
        file.filename or "file", file.content_type or "",
    )
    source = await source_registry_service.register(
        db=db,
        project_id=project_id,
        user_id=user,
        source_type=detected_type,
        display_name=file.filename,
        file_path=file.filename,
        mime_type=file.content_type,
        size_bytes=len(file_bytes),
    )
    job = await import_pipeline_service.create_job(
        db=db,
        project_id=project_id,
        user_id=user,
        source_type=detected_type,
        display_name=file.filename,
        metadata={"filename": file.filename, "source_id": source.id},
    )
    await background_import_service.start_import(get_db, job, file_bytes)
    return ImportResponse(
        job_id=job.id,
        source_id=source.id,
        status="queued",
        message=f"Upload {file.filename} queued as {detected_type}",
    )


@router.get("/imports", response_model=ImportJobListResponse)
async def list_imports(
    db: DBDep,
    user: CurrentUserRequired,
    project_id: str,
    limit: int = 50,
    offset: int = 0,
):
    jobs = await ImportJob.find_by_project(db, project_id, limit, offset)
    return ImportJobListResponse(
        jobs=[_job_to_response(j) for j in jobs],
        total=len(jobs),
    )


@router.get("/imports/{job_id}", response_model=ImportJobResponse)
async def get_import(db: DBDep, job_id: str):
    job = await ImportJob.find_by_id(db, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Import job not found")
    return _job_to_response(job)


@router.delete("/imports/{job_id}")
async def delete_import(db: DBDep, user: CurrentUserRequired, job_id: str):
    job = await ImportJob.find_by_id(db, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Import job not found")
    await background_import_service.cancel_import(job_id)
    await db.delete(job)
    await db.commit()
    return {"status": "deleted", "job_id": job_id}


@router.get("/sources", response_model=SourceListResponse)
async def list_sources(
    db: DBDep,
    user: CurrentUserRequired,
    project_id: str,
    limit: int = 50,
    offset: int = 0,
):
    sources = await source_registry_service.list_sources(db, project_id, limit, offset)
    return SourceListResponse(
        sources=[_source_to_response(s) for s in sources],
        total=len(sources),
    )


@router.get("/sources/{source_id}", response_model=SourceResponse)
async def get_source(db: DBDep, source_id: str):
    source = await source_registry_service.get_source(db, source_id)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return _source_to_response(source)


@router.get("/sources/{source_id}/memories")
async def get_source_memories(
    db: DBDep,
    source_id: str,
    limit: int = 50,
    offset: int = 0,
):
    source = await source_registry_service.get_source(db, source_id)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    from sqlalchemy import select

    from app.models.memory import Memory
    result = await db.execute(
        select(Memory)
        .where(Memory.project_id == source.project_id)
        .order_by(Memory.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    memories = list(result.scalars().all())
    from app.services.memory_serializer import memory_serializer
    return {
        "memories": [memory_serializer.memory_to_detail(m) for m in memories],
        "total": len(memories),
        "source_id": source_id,
    }


@router.get("/imports/{job_id}/stream")
async def stream_import_progress(
    db: DBDep,
    user: CurrentUserRequired,
    job_id: str,
):
    async def event_generator() -> AsyncGenerator[str, None]:
        last_status = ""
        last_pct = -1
        for _ in range(300):
            job = await ImportJob.find_by_id(db, job_id)
            if job is None:
                err_data = json.dumps({"event": "error", "data": {"message": "Job not found"}})
                yield f"data: {err_data}\n\n"
                break
            if job.status != last_status or job.progress_pct != last_pct:
                yield f"data: {json.dumps({
                    'event': 'progress',
                    'data': {
                        'job_id': job.id,
                        'status': job.status,
                        'progress_pct': job.progress_pct,
                        'current_step': job.current_step,
                        'total_items': job.total_items,
                        'processed_items': job.processed_items,
                    },
                })}\n\n"
                last_status = job.status
                last_pct = job.progress_pct
            if job.status in ("completed", "failed"):
                yield f"data: {json.dumps({'event': job.status, 'data': {'job_id': job.id}})}\n\n"
                break
            await asyncio.sleep(1)
        else:
            yield f"data: {json.dumps({'event': 'timeout', 'data': {}})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


def _detect_source_type(filename: str, content_type: str) -> str:
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    type_map = {
        "md": "markdown",
        "markdown": "markdown",
        "txt": "plain_text",
        "csv": "csv",
        "json": "json",
        "pdf": "pdf",
        "html": "url",
        "htm": "url",
    }
    if ext in type_map:
        return type_map[ext]
    if "markdown" in content_type:
        return "markdown"
    if "pdf" in content_type:
        return "pdf"
    if "csv" in content_type:
        return "csv"
    if "json" in content_type:
        return "json"
    if "text/plain" in content_type:
        return "plain_text"
    return "plain_text"
