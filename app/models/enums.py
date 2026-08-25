"""Enumerations shared by models and schemas.

Each maps to a native Postgres enum type (created in the Alembic migration).
The string values are the on-the-wire and in-database representation.
"""

from __future__ import annotations

import enum

import sqlalchemy as sa


def pg_enum(py_enum: type[enum.Enum], name: str) -> sa.Enum:
    """Build a native Postgres enum column type.

    ``create_type=False``: the Alembic migration owns type creation, so the ORM
    never attempts an implicit ``CREATE TYPE``. ``values_callable`` stores the
    enum *value* (not the member name) in the database.
    """
    return sa.Enum(
        py_enum,
        name=name,
        native_enum=True,
        create_type=False,
        values_callable=lambda e: [member.value for member in e],
    )


class UserRole(enum.StrEnum):
    customer = "customer"
    admin = "admin"


class BikeCategory(enum.StrEnum):
    city = "city"
    trekking = "trekking"
    mtb = "mtb"
    road = "road"
    kids = "kids"
    ebike = "ebike"


class ConditionGrade(enum.StrEnum):
    A = "A"
    B = "B"
    C = "C"


class BikeStatus(enum.StrEnum):
    draft = "draft"
    available = "available"
    reserved = "reserved"
    sold = "sold"
    withdrawn = "withdrawn"


class ServiceRecordKind(enum.StrEnum):
    intake = "intake"
    final = "final"


class ReservationStatus(enum.StrEnum):
    active = "active"
    expired = "expired"
    cancelled = "cancelled"
    converted = "converted"


class OrderStatus(enum.StrEnum):
    pending = "pending"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"


class RepairTier(enum.StrEnum):
    basic = "basic"
    quality = "quality"
    premium = "premium"


class BillingType(enum.StrEnum):
    individual = "individual"
    company = "company"


class DeliveryMethod(enum.StrEnum):
    pickup = "pickup"
    courier = "courier"


class EmailStatus(enum.StrEnum):
    sent = "sent"
    failed = "failed"


# --- Non-DB enums (used inside JSONB payloads / validated by Pydantic) --------


class ChecklistItemStatus(enum.StrEnum):
    ok = "ok"
    replaced = "replaced"
    repaired = "repaired"
    attention = "attention"
