from __future__ import annotations

from fastapi import APIRouter, File, Form, UploadFile

from app.api.deps import CurrentUserRequired, DBDep
from app.schemas.memory import (
    ForgetRequest,
    ForgetResponse,
    ImproveRequest,
    ImproveResponse,
    MemoryDetailResponse,
    MemoryUpdateRequest,
    RecallRequest,
    RecallResponse,
    RememberResponse,
    SearchRequest,
    SearchResponse,
)
from app.services.memory_engine import memory_engine
from app.services.memory_lifecycle import memory_lifecycle

router = APIRouter()


@router.post("/remember", response_model=RememberResponse)
async def remember(
    user_id: CurrentUserRequired,
    db: DBDep,
    project_id: str = Form(...),
    data: str | None = Form(None),
    file: UploadFile | None = File(None),
    session_id: str | None = Form(None),
    memory_type: str | None = Form(None),
    title: str | None = Form(None),
    tags: str | None = Form(None),
    run_in_background: bool = Form(False),
) -> RememberResponse:
    return await memory_engine.remember(
        db=db,
        user_id=user_id,
        project_id=project_id,
        data=data,
        file=file,
        session_id=session_id,
        memory_type=memory_type,
        title=title,
        tags=tags,
        run_in_background=run_in_background,
    )


@router.post("/recall", response_model=RecallResponse)
async def recall(
    user_id: CurrentUserRequired,
    db: DBDep,
    body: RecallRequest,
) -> RecallResponse:
    return await memory_engine.recall(
        db=db,
        user_id=user_id,
        query=body.query,
        project_id=body.project_id,
        session_id=body.session_id,
        session_only=body.session_only,
        datasets=body.datasets,
        query_type=body.query_type,
        top_k=body.top_k or 15,
        only_context=body.only_context or False,
        stream=body.stream or False,
    )


@router.post("/improve", response_model=ImproveResponse)
async def improve(
    user_id: CurrentUserRequired,
    db: DBDep,
    body: ImproveRequest,
) -> ImproveResponse:
    return await memory_engine.improve(
        db=db,
        user_id=user_id,
        project_id=body.project_id,
        session_ids=body.session_ids,
        build_global_context_index=body.build_global_context_index or False,
        run_in_background=body.run_in_background or False,
    )


@router.post("/forget", response_model=ForgetResponse)
async def forget(
    user_id: CurrentUserRequired,
    db: DBDep,
    body: ForgetRequest,
) -> ForgetResponse:
    return await memory_engine.forget(
        db=db,
        user_id=user_id,
        project_id=body.project_id,
        data_id=body.data_id,
        dataset=body.dataset,
        everything=body.everything or False,
        memory_only=body.memory_only or False,
    )


@router.get("/memory/{memory_id}", response_model=MemoryDetailResponse)
async def get_memory(
    user_id: CurrentUserRequired,
    db: DBDep,
    memory_id: str,
) -> MemoryDetailResponse | None:
    return await memory_engine.get_memory(db, memory_id)


@router.get("/memory", response_model=list[MemoryDetailResponse])
async def list_memories(
    user_id: CurrentUserRequired,
    db: DBDep,
    project_id: str,
    limit: int = 50,
    offset: int = 0,
) -> list[MemoryDetailResponse]:
    return await memory_engine.list_memories(db, project_id, limit, offset)


@router.patch("/memory/{memory_id}", response_model=MemoryDetailResponse)
async def update_memory(
    user_id: CurrentUserRequired,
    db: DBDep,
    memory_id: str,
    body: MemoryUpdateRequest,
) -> MemoryDetailResponse | None:
    from sqlalchemy import update as sa_update

    from app.models.memory import Memory

    values = body.model_dump(exclude_unset=True)
    if not values:
        return await memory_engine.get_memory(db, memory_id)

    await db.execute(
        sa_update(Memory)
        .where(Memory.id == memory_id, Memory.user_id == user_id)
        .values(**values)
    )
    await db.commit()
    return await memory_engine.get_memory(db, memory_id)


@router.post("/memory/search", response_model=SearchResponse)
async def search_memories(
    user_id: CurrentUserRequired,
    db: DBDep,
    body: SearchRequest,
) -> SearchResponse:
    import time
    start = time.monotonic()
    results = await memory_engine.search_memories(
        db=db,
        user_id=user_id,
        project_id=body.project_id,
        query=body.query,
        limit=body.limit,
    )
    elapsed = int((time.monotonic() - start) * 1000)
    return SearchResponse(
        results=results,
        total=len(results),
        processing_time_ms=elapsed,
    )


@router.delete("/memory/{memory_id}")
async def delete_memory(
    user_id: CurrentUserRequired,
    db: DBDep,
    memory_id: str,
    permanent: bool = False,
) -> dict:
    if permanent:
        success = await memory_lifecycle.hard_delete(db, memory_id, user_id)
    else:
        success = await memory_lifecycle.soft_delete(db, memory_id, user_id)
    return {
        "status": "ok" if success else "not_found",
        "deleted": success,
    }


@router.post("/memory/{memory_id}/archive")
async def archive_memory(
    user_id: CurrentUserRequired,
    db: DBDep,
    memory_id: str,
) -> dict:
    success = await memory_lifecycle.archive(db, memory_id, user_id)
    return {"status": "ok" if success else "not_found"}


@router.post("/memory/{memory_id}/restore")
async def restore_memory(
    user_id: CurrentUserRequired,
    db: DBDep,
    memory_id: str,
) -> dict:
    success = await memory_lifecycle.restore(db, memory_id, user_id)
    return {"status": "ok" if success else "not_found"}
