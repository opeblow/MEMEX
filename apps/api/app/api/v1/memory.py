from __future__ import annotations

from fastapi import APIRouter, File, Form, UploadFile

from app.api.deps import CurrentUserRequired
from app.schemas.memory import (
    ForgetRequest,
    ForgetResponse,
    ImproveRequest,
    ImproveResponse,
    RecallRequest,
    RecallResponse,
    RememberResponse,
)
from app.services.memory import MemoryService
from app.services.search import SearchService

router = APIRouter()


@router.post("/remember", response_model=RememberResponse)
async def remember(
    user_id: CurrentUserRequired,
    project_id: str = Form(...),
    data: str | None = Form(None),
    file: UploadFile | None = File(None),
    session_id: str | None = Form(None),
    memory_type: str | None = Form(None),
    title: str | None = Form(None),
    tags: str | None = Form(None),
    run_in_background: bool = Form(False),
) -> RememberResponse:
    service = MemoryService()
    result = await service.remember(
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
    return result


@router.post("/recall")
async def recall(
    user_id: CurrentUserRequired,
    body: RecallRequest,
) -> RecallResponse:
    service = SearchService()
    result = await service.recall(
        user_id=user_id,
        query=body.query,
        project_id=body.project_id,
        session_id=body.session_id,
        datasets=body.datasets,
        query_type=body.query_type,
        top_k=body.top_k or 15,
        only_context=body.only_context or False,
        stream=body.stream or False,
    )
    return result


@router.post("/improve", response_model=ImproveResponse)
async def improve(
    user_id: CurrentUserRequired,
    body: ImproveRequest,
) -> ImproveResponse:
    service = MemoryService()
    result = await service.improve(
        user_id=user_id,
        project_id=body.project_id,
        session_ids=body.session_ids,
        build_global_context_index=body.build_global_context_index or False,
        run_in_background=body.run_in_background or False,
    )
    return result


@router.post("/forget", response_model=ForgetResponse)
async def forget(
    user_id: CurrentUserRequired,
    body: ForgetRequest,
) -> ForgetResponse:
    service = MemoryService()
    result = await service.forget(
        user_id=user_id,
        project_id=body.project_id,
        data_id=body.data_id,
        dataset=body.dataset,
        everything=body.everything or False,
        memory_only=body.memory_only or False,
    )
    return result
