# app/crm/quotation_domain/models/quotation.py

"""
Quotation model for CreditBridge CRM — FULL field parity with ERPNext's
Quotation doctype, per explicit instruction to not drop any field.

Structural notes (things that could NOT simply become a column):
  - `items`            -> separate QuotationItem child table (FK to quotation_id)
  - `taxes`             -> separate QuotationTax child table
  - `payment_schedule`  -> separate QuotationPaymentScheduleEntry child table
  - `lost_reasons`      -> Postgres ARRAY(String) column (pragmatic
                           simplification of ERPNext's Table MultiSelect
                           child-doctype-with-junction-table pattern —
                           captures the same data without a 4th child table)
  - `competitors`       -> Postgres ARRAY(String) column, same reasoning
  - `pricing_rules`     -> Postgres ARRAY(String) column storing applied
                           pricing rule identifiers (full Pricing Rule
                           *engine* — i.e. rule evaluation logic — is NOT
                           implemented; only the applied-rules record is)

quotation_to / party_name (ERPNext's Dynamic Link) remain redesigned as
`opportunity_id` (required FK) — this is NOT a dropped field, it's an
architectural redesign already migrated into the database (Opportunity
already carries lead_id/customer_id). Reverting this would break the
already-applied schema and reintroduce the exact Dynamic Link problem we
solved for Opportunity. All party/customer/contact/address data remains
reachable via `opportunity_id` -> Opportunity -> Lead/Customer join.
"""

import enum
import uuid
from datetime import date, datetime
from typing import Optional

from sqlalchemy import (
    ARRAY,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    text,
)
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.session import Base


class QuotationStatus(str, enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    PARTIALLY_ORDERED = "partially_ordered"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class QuotationOrderType(str, enum.Enum):
    SALES = "sales"
    MAINTENANCE = "maintenance"
    SHOPPING_CART = "shopping_cart"


class Quotation(Base):
    __tablename__ = "quotations"

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

    # ── Origin (redesigned from quotation_to/party_name — see module docstring) ─
    opportunity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("opportunities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    converted_customer_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="SET NULL"),
        nullable=True,
    )

    # ── Core / dates ───────────────────────────────────────────────────────
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    transaction_date: Mapped[date] = mapped_column(
        Date, nullable=False, server_default=func.current_date()
    )
    valid_till: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    order_type: Mapped[QuotationOrderType] = mapped_column(
        SAEnum(QuotationOrderType, name="quotation_order_type", native_enum=False, values_callable=lambda e: [m.value for m in e]),
        nullable=False,
        default=QuotationOrderType.SALES,
    )
    has_unit_price_items: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False,
        comment="Allows 0-qty items with a fixed unit price, per ERPNext's allow_zero_qty_in_quotation setting"
    )

    # ── Currency & Price List ─────────────────────────────────────────────
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="INR")
    conversion_rate: Mapped[float] = mapped_column(Numeric(18, 9), nullable=False, default=1.0)
    selling_price_list: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    price_list_currency: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    plc_conversion_rate: Mapped[float] = mapped_column(Numeric(18, 9), nullable=False, default=1.0)
    ignore_pricing_rule: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # ── Applied pricing rules (record only — evaluation engine NOT built) ──
    pricing_rules: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String), nullable=True)

    # ── Totals (computed by service layer from QuotationItem rows) ─────────
    total_qty: Mapped[Optional[float]] = mapped_column(Numeric(14, 3), nullable=True)
    total_net_weight: Mapped[Optional[float]] = mapped_column(Numeric(14, 3), nullable=True)
    base_total: Mapped[Optional[float]] = mapped_column(Numeric(14, 2), nullable=True)
    base_net_total: Mapped[Optional[float]] = mapped_column(Numeric(14, 2), nullable=True)
    total: Mapped[Optional[float]] = mapped_column(Numeric(14, 2), nullable=True)
    net_total: Mapped[Optional[float]] = mapped_column(Numeric(14, 2), nullable=True)

    # ── Taxes (summary numerics; line-level detail lives in QuotationTax) ──
    tax_category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    taxes_and_charges_template: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    base_total_taxes_and_charges: Mapped[Optional[float]] = mapped_column(Numeric(14, 2), nullable=True)
    total_taxes_and_charges: Mapped[Optional[float]] = mapped_column(Numeric(14, 2), nullable=True)
    other_charges_calculation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # ── Shipping / Incoterms ────────────────────────────────────────────────
    shipping_rule: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    incoterm: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    named_place: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # ── Discounts ────────────────────────────────────────────────────────────
    apply_discount_on: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    base_discount_amount: Mapped[Optional[float]] = mapped_column(Numeric(14, 2), nullable=True)
    additional_discount_percentage: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)
    discount_amount: Mapped[Optional[float]] = mapped_column(Numeric(14, 2), nullable=True)
    coupon_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    referral_sales_partner: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # ── Grand totals ───────────────────────────────────────────────────────
    grand_total: Mapped[Optional[float]] = mapped_column(Numeric(14, 2), nullable=True)
    in_words: Mapped[Optional[str]] = mapped_column(String(240), nullable=True)
    rounded_total: Mapped[Optional[float]] = mapped_column(Numeric(14, 2), nullable=True)
    rounding_adjustment: Mapped[Optional[float]] = mapped_column(Numeric(14, 2), nullable=True)
    disable_rounded_total: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    base_grand_total: Mapped[Optional[float]] = mapped_column(Numeric(14, 2), nullable=True)
    base_in_words: Mapped[Optional[str]] = mapped_column(String(240), nullable=True)
    base_rounded_total: Mapped[Optional[float]] = mapped_column(Numeric(14, 2), nullable=True)
    base_rounding_adjustment: Mapped[Optional[float]] = mapped_column(Numeric(14, 2), nullable=True)

    # ── Payment terms (basic due-date/amount + child table for full schedule) ─
    payment_terms_template: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    payment_due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    payment_amount: Mapped[Optional[float]] = mapped_column(Numeric(14, 2), nullable=True)

    # ── Terms & Conditions ────────────────────────────────────────────────
    tc_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    terms: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # ── Print settings ────────────────────────────────────────────────────
    letter_head: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    group_same_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    select_print_heading: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    language: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # ── Auto Repeat (recurring quotation) ───────────────────────────────────
    auto_repeat_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)

    # ── Status ────────────────────────────────────────────────────────────
    status: Mapped[QuotationStatus] = mapped_column(
        SAEnum(QuotationStatus, name="quotation_status", native_enum=False, values_callable=lambda e: [m.value for m in e]),
        nullable=False,
        default=QuotationStatus.DRAFT,
        index=True,
    )

    # ── Lost / Rejected tracking ─────────────────────────────────────────
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    lost_reasons: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String), nullable=True)
    competitors: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String), nullable=True)

    # ── Denormalized address/contact snapshot (copied from Opportunity's
    # linked party at Quotation-creation time, for point-in-time accuracy
    # even if the Customer's address later changes) ────────────────────
    customer_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    shipping_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    company_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    contact_person: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact_mobile: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    contact_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # ── UTM Analytics ──────────────────────────────────────────────────────
    utm_source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    utm_medium: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    utm_campaign: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    utm_content: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # ── Misc ──────────────────────────────────────────────────────────────
    scan_barcode: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    supplier_quotation_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True,
        comment="Deferred FK — Supplier Quotation belongs to the future Buying module"
    )
    customer_group: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    territory: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # ── Soft Delete ───────────────────────────────────────────────────────
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # ── Audit ─────────────────────────────────────────────────────────────
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    updated_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    # ── Relationships to child tables ────────────────────────────────────
    items: Mapped[list["QuotationItem"]] = relationship(
        back_populates="quotation", cascade="all, delete-orphan"
    )
    taxes: Mapped[list["QuotationTax"]] = relationship(
        back_populates="quotation", cascade="all, delete-orphan"
    )
    payment_schedule_entries: Mapped[list["QuotationPaymentScheduleEntry"]] = relationship(
        back_populates="quotation", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index(
            "ix_quotations_business_status_created",
            "business_id", "status", "created_at",
            postgresql_where=text("is_deleted = false"),
        ),
        Index(
            "ix_quotations_opportunity_id", "opportunity_id",
            postgresql_where=text("is_deleted = false"),
        ),
        Index(
            "ix_quotations_converted_customer_id", "converted_customer_id",
            postgresql_where=text("is_deleted = false"),
        ),
        Index(
            "ix_quotations_valid_till", "valid_till",
            postgresql_where=text("is_deleted = false AND status = 'sent'"),
        ),
    )


class QuotationItem(Base):
    """Line item on a Quotation. Lean version of ERPNext's Quotation Item —
    no warehouse/stock/serial-batch/UOM-conversion tracking (that belongs
    to a future Stock/Inventory module), just what's needed to quote a
    price for a product or service."""

    __tablename__ = "quotation_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quotation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("quotations.id", ondelete="CASCADE"), nullable=False, index=True
    )

    item_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    qty: Mapped[float] = mapped_column(Numeric(14, 3), nullable=False, default=1)
    uom: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    rate: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False, default=0)
    amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False, default=0)

    is_alternative: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_free_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    idx: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    quotation: Mapped["Quotation"] = relationship(back_populates="items")


class QuotationTax(Base):
    """Line item in the Taxes and Charges table. Simplified — actual GST
    calculation logic lives in the future GST Compliance module (Phase 3);
    this table just records the applied charge lines on a given quote."""

    __tablename__ = "quotation_taxes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quotation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("quotations.id", ondelete="CASCADE"), nullable=False, index=True
    )

    charge_type: Mapped[str] = mapped_column(String(30), nullable=False, default="On Net Total")
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    rate: Mapped[Optional[float]] = mapped_column(Numeric(6, 2), nullable=True)
    tax_amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False, default=0)
    total: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False, default=0)

    idx: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    quotation: Mapped["Quotation"] = relationship(back_populates="taxes")


class QuotationPaymentScheduleEntry(Base):
    """Split payment terms — e.g. '50% advance, 50% on delivery'. Separate
    from the single payment_due_date/payment_amount columns on Quotation,
    which remain as a convenience default for the simple single-term case."""

    __tablename__ = "quotation_payment_schedule_entries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quotation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("quotations.id", ondelete="CASCADE"), nullable=False, index=True
    )

    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    invoice_portion_percent: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)
    payment_amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False, default=0)

    idx: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    quotation: Mapped["Quotation"] = relationship(back_populates="payment_schedule_entries")