"""Email log — metadata for every outbound email (no body storage)."""

from __future__ import annotations

import datetime as dt

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDPrimaryKeyMixin
from app.models.enums import EmailStatus, pg_enum


class EmailLog(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "email_log"

    to_email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    template: Mapped[str] = mapped_column(String(100), nullable=False)
    subject: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[EmailStatus] = mapped_column(
        pg_enum(EmailStatus, "email_status"), nullable=False
    )
    provider_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
