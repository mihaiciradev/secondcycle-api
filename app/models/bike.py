"""Bike model — a single physical unit for sale."""

from __future__ import annotations

from sqlalchemy import Integer, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import BikeCategory, BikeStatus, ConditionGrade, pg_enum


class Bike(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "bikes"

    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    frame_number: Mapped[str] = mapped_column(Text, nullable=False)
    brand: Mapped[str | None] = mapped_column(String(255), nullable=True)
    model: Mapped[str | None] = mapped_column(String(255), nullable=True)
    model_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    category: Mapped[BikeCategory] = mapped_column(
        pg_enum(BikeCategory, "bike_category"), nullable=False
    )
    frame_size: Mapped[str | None] = mapped_column(String(50), nullable=True)
    wheel_size: Mapped[str | None] = mapped_column(String(50), nullable=True)
    condition_grade: Mapped[ConditionGrade] = mapped_column(
        pg_enum(ConditionGrade, "condition_grade"), nullable=False
    )
    # Money in integer bani (RON * 100). Never floats.
    price_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    old_price_cents: Mapped[int | None] = mapped_column(Integer, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Ordered list of strings.
    work_done: Mapped[list[str]] = mapped_column(
        JSONB, nullable=False, default=list, server_default=text("'[]'::jsonb")
    )
    status: Mapped[BikeStatus] = mapped_column(
        pg_enum(BikeStatus, "bike_status"),
        nullable=False,
        default=BikeStatus.draft,
        server_default=BikeStatus.draft.value,
        index=True,
    )
    # Ordered list of R2 object keys.
    photos: Mapped[list[str]] = mapped_column(
        JSONB, nullable=False, default=list, server_default=text("'[]'::jsonb")
    )
