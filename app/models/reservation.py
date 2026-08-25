"""Reservation — the 30-minute hold on a bike."""

from __future__ import annotations

import datetime as dt
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDPrimaryKeyMixin
from app.models.enums import ReservationStatus, pg_enum


class Reservation(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "reservations"
    __table_args__ = (
        # At most one active hold per bike, and one active hold per user.
        # These partial unique indexes are the final race-condition guarantee.
        Index(
            "uq_reservation_active_bike",
            "bike_id",
            unique=True,
            postgresql_where=text("status = 'active'"),
        ),
        Index(
            "uq_reservation_active_user",
            "user_id",
            unique=True,
            postgresql_where=text("status = 'active'"),
        ),
    )

    bike_id: Mapped[UUID] = mapped_column(
        ForeignKey("bikes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[ReservationStatus] = mapped_column(
        pg_enum(ReservationStatus, "reservation_status"),
        nullable=False,
        default=ReservationStatus.active,
    )
    expires_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
