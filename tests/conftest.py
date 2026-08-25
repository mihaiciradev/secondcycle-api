"""Test harness — Docker-free, against a Neon test branch.

The whole suite runs against the database in ``TEST_DATABASE_URL`` (the direct,
unpooled URL of the Neon *preprod* branch). At session start the public schema
is dropped and rebuilt via the real Alembic migrations; every table is
truncated between tests. ``NullPool`` keeps no connections across tests, so the
shared engine is safe under pytest-asyncio's per-test event loops.
"""

from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

_ROOT = Path(__file__).resolve().parent.parent


def _load_dotenv() -> None:
    """Load .env into os.environ (only keys not already set)."""
    env_path = _ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()

TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")
if not TEST_DATABASE_URL:
    raise RuntimeError("TEST_DATABASE_URL is not set (see .env)")

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
    connect_args={"ssl": True},
)
TestSession = async_sessionmaker(test_engine, expire_on_commit=False, autoflush=False)


@pytest.fixture(scope="session", autouse=True)
def _prepare_database() -> Iterator[None]:
    """Rebuild the schema once per session from the real migrations."""

    async def _reset_schema() -> None:
        async with test_engine.begin() as conn:
            await conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
            await conn.execute(text("CREATE SCHEMA public"))

    asyncio.run(_reset_schema())

    cfg = Config(str(_ROOT / "alembic.ini"))
    cfg.set_main_option("script_location", str(_ROOT / "migrations"))
    cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    command.upgrade(cfg, "head")

    yield


@pytest.fixture(autouse=True)
async def _truncate_tables() -> AsyncIterator[None]:
    """Give every test a clean slate."""
    from app.models import Base

    tables = ", ".join(t.name for t in Base.metadata.sorted_tables)
    async with test_engine.begin() as conn:
        await conn.execute(text(f"TRUNCATE {tables} RESTART IDENTITY CASCADE"))
        await conn.execute(text("ALTER SEQUENCE order_number_seq RESTART"))
    yield


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    """An httpx client bound to the app, with the DB session overridden."""
    from app.db import get_session
    from app.main import app

    async def _override_get_session() -> AsyncIterator[object]:
        async with TestSession() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_session] = _override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
