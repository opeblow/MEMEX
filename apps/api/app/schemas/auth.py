from __future__ import annotations

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    display_name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class GoogleAuthRequest(BaseModel):
    token: str


class VerifyEmailRequest(BaseModel):
    token: str


class RequestResetRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    display_name: str
    avatar_url: str | None = None
    role: str = "user"
    email_verified: bool = False


class AuthResponse(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: str
