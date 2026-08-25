"""Application settings, loaded from environment via pydantic-settings.

Every value comes from the environment. See ``.env.example`` for the full
documented list. Secrets must never be hard-coded here.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Annotated, Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- Environment -------------------------------------------------------
    environment: Literal["local", "staging", "production", "test"] = "local"

    # --- Database ----------------------------------------------------------
    # Pooled (PgBouncer transaction mode) URL used by the app. asyncpg prepared
    # statement caching is disabled at the engine layer for this reason.
    database_url: str
    # Direct (unpooled) URL used by Alembic migrations only.
    database_url_direct: str

    # --- Auth / JWT --------------------------------------------------------
    jwt_secret: str = Field(min_length=32)
    access_token_ttl_seconds: int = 15 * 60
    refresh_token_ttl_seconds: int = 30 * 24 * 60 * 60

    google_client_id: str = ""

    # --- CORS --------------------------------------------------------------
    # Comma-separated list of exact allowed origins. Never "*" with credentials.
    cors_origins: Annotated[list[str], NoDecode] = Field(default_factory=list)

    # --- Email (Resend) ----------------------------------------------------
    resend_api_key: str = ""
    email_from: str = "SecondCycle <no-reply@secondcycle.ro>"
    # Public site origin, used to build links inside outbound emails.
    frontend_base_url: str = "https://www.secondcycle.ro"

    # --- Cloudflare R2 (S3 API) -------------------------------------------
    r2_account_id: str = ""
    r2_access_key_id: str = ""
    r2_secret_access_key: str = ""
    r2_bucket: str = ""
    # Full S3 endpoint, e.g. https://<account>.r2.cloudflarestorage.com
    r2_endpoint_url: str = ""

    # --- Seed admin (used by `python -m app.seed`) -------------------------
    admin_email: str = ""
    admin_password: str = ""

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_cors(cls, value: object) -> object:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
