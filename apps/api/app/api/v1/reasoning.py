from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncGenerator

from fastapi import APIRouter, HTTPException
from starlette.responses import StreamingResponse

from app.api.deps import CurrentUserRequired, DBDep
from app.schemas.reasoning import ReasoningRequest, ReasoningResponse
from app.schemas.trail import MemoryEvidenceResponse, MemoryTrailResponse
from app.services.memory_trail import trail_service
from app.services.reasoning_engine import reasoning_engine

router = APIRouter()


@router.post("/reason", response_model=ReasoningResponse)
async def reason(
    db: DBDep,
    user: CurrentUserRequired,
    request: ReasoningRequest,
):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query is required")
    result = await reasoning_engine.reason(db=db, user_id=user, request=request)
    return result


@router.post("/reason/stream")
async def reason_stream(
    db: DBDep,
    user: CurrentUserRequired,
    request: ReasoningRequest,
):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query is required")

    def _sse(event: str, data: dict) -> str:
        return f"data: {json.dumps({'event': event, 'data': data})}\n\n"

    async def event_generator() -> AsyncGenerator[str, None]:
        yield _sse("start", {"query": request.query})

        yield _sse("step", {"step": 1, "name": "intent_detection", "status": "running"})
        await asyncio.sleep(0.1)
        yield _sse("step", {"step": 1, "name": "intent_detection", "status": "complete"})

        yield _sse("step", {"step": 2, "name": "memory_retrieval", "status": "running"})
        from app.services.memory_retriever import memory_retriever
        results = await memory_retriever.multi_strategy_search(
            db=db, user_id=user, query=request.query,
            project_id=request.project_id, top_k=request.top_k,
        )
        memory_ids = [r.get("memory_id", "") for r in results if r.get("memory_id")]
        yield _sse("step", {
            "step": 2, "name": "memory_retrieval",
            "status": "complete", "memory_ids": memory_ids,
        })

        yield _sse("step", {"step": 8, "name": "generating_answer", "status": "running"})
        full_response = await reasoning_engine.reason(db=db, user_id=user, request=request)

        for word in full_response.answer.split(" "):
            yield f"data: {json.dumps({'event': 'token', 'content': word + ' '})}\n\n"
            await asyncio.sleep(0.02)

        yield _sse("complete", {
            "answer": full_response.answer,
            "trail_id": full_response.trail_id,
            "explanation": full_response.explanation.model_dump()
                if full_response.explanation else None,
            "processing_time_ms": full_response.processing_time_ms,
        })

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/memory/trail/{trail_id}", response_model=MemoryTrailResponse)
async def get_trail(db: DBDep, trail_id: str):
    trail = await trail_service.get_trail(db=db, trail_id=trail_id)
    if trail is None:
        raise HTTPException(status_code=404, detail="Trail not found")
    return trail


@router.get("/memory/evidence/{memory_id}", response_model=MemoryEvidenceResponse)
async def get_evidence(db: DBDep, memory_id: str):
    from app.models.memory import Memory
    from app.services.entity_store import entity_store_service
    memory = await db.get(Memory, memory_id)
    if memory is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    relationships = []
    timeline_events = []
    try:
        entities = await entity_store_service.get_entities(db, memory.project_id)
        for ent in entities[:20]:
            rels = await entity_store_service.get_relationships(db, memory.project_id)
            for r in rels[:5]:
                relationships.append({
                    "from": r.source_entity_id,
                    "to": r.target_entity_id,
                    "type": r.relationship_type,
                    "strength": r.strength,
                })
    except Exception:
        pass
    result = await trail_service.get_evidence(
        db=db, memory_id=memory_id,
        relationships=relationships, timeline_events=timeline_events,
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return result
