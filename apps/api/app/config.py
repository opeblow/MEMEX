from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "MEMEX"
    app_version: str = "1.0.0"
    debug: bool = False

    database_url: str = "postgresql+asyncpg://memex:memex@localhost:5432/memex"
    database_url_sync: str = "postgresql+psycopg2://memex:memex@localhost:5432/memex"

    jwt_secret: str = "change-me-to-a-long-random-string"
    jwt_algorithm: str = "HS256"
    jwt_access_expire_minutes: int = 15
    jwt_refresh_expire_days: int = 7

    google_client_id: str | None = None
    google_client_secret: str | None = None

    resend_api_key: str | None = None

    openai_api_key: str | None = None

    cognee_api_key: str | None = None
    cognee_url: str = "http://localhost:8001"

    app_url: str = "http://localhost:3000"

    allowed_origins: list[str] = ["http://localhost:3000"]

    model_config = {"env_prefix": "", "case_sensitive": False}


settings = Settings()
