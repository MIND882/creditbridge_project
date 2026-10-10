"""
Opportunity model for CreditBridge CRM.

An Opportunity represents a qualified sales interest that originates from
EITHER a Lead (new prospect) OR an existing Customer (repeat business).
Exactly one of `lead_id` / `customer_id` must be set — enforced by a
DB-level CHECK constraint below.

This replaces ERPNext's `opportunity_from` + `party_name` Dynamic Link
pattern (which requires a Frappe-specific runtime resolution mechanism
with no native SQL equivalent) with two explicit, typed, FK-constrained
columns. This gives us real referential integrity at the database level,
which the Dynamic Link pattern cannot provide in plain Postgres.
"""

import enum
import uuid
from datetime import date, datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    text,
)
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.session import Base


class OpportunityStatus(str, enum.Enum):
    OPEN = "open"
    QUOTATION_SENT = "quotation_sent"
    WON = "won"
    LOST = "lost"
    CLOSED = "closed"


class OpportunitySalesStage(str, enum.Enum):
    PROSPECTING = "prospecting"
    QUALIFICATION = "qualification"
    NEEDS_ANALYSIS = "needs_analysis"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"


class Opportunity(Base):
    """
    A qualified sales interest, originating from a Lead (new prospect) or
    an existing Customer (repeat business). Lives in the CRM domain
    package — unlike Customer, Opportunity has no life beyond the sales
    pipeline and is safe to keep CRM-scoped.
    """

    __tablename__ = "opportunities"

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

    # ── Origin: exactly one of these two must be set ─────────────────────
    # Replaces ERPNext's opportunity_from + party_name Dynamic Link.
    lead_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("leads.id", ondelete="SET NULL"),
        nullable=True,
    )
    customer_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="SET NULL"),
        nullable=True,
    )

    # ── Outcome: set ONLY when this Opportunity is won and converted ────
    # This is DIFFERENT from `customer_id` above (which tracks ORIGIN —
    # "this Opportunity started from an existing Customer"). This field
    # tracks OUTCOME — "this Opportunity, which may have started from a
    # Lead, resulted in this Customer being created." Kept as a separate
    # column specifically so it does NOT interact with the
    # ck_opportunity_exactly_one_party CHECK constraint below.
    converted_customer_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="SET NULL"),
        nullable=True,
    )

    # ── Core fields ────────────────────────────────────────────────────────
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    opportunity_amount: Mapped[Optional[float]] = mapped_column(
        Numeric(14, 2), nullable=True
    )
    # Multi-currency fields reserved for Phase 2 (international trade rails)
    # but INR-only logic applies for now — currency defaults to INR and is
    # not yet exposed for editing anywhere in the app layer.
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="INR")

    status: Mapped[OpportunityStatus] = mapped_column(
        SAEnum(OpportunityStatus, name="opportunity_status", native_enum=False),
        nullable=False,
        default=OpportunityStatus.OPEN,
        index=True,
    )
    sales_stage: Mapped[Optional[OpportunitySalesStage]] = mapped_column(
        SAEnum(OpportunitySalesStage, name="opportunity_sales_stage", native_enum=False),
        nullable=True,
        default=OpportunitySalesStage.PROSPECTING,
    )
    probability: Mapped[Optional[float]] = mapped_column(
        Numeric(5, 2), nullable=True, comment="Percent, 0-100. Manual for now; AI-suggested later."
    )
    expected_closing_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    opportunity_owner_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True, comment="User assigned to this opportunity"
    )

    # ── Lost tracking (no separate lookup tables — plain text for MVP) ─────
    lost_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    competitor: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # ── Soft Delete ───────────────────────────────────────────────────────
    is_deleted: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, index=True
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # ── Audit ─────────────────────────────────────────────────────────────
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

    # ── Constraints & Indexes ────────────────────────────────────────────
    __table_args__ = (
        # Exactly one of lead_id / customer_id must be set — never both,
        # never neither. This is the SQL-native replacement for ERPNext's
        # Dynamic Link (opportunity_from + party_name).
        CheckConstraint(
            "(lead_id IS NOT NULL)::int + (customer_id IS NOT NULL)::int = 1",
            name="ck_opportunity_exactly_one_party",
        ),
        Index(
            "ix_opportunities_business_status_created",
            "business_id",
            "status",
            "created_at",
            postgresql_where=text("is_deleted = false"),
        ),
        Index(
            "ix_opportunities_lead_id",
            "lead_id",
            postgresql_where=text("is_deleted = false"),
        ),
        Index(
            "ix_opportunities_customer_id",
            "customer_id",
            postgresql_where=text("is_deleted = false"),
        ),
        Index(
            "ix_opportunities_converted_customer_id",
            "converted_customer_id",
            postgresql_where=text("is_deleted = false"),
        ),
    )
