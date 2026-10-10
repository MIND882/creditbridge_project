"""
Customer model for CreditBridge.
"""

import enum
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    text,
)
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.session import Base


class CustomerStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class CustomerGSTStatus(str, enum.Enum):
    NOT_LINKED = "not_linked"
    PENDING_VERIFICATION = "pending_verification"
    VERIFIED = "verified"


class CustomerBankConnectionStatus(str, enum.Enum):
    NOT_CONNECTED = "not_connected"
    PENDING = "pending"
    CONNECTED = "connected"


class Customer(Base):
    """
    A business counterparty that has been converted from a CRM lead and is
    now used across operational and financial modules.
    """

    __tablename__ = "customers"

    # ── Primary key ────────────────────────────────────────────────────────
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # ── Tenancy ────────────────────────────────────────────────────────────
    business_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Identity & Organization ────────────────────────────────────────────
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    customer_group: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    territory: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # ── Contact ────────────────────────────────────────────────────────────
    primary_contact_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    primary_contact_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    primary_contact_phone: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)

    # ── Address ────────────────────────────────────────────────────────────
    address_line: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False, default="India")
    pincode: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    # ── Tax / KYC (India-specific) ──────────────────────────────────────────
    gstin: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    pan: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    # ── Conversion Origin (from CRM) ─────────────────────────────────────────
    converted_from_lead_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("leads.id", ondelete="SET NULL"),
        nullable=True,
    )
    converted_from_opportunity_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
        comment="Deferred FK to opportunities.id — add constraint once Opportunity table exists",
    )
    converted_from_quotation_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
        comment="Deferred FK to quotations.id — add constraint once Quotation table exists",
    )

    # ── Status ────────────────────────────────────────────────────────────────
    status: Mapped[CustomerStatus] = mapped_column(
        SAEnum(CustomerStatus, name="customer_status", native_enum=False),
        nullable=False,
        default=CustomerStatus.ACTIVE,
        index=True,
    )

    # ── CreditBridge Intelligence Placeholders ───────────────────────────────
    credit_readiness_score: Mapped[Optional[float]] = mapped_column(
        Numeric(5, 2), nullable=True
    )
    gst_status: Mapped[Optional[CustomerGSTStatus]] = mapped_column(
        SAEnum(CustomerGSTStatus, name="customer_gst_status", native_enum=False),
        nullable=True,
    )
    bank_connection_status: Mapped[Optional[CustomerBankConnectionStatus]] = mapped_column(
        SAEnum(
            CustomerBankConnectionStatus,
            name="customer_bank_connection_status",
            native_enum=False,
        ),
        nullable=True,
    )
    loan_eligibility_flag: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    # ── Soft Delete ───────────────────────────────────────────────────────────
    is_deleted: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, index=True
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # ── Audit ─────────────────────────────────────────────────────────────────
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    updated_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    # ── Indexes ───────────────────────────────────────────────────────────────
    __table_args__ = (
        Index(
            "ix_customers_business_status_created",
            "business_id",
            "status",
            "created_at",
            postgresql_where=text("is_deleted = false"),
        ),
        Index(
            "ix_customers_business_name",
            "business_id",
            "customer_name",
            postgresql_where=text("is_deleted = false"),
        ),
        Index(
            "ix_customers_business_gst_status",
            "business_id",
            "gst_status",
            postgresql_where=text("is_deleted = false"),
        ),
        Index(
            "ix_customers_business_credit_score",
            "business_id",
            "credit_readiness_score",
            postgresql_where=text("is_deleted = false"),
        ),
    )
