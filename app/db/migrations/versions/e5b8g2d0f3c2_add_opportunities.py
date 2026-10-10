"""add opportunities table

Revision ID: e5b8g2d0f3c2
Revises: d4a7f1c9e2b1
Create Date: 2026-08-04
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "e5b8g2d0f3c2"
down_revision: Union[str, None] = "d4a7f1c9e2b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "opportunities",
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
        sa.Column(
            "lead_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("leads.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "customer_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("customers.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "converted_customer_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("customers.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("opportunity_amount", sa.Numeric(14, 2), nullable=True),
        sa.Column("currency", sa.String(length=3), nullable=False, server_default="INR"),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="open"),
        sa.Column("sales_stage", sa.String(length=30), nullable=True, server_default="prospecting"),
        sa.Column("probability", sa.Numeric(5, 2), nullable=True),
        sa.Column("expected_closing_date", sa.Date(), nullable=True),
        sa.Column("opportunity_owner_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("lost_reason", sa.Text(), nullable=True),
        sa.Column("competitor", sa.String(length=255), nullable=True),
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
        sa.CheckConstraint(
            "(lead_id IS NOT NULL)::int + (customer_id IS NOT NULL)::int = 1",
            name="ck_opportunity_exactly_one_party",
        ),
    )

    op.create_index(
        "ix_opportunities_business_status_created",
        "opportunities",
        ["business_id", "status", "created_at"],
        postgresql_where=sa.text("is_deleted = false"),
    )
    op.create_index(
        "ix_opportunities_lead_id",
        "opportunities",
        ["lead_id"],
        postgresql_where=sa.text("is_deleted = false"),
    )
    op.create_index(
        "ix_opportunities_customer_id",
        "opportunities",
        ["customer_id"],
        postgresql_where=sa.text("is_deleted = false"),
    )
    op.create_index(
        "ix_opportunities_converted_customer_id",
        "opportunities",
        ["converted_customer_id"],
        postgresql_where=sa.text("is_deleted = false"),
    )
    op.create_index("ix_opportunities_business_id", "opportunities", ["business_id"])
    op.create_index("ix_opportunities_status", "opportunities", ["status"])
    op.create_index("ix_opportunities_is_deleted", "opportunities", ["is_deleted"])


def downgrade() -> None:
    op.drop_index("ix_opportunities_is_deleted", table_name="opportunities")
    op.drop_index("ix_opportunities_status", table_name="opportunities")
    op.drop_index("ix_opportunities_business_id", table_name="opportunities")
    op.drop_index("ix_opportunities_converted_customer_id", table_name="opportunities")
    op.drop_index("ix_opportunities_customer_id", table_name="opportunities")
    op.drop_index("ix_opportunities_lead_id", table_name="opportunities")
    op.drop_index("ix_opportunities_business_status_created", table_name="opportunities")
    op.drop_table("opportunities")
