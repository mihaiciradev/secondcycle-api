"""SQLAlchemy models.

Importing this package must import every model module so that
``Base.metadata`` is fully populated for Alembic autogenerate.
"""

from __future__ import annotations

from app.models.base import Base

__all__ = ["Base"]
