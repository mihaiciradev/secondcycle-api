"""Newsletter subscriber model (non-account emails, double opt-in)."""

from __future__ import annotations

import datetime as dt

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class NewsletterSubscriber(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "newsletter_subscribers"

    email: Mapped[str] = mapped_column(CITEXT, unique=True, nullable=False)
    confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    # sha256 hashes of single-use tokens.
    confirm_token_hash: Mapped[str | None] = mapped_column(
        String(64), nullable=True, index=True
    )
    unsubscribe_token_hash: Mapped[str | None] = mapped_column(
        String(64), nullable=True, index=True
    )
    confirmed_at: Mapped[dt.datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    unsubscribed_at: Mapped[dt.datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
