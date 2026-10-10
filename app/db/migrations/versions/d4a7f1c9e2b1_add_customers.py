"""add customers table

Revision ID: d4a7f1c9e2b1
Revises: c3f1a9e2b6d4
Create Date: 2026-08-03
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "d4a7f1c9e2b1"
down_revision: Union[str, None] = "c3f1a9e2b6d4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "customers",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "business_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("businesses.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("customer_name", sa.String(length=255), nullable=False),
        sa.Column("customer_group", sa.String(length=100), nullable=True),
        sa.Column("territory", sa.String(length=100), nullable=True),
        sa.Column("industry", sa.String(length=100), nullable=True),
        sa.Column("primary_contact_name", sa.String(length=255), nullable=True),
        sa.Column("primary_contact_email", sa.String(length=255), nullable=True),
        sa.Column("primary_contact_phone", sa.String(length=15), nullable=True),
        sa.Column("address_line", sa.String(length=255), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=100), nullable=True),
        sa.Column("country", sa.String(length=100), nullable=False, server_default="India"),
        sa.Column("pincode", sa.String(length=10), nullable=True),
        sa.Column("gstin", sa.String(length=15), nullable=True),
        sa.Column("pan", sa.String(length=10), nullable=True),
        sa.Column(
            "converted_from_lead_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("leads.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("converted_from_opportunity_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("converted_from_quotation_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default="active",
        ),
        sa.Column("credit_readiness_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("gst_status", sa.String(length=30), nullable=True),
        sa.Column("bank_connection_status", sa.String(length=30), nullable=True),
        sa.Column("loan_eligibility_flag", sa.Boolean(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_index(
        "ix_customers_business_status_created",
        "customers",
        ["business_id", "status", "created_at"],
        postgresql_where=sa.text("is_deleted = false"),
    )
    op.create_index(
        "ix_customers_business_name",
        "customers",
        ["business_id", "customer_name"],
        postgresql_where=sa.text("is_deleted = false"),
    )
    op.create_index(
        "ix_customers_business_gst_status",
        "customers",
        ["business_id", "gst_status"],
        postgresql_where=sa.text("is_deleted = false"),
    )
    op.create_index(
        "ix_customers_business_credit_score",
        "customers",
        ["business_id", "credit_readiness_score"],
        postgresql_where=sa.text("is_deleted = false"),
    )
    op.create_index(
        "ix_customers_business_id", "customers", ["business_id"]
    )
    op.create_index("ix_customers_status", "customers", ["status"])
    op.create_index("ix_customers_is_deleted", "customers", ["is_deleted"])


def downgrade() -> None:
    op.drop_index("ix_customers_is_deleted", table_name="customers")
    op.drop_index("ix_customers_status", table_name="customers")
    op.drop_index("ix_customers_business_id", table_name="customers")
    op.drop_index("ix_customers_business_credit_score", table_name="customers")
    op.drop_index("ix_customers_business_gst_status", table_name="customers")
    op.drop_index("ix_customers_business_name", table_name="customers")
    op.drop_index("ix_customers_business_status_created", table_name="customers")
    op.drop_table("customers")
