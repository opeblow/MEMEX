from __future__ import annotations

import secrets
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.api.deps import CurrentUserRequired, DBDep
from app.config import settings
from app.models.user import User
from app.models.verification_token import VerificationToken
from app.schemas.auth import (
    AuthResponse,
    GoogleAuthRequest,
    LoginRequest,
    RegisterRequest,
    RequestResetRequest,
    ResetPasswordRequest,
    TokenRefreshRequest,
    UserResponse,
    VerifyEmailRequest,
)
from app.services.email import email_service

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(user_id: str) -> str:
    expire = datetime.now(UTC) + timedelta(
        minutes=settings.jwt_access_expire_minutes
    )
    return jwt.encode(
        {"sub": user_id, "exp": expire, "type": "access"},
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def create_refresh_token(user_id: str) -> str:
    expire = datetime.now(UTC) + timedelta(
        days=settings.jwt_refresh_expire_days
    )
    return jwt.encode(
        {"sub": user_id, "exp": expire, "type": "refresh"},
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def _user_to_response(user: User) -> UserResponse:
    return UserResponse(
        id=str(user.id),
        email=user.email,
        display_name=user.display_name,
        avatar_url=user.avatar_url,
        role=user.role,
        email_verified=user.email_verified,
    )


def _auth_response(user: User) -> AuthResponse:
    return AuthResponse(
        user=_user_to_response(user),
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )


@router.post("/register", response_model=AuthResponse)
async def register(body: RegisterRequest, db: DBDep) -> AuthResponse:
    existing = await User.find_by_email(db, body.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = await User.create(
        db,
        email=body.email,
        hashed_password=pwd_context.hash(body.password),
        display_name=body.display_name,
    )

    token = secrets.token_urlsafe(32)
    await VerificationToken.create(
        db,
        user_id=str(user.id),
        token=token,
        token_type="email_verification",
    )
    await email_service.send_verification_email(body.email, body.display_name, token)

    user.last_login_at = datetime.now(UTC)
    await db.commit()

    return _auth_response(user)


@router.post("/login", response_model=AuthResponse)
async def login(body: LoginRequest, db: DBDep) -> AuthResponse:
    user = await User.find_by_email(db, body.email)
    if not user or not user.hashed_password or not pwd_context.verify(
        body.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    user.last_login_at = datetime.now(UTC)
    await db.commit()

    return _auth_response(user)


@router.post("/google", response_model=AuthResponse)
async def google_auth(body: GoogleAuthRequest, db: DBDep) -> AuthResponse:
    if not settings.google_client_id:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Google OAuth not configured",
        )

    try:

        payload = jwt.decode(
            body.token,
            settings.google_client_secret or "",
            algorithms=["RS256"],
            options={"verify_aud": False},
        )
    except JWTError:
        try:
            import httpx

            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    "https://www.googleapis.com/oauth2/v3/tokeninfo",
                    params={"id_token": body.token},
                )
                if resp.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid Google token",
                    )
                payload = resp.json()
        except httpx.HTTPError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google token",
            )

    email = payload.get("email")
    google_id = payload.get("sub")
    name = payload.get("name", email or "User")
    avatar = payload.get("picture")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google account has no email",
        )

    user = await User.find_by_email(db, email)
    if not user:
        user = await User.create_google_user(
            db,
            email=email,
            display_name=name,
            google_id=google_id,
            avatar_url=avatar,
        )
    else:
        user.last_login_at = datetime.now(UTC)
        if avatar and not user.avatar_url:
            user.avatar_url = avatar
        await db.commit()

    return _auth_response(user)


@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(body: TokenRefreshRequest, db: DBDep) -> AuthResponse:
    try:
        payload = jwt.decode(
            body.refresh_token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        user = await User.find_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return _auth_response(user)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )


@router.get("/me", response_model=UserResponse)
async def get_me(user_id: CurrentUserRequired, db: DBDep) -> UserResponse:
    user = await User.find_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return _user_to_response(user)


@router.post("/logout")
async def logout(_user_id: CurrentUserRequired) -> dict:
    return {"status": "ok", "message": "Logged out"}


@router.post("/verify-email")
async def verify_email(body: VerifyEmailRequest, db: DBDep) -> dict:
    vt = await VerificationToken.find_valid(db, body.token, "email_verification")
    if not vt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token",
        )

    user = await User.find_by_id(db, vt.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.email_verified = True
    await VerificationToken.mark_used(db, vt.id)
    await db.commit()

    return {"status": "ok", "message": "Email verified"}


@router.post("/resend-verification")
async def resend_verification(user_id: CurrentUserRequired, db: DBDep) -> dict:
    user = await User.find_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if user.email_verified:
        return {"status": "ok", "message": "Email already verified"}

    token = secrets.token_urlsafe(32)
    await VerificationToken.create(
        db,
        user_id=str(user.id),
        token=token,
        token_type="email_verification",
    )
    await email_service.send_verification_email(user.email, user.display_name, token)

    return {"status": "ok", "message": "Verification email sent"}


@router.post("/request-reset")
async def request_reset(body: RequestResetRequest, db: DBDep) -> dict:
    user = await User.find_by_email(db, body.email)
    if not user:
        return {"status": "ok", "message": "If the email exists, a reset link has been sent"}

    token = secrets.token_urlsafe(32)
    await VerificationToken.create(
        db,
        user_id=str(user.id),
        token=token,
        token_type="password_reset",
        expires_in_hours=1,
    )
    await email_service.send_password_reset_email(
        user.email, user.display_name, token
    )

    return {"status": "ok", "message": "If the email exists, a reset link has been sent"}


@router.post("/reset-password")
async def reset_password(body: ResetPasswordRequest, db: DBDep) -> dict:
    vt = await VerificationToken.find_valid(db, body.token, "password_reset")
    if not vt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )

    user = await User.find_by_id(db, vt.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.hashed_password = pwd_context.hash(body.password)
    await VerificationToken.mark_used(db, vt.id)
    await db.commit()

    return {"status": "ok", "message": "Password reset successfully"}
