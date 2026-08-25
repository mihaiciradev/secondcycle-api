"""Service record — the service paper, per bike, at intake and final."""

from __future__ import annotations

import datetime as dt
from typing import Any
from uuid import UUID

from sqlalchemy import Date, DateTime, ForeignKey, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDPrimaryKeyMixin
from app.models.enums import ServiceRecordKind, pg_enum


class ServiceRecord(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "service_records"
    __table_args__ = (
        # At most one 'intake' and one 'final' per bike.
        UniqueConstraint("bike_id", "kind", name="uq_service_record_bike_kind"),
    )

    bike_id: Mapped[UUID] = mapped_column(
        ForeignKey("bikes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    workshop_id: Mapped[UUID] = mapped_column(
        ForeignKey("workshops.id"), nullable=False, index=True
    )
    kind: Mapped[ServiceRecordKind] = mapped_column(
        pg_enum(ServiceRecordKind, "service_record_kind"), nullable=False
    )
    # List of {item, status: ok|replaced|repaired|attention, note: str|null}.
    checklist: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    performed_by: Mapped[str] = mapped_column(Text, nullable=False)
    performed_at: Mapped[dt.date] = mapped_column(Date, nullable=False)
    created_by: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
