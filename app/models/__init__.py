"""SQLAlchemy models.

Importing this package imports every model module so that ``Base.metadata`` is
fully populated for Alembic autogenerate and for the app.
"""

from __future__ import annotations

from app.models.base import Base
from app.models.bike import Bike
from app.models.email_log import EmailLog
from app.models.newsletter import NewsletterSubscriber
from app.models.order import Order
from app.models.reservation import Reservation
from app.models.service_record import ServiceRecord
from app.models.user import RefreshToken, User
from app.models.workshop import Workshop

__all__ = [
    "Base",
    "Bike",
    "EmailLog",
    "NewsletterSubscriber",
    "Order",
    "RefreshToken",
    "Reservation",
    "ServiceRecord",
    "User",
    "Workshop",
]
