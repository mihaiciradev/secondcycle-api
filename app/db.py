"""Async database engine and session management.

The app connects through Neon's pooled URL, which runs PgBouncer in
transaction mode. asyncpg's prepared-statement cache is incompatible with
that, so we disable it via ``statement_cache_size=0``. Alembic uses the
direct (unpooled) URL and is configured separately in ``migrations/env.py``.
"""

from __future__ import annotations

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import get_settings


def _create_engine() -> AsyncEngine:
    settings = get_settings()
    return create_async_engine(
        settings.database_url,
        pool_pre_ping=True,
        connect_args={
            # Required for PgBouncer transaction-mode pooling.
            "statement_cache_size": 0,
            # Neon requires TLS. asyncpg does not understand libpq's
            # sslmode/channel_binding query params, so we strip those from the
            # URL and enable SSL here instead.
            "ssl": True,
        },
    )


engine: AsyncEngine = _create_engine()

SessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)


async def get_session() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency yielding a transactional session.

    The session commits on success and rolls back on any exception, then is
    always closed.
    """
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
