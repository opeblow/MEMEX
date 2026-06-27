from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter

from app.api.deps import CurrentUserRequired, DBDep
from app.schemas.memory import TimelineQueryRequest, TimelineResponse
from app.services.memory_timeline import memory_timeline

router = APIRouter()


@router.post("/timeline", response_model=TimelineResponse)
async def get_timeline(
    user_id: CurrentUserRequired,
    db: DBDep,
    body: TimelineQueryRequest,
) -> TimelineResponse:
    from_date = None
    to_date = None
    if body.from_date:
        try:
            from_date = datetime.fromisoformat(body.from_date)
        except ValueError:
            pass
    if body.to_date:
        try:
            to_date = datetime.fromisoformat(body.to_date)
        except ValueError:
            pass

    events = await memory_timeline.get_events(
        db=db,
        project_id=body.project_id,
        from_date=from_date,
        to_date=to_date,
        event_types=body.event_types,
        limit=body.limit,
        offset=body.offset,
    )

    summary = await memory_timeline.get_timeline_summary(
        db=db,
        project_id=body.project_id,
    )

    return TimelineResponse(
        events=events,
        total=len(events),
        summary=summary,
    )


@router.get("/timeline/summary/{project_id}")
async def get_timeline_summary(
    user_id: CurrentUserRequired,
    db: DBDep,
    project_id: str,
) -> dict:
    return await memory_timeline.get_timeline_summary(db, project_id)
