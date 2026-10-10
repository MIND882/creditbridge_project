"""add quotations table (full field parity) + child tables

Revision ID: f6c9h3e1g4d3
Revises: e5b8g2d0f3c2
Create Date: 2026-08-05

Verify `down_revision` matches your actual current head (`alembic heads`)
before running.

Creates 4 tables:
  - quotations (main table, full ERPNext field parity)
  - quotation_items (line items)
  - quotation_taxes (tax/charge lines)
  - quotation_payment_schedule_entries (split payment terms)
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "f6c9h3e1g4d3"
down_revision: Union[str, None] = "e5b8g2d0f3c2"  # <- VERIFY against `alembic heads`
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "quotations",
        sa.Column(
            "id", postgresql.UUID(as_uuid=True), primary_key=True,
            default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "business_id", postgresql.UUID(as_uuid=True),
            sa.ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False,
        ),
        sa.Column(
            "opportunity_id", postgresql.UUID(as_uuid=True),
            sa.ForeignKey("opportunities.id", ondelete="CASCADE"), nullable=False,
        ),
        sa.Column(
            "converted_customer_id", postgresql.UUID(as_uuid=True),
            sa.ForeignKey("customers.id", ondelete="SET NULL"), nullable=True,
        ),
        # Core / dates
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("transaction_date", sa.Date(), nullable=False, server_default=sa.text("CURRENT_DATE")),
        sa.Column("valid_till", sa.Date(), nullable=True),
        sa.Column("order_type", sa.String(length=20), nullable=False, server_default="sales"),
        sa.Column("has_unit_price_items", sa.Boolean(), nullable=False, server_default=sa.false()),
        # Currency & Price List
        sa.Column("currency", sa.String(length=3), nullable=False, server_default="INR"),
        sa.Column("conversion_rate", sa.Numeric(18, 9), nullable=False, server_default="1.0"),
        sa.Column("selling_price_list", sa.String(length=100), nullable=True),
        sa.Column("price_list_currency", sa.String(length=3), nullable=True),
        sa.Column("plc_conversion_rate", sa.Numeric(18, 9), nullable=False, server_default="1.0"),
        sa.Column("ignore_pricing_rule", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("pricing_rules", postgresql.ARRAY(sa.String()), nullable=True),
        # Totals
        sa.Column("total_qty", sa.Numeric(14, 3), nullable=True),
        sa.Column("total_net_weight", sa.Numeric(14, 3), nullable=True),
        sa.Column("base_total", sa.Numeric(14, 2), nullable=True),
        sa.Column("base_net_total", sa.Numeric(14, 2), nullable=True),
        sa.Column("total", sa.Numeric(14, 2), nullable=True),
        sa.Column("net_total", sa.Numeric(14, 2), nullable=True),
        # Taxes
        sa.Column("tax_category", sa.String(length=100), nullable=True),
        sa.Column("taxes_and_charges_template", sa.String(length=255), nullable=True),
        sa.Column("base_total_taxes_and_charges", sa.Numeric(14, 2), nullable=True),
        sa.Column("total_taxes_and_charges", sa.Numeric(14, 2), nullable=True),
        sa.Column("other_charges_calculation", sa.Text(), nullable=True),
        # Shipping / Incoterms
        sa.Column("shipping_rule", sa.String(length=100), nullable=True),
        sa.Column("incoterm", sa.String(length=10), nullable=True),
        sa.Column("named_place", sa.String(length=255), nullable=True),
        # Discounts
        sa.Column("apply_discount_on", sa.String(length=20), nullable=True),
        sa.Column("base_discount_amount", sa.Numeric(14, 2), nullable=True),
        sa.Column("additional_discount_percentage", sa.Numeric(5, 2), nullable=True),
        sa.Column("discount_amount", sa.Numeric(14, 2), nullable=True),
        sa.Column("coupon_code", sa.String(length=50), nullable=True),
        sa.Column("referral_sales_partner", sa.String(length=255), nullable=True),
        # Grand totals
        sa.Column("grand_total", sa.Numeric(14, 2), nullable=True),
        sa.Column("in_words", sa.String(length=240), nullable=True),
        sa.Column("rounded_total", sa.Numeric(14, 2), nullable=True),
        sa.Column("rounding_adjustment", sa.Numeric(14, 2), nullable=True),
        sa.Column("disable_rounded_total", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("base_grand_total", sa.Numeric(14, 2), nullable=True),
        sa.Column("base_in_words", sa.String(length=240), nullable=True),
        sa.Column("base_rounded_total", sa.Numeric(14, 2), nullable=True),
        sa.Column("base_rounding_adjustment", sa.Numeric(14, 2), nullable=True),
        # Payment terms
        sa.Column("payment_terms_template", sa.String(length=255), nullable=True),
        sa.Column("payment_due_date", sa.Date(), nullable=True),
        sa.Column("payment_amount", sa.Numeric(14, 2), nullable=True),
        # Terms & Conditions
        sa.Column("tc_name", sa.String(length=255), nullable=True),
        sa.Column("terms", sa.Text(), nullable=True),
        # Print settings
        sa.Column("letter_head", sa.String(length=255), nullable=True),
        sa.Column("group_same_items", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("select_print_heading", sa.String(length=255), nullable=True),
        sa.Column("language", sa.String(length=20), nullable=True),
        # Auto Repeat
        sa.Column("auto_repeat_id", postgresql.UUID(as_uuid=True), nullable=True),
        # Status
        sa.Column("status", sa.String(length=20), nullable=False, server_default="draft"),
        # Lost/Rejected
        sa.Column("rejection_reason", sa.Text(), nullable=True),
        sa.Column("lost_reasons", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("competitors", postgresql.ARRAY(sa.String()), nullable=True),
        # Denormalized address/contact
        sa.Column("customer_address", sa.Text(), nullable=True),
        sa.Column("shipping_address", sa.Text(), nullable=True),
        sa.Column("company_address", sa.Text(), nullable=True),
        sa.Column("contact_person", sa.String(length=255), nullable=True),
        sa.Column("contact_mobile", sa.String(length=15), nullable=True),
        sa.Column("contact_email", sa.String(length=255), nullable=True),
        # UTM
        sa.Column("utm_source", sa.String(length=100), nullable=True),
        sa.Column("utm_medium", sa.String(length=100), nullable=True),
        sa.Column("utm_campaign", sa.String(length=100), nullable=True),
        sa.Column("utm_content", sa.String(length=100), nullable=True),
        # Misc
        sa.Column("scan_barcode", sa.String(length=100), nullable=True),
        sa.Column("supplier_quotation_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("customer_group", sa.String(length=100), nullable=True),
        sa.Column("territory", sa.String(length=100), nullable=True),
        # Soft delete
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        # Audit
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_index(
        "ix_quotations_business_status_created", "quotations",
        ["business_id", "status", "created_at"], postgresql_where=sa.text("is_deleted = false"),
    )
    op.create_index(
        "ix_quotations_opportunity_id", "quotations",
        ["opportunity_id"], postgresql_where=sa.text("is_deleted = false"),
    )
    op.create_index(
        "ix_quotations_converted_customer_id", "quotations",
        ["converted_customer_id"], postgresql_where=sa.text("is_deleted = false"),
    )
    op.create_index(
        "ix_quotations_valid_till", "quotations",
        ["valid_till"], postgresql_where=sa.text("is_deleted = false AND status = 'sent'"),
    )
    op.create_index("ix_quotations_business_id", "quotations", ["business_id"])
    op.create_index("ix_quotations_status", "quotations", ["status"])
    op.create_index("ix_quotations_is_deleted", "quotations", ["is_deleted"])

    # ── Child table: quotation_items ────────────────────────────────────
    op.create_table(
        "quotation_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text("gen_random_uuid()")),
        sa.Column(
            "quotation_id", postgresql.UUID(as_uuid=True),
            sa.ForeignKey("quotations.id", ondelete="CASCADE"), nullable=False,
        ),
        sa.Column("item_name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("qty", sa.Numeric(14, 3), nullable=False, server_default="1"),
        sa.Column("uom", sa.String(length=50), nullable=True),
        sa.Column("rate", sa.Numeric(14, 2), nullable=False, server_default="0"),
        sa.Column("amount", sa.Numeric(14, 2), nullable=False, server_default="0"),
        sa.Column("is_alternative", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("is_free_item", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("idx", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_quotation_items_quotation_id", "quotation_items", ["quotation_id"])

    # ── Child table: quotation_taxes ────────────────────────────────────
    op.create_table(
        "quotation_taxes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text("gen_random_uuid()")),
        sa.Column(
            "quotation_id", postgresql.UUID(as_uuid=True),
            sa.ForeignKey("quotations.id", ondelete="CASCADE"), nullable=False,
        ),
        sa.Column("charge_type", sa.String(length=30), nullable=False, server_default="On Net Total"),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("rate", sa.Numeric(6, 2), nullable=True),
        sa.Column("tax_amount", sa.Numeric(14, 2), nullable=False, server_default="0"),
        sa.Column("total", sa.Numeric(14, 2), nullable=False, server_default="0"),
        sa.Column("idx", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_quotation_taxes_quotation_id", "quotation_taxes", ["quotation_id"])

    # ── Child table: quotation_payment_schedule_entries ─────────────────
    op.create_table(
        "quotation_payment_schedule_entries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text("gen_random_uuid()")),
        sa.Column(
            "quotation_id", postgresql.UUID(as_uuid=True),
            sa.ForeignKey("quotations.id", ondelete="CASCADE"), nullable=False,
        ),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("due_date", sa.Date(), nullable=False),
        sa.Column("invoice_portion_percent", sa.Numeric(5, 2), nullable=True),
        sa.Column("payment_amount", sa.Numeric(14, 2), nullable=False, server_default="0"),
        sa.Column("idx", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index(
        "ix_quotation_payment_schedule_entries_quotation_id",
        "quotation_payment_schedule_entries", ["quotation_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_quotation_payment_schedule_entries_quotation_id", table_name="quotation_payment_schedule_entries")
    op.drop_table("quotation_payment_schedule_entries")

    op.drop_index("ix_quotation_taxes_quotation_id", table_name="quotation_taxes")
    op.drop_table("quotation_taxes")

    op.drop_index("ix_quotation_items_quotation_id", table_name="quotation_items")
    op.drop_table("quotation_items")

    op.drop_index("ix_quotations_is_deleted", table_name="quotations")
    op.drop_index("ix_quotations_status", table_name="quotations")
    op.drop_index("ix_quotations_business_id", table_name="quotations")
    op.drop_index("ix_quotations_valid_till", table_name="quotations")
    op.drop_index("ix_quotations_converted_customer_id", table_name="quotations")
    op.drop_index("ix_quotations_opportunity_id", table_name="quotations")
    op.drop_index("ix_quotations_business_status_created", table_name="quotations")
    op.drop_table("quotations")