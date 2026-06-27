from __future__ import annotations

from pydantic import BaseModel


class ProfileResponse(BaseModel):
    id: str
    email: str
    display_name: str
    avatar_url: str | None = None
    role: str
    email_verified: bool
    is_onboarded: bool
    created_at: str
    updated_at: str


class ProfileUpdate(BaseModel):
    display_name: str | None = None
    avatar_url: str | None = None


class SettingsResponse(BaseModel):
    theme: str = "dark"
    language: str = "en"
    notifications_enabled: bool = True
    email_digest: bool = False


class SettingsUpdate(BaseModel):
    theme: str | None = None
    language: str | None = None
    notifications_enabled: bool | None = None
    email_digest: bool | None = None
