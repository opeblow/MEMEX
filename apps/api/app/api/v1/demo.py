from __future__ import annotations

from fastapi import APIRouter

from app.api.deps import CurrentUserRequired, DBDep
from app.services.seed_data import seed_service

router = APIRouter(tags=["demo"])


@router.post("/demo/load")
async def load_demo_data(
    user_id: CurrentUserRequired,
    db: DBDep,
):
    result = await seed_service.load_demo_data(db, user_id)
    return {"status": "ok", "data": result}
