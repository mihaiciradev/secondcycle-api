"""Order model.

Prices are snapshotted at creation: later edits to the bike's price must never
change an existing order's totals.
"""

from __future__ import annotations

import datetime as dt
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import (
    BillingType,
    DeliveryMethod,
    OrderStatus,
    RepairTier,
    pg_enum,
)


class Order(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "orders"

    # e.g. "SC-2026-000123", generated from the order_number_seq sequence.
    order_number: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)

    bike_id: Mapped[UUID] = mapped_column(
        ForeignKey("bikes.id"), nullable=False, index=True
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    reservation_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("reservations.id"), nullable=True
    )

    status: Mapped[OrderStatus] = mapped_column(
        pg_enum(OrderStatus, "order_status"),
        nullable=False,
        default=OrderStatus.pending,
        index=True,
    )
    repair_tier: Mapped[RepairTier] = mapped_column(
        pg_enum(RepairTier, "repair_tier"), nullable=False
    )

    # --- Money snapshots (integer bani) -----------------------------------
    bike_price_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    tier_price_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    total_cents: Mapped[int] = mapped_column(Integer, nullable=False)

    # --- Billing ----------------------------------------------------------
    billing_type: Mapped[BillingType] = mapped_column(
        pg_enum(BillingType, "billing_type"), nullable=False
    )
    billing_name: Mapped[str] = mapped_column(String(255), nullable=False)
    billing_email: Mapped[str] = mapped_column(String(255), nullable=False)
    billing_phone: Mapped[str] = mapped_column(String(50), nullable=False)
    billing_street: Mapped[str] = mapped_column(Text, nullable=False)
    billing_city: Mapped[str] = mapped_column(String(255), nullable=False)
    billing_county: Mapped[str] = mapped_column(String(64), nullable=False)
    billing_postal_code: Mapped[str] = mapped_column(String(16), nullable=False)
    billing_country: Mapped[str] = mapped_column(
        String(2), nullable=False, default="RO", server_default="RO"
    )

    # Required together when billing_type='company' (enforced in the schema).
    company_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    company_cui: Mapped[str | None] = mapped_column(String(16), nullable=True)
    company_reg_com: Mapped[str | None] = mapped_column(String(32), nullable=True)

    # --- Delivery ---------------------------------------------------------
    delivery_method: Mapped[DeliveryMethod] = mapped_column(
        pg_enum(DeliveryMethod, "delivery_method"), nullable=False
    )
    # Nullable when delivery_method='pickup'; required when 'courier'
    # (enforced in the schema).
    delivery_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    delivery_phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    delivery_street: Mapped[str | None] = mapped_column(Text, nullable=True)
    delivery_city: Mapped[str | None] = mapped_column(String(255), nullable=True)
    delivery_county: Mapped[str | None] = mapped_column(String(64), nullable=True)
    delivery_postal_code: Mapped[str | None] = mapped_column(String(16), nullable=True)
    delivery_country: Mapped[str | None] = mapped_column(String(2), nullable=True)

    # --- Terms consent (recorded, not shown by the API) -------------------
    terms_version: Mapped[str] = mapped_column(String(32), nullable=False)
    terms_accepted_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    terms_accepted_ip: Mapped[str] = mapped_column(INET, nullable=False)

    customer_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    admin_note: Mapped[str | None] = mapped_column(Text, nullable=True)
