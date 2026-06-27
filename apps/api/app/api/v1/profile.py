from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUserRequired, DBDep
from app.models.user import User
from app.schemas.profile import (
    ProfileResponse,
    ProfileUpdate,
    SettingsResponse,
    SettingsUpdate,
)

router = APIRouter()


@router.get("", response_model=ProfileResponse)
async def get_profile(user_id: CurrentUserRequired, db: DBDep) -> ProfileResponse:
    user = await User.find_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return ProfileResponse(
        id=str(user.id),
        email=user.email,
        display_name=user.display_name,
        avatar_url=user.avatar_url,
        role=user.role,
        email_verified=user.email_verified,
        is_onboarded=user.is_onboarded,
        created_at=user.created_at.isoformat(),
        updated_at=user.updated_at.isoformat(),
    )


@router.patch("", response_model=ProfileResponse)
async def update_profile(
    user_id: CurrentUserRequired, db: DBDep, body: ProfileUpdate
) -> ProfileResponse:
    user = await User.find_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if body.display_name is not None:
        user.display_name = body.display_name
    if body.avatar_url is not None:
        user.avatar_url = body.avatar_url

    await db.commit()
    await db.refresh(user)

    return ProfileResponse(
        id=str(user.id),
        email=user.email,
        display_name=user.display_name,
        avatar_url=user.avatar_url,
        role=user.role,
        email_verified=user.email_verified,
        is_onboarded=user.is_onboarded,
        created_at=user.created_at.isoformat(),
        updated_at=user.updated_at.isoformat(),
    )


@router.post("/onboarded")
async def mark_onboarded(user_id: CurrentUserRequired, db: DBDep) -> dict:
    user = await User.find_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_onboarded = True
    await db.commit()

    return {"status": "ok", "message": "Onboarding completed"}


@router.get("/settings", response_model=SettingsResponse)
async def get_settings(_user_id: CurrentUserRequired) -> SettingsResponse:
    return SettingsResponse()


@router.patch("/settings", response_model=SettingsResponse)
async def update_settings(
    _user_id: CurrentUserRequired, _body: SettingsUpdate
) -> SettingsResponse:
    return SettingsResponse()
