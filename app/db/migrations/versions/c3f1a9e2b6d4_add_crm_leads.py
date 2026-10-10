"""add_leads_module

Revision ID: c3f1a9e2b6d4
Revises: 90be1b37cdb0
Create Date: 2026-05-05 10:00:00.000000

Creates the Lead CRM module:
  - leads
  - lead_activities
  - lead_attachments
  - lead_ai_insights

Enum columns are stored as VARCHAR + CHECK constraint (native_enum=False
in the ORM layer), matching CreditBridge's existing convention (see
Invoice.status, RiskScore.grade) to avoid Postgres ALTER TYPE migrations
whenever an enum value is added.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c3f1a9e2b6d4'
down_revision: Union[str, Sequence[str], None] = '90be1b37cdb0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # ────────────────────────────────────────────────────────────────
    # leads
    # ────────────────────────────────────────────────────────────────
    op.create_table(
        'leads',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),

        # Tenancy
        sa.Column('business_id', postgresql.UUID(as_uuid=True), nullable=False),

        # Ownership (no FK yet -- see model docstring, upgraded later
        # once staff-user/RBAC tables exist)
        sa.Column('lead_owner_id', postgresql.UUID(as_uuid=True), nullable=True),

        # Identity
        sa.Column('first_name', sa.String(length=100), nullable=True),
        sa.Column('middle_name', sa.String(length=100), nullable=True),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('lead_name', sa.String(length=255), nullable=False),
        sa.Column('company_name', sa.String(length=255), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('gender', sa.String(length=20), nullable=True),

        # Contact channels
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=15), nullable=True),
        sa.Column('mobile_no', sa.String(length=15), nullable=True),
        sa.Column('whatsapp_no', sa.String(length=15), nullable=True),
        sa.Column('website', sa.String(length=255), nullable=True),

        # Location
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('state', sa.String(length=100), nullable=True),
        sa.Column('country', sa.String(length=100), nullable=True, server_default='India'),

        # Organization
        sa.Column('industry', sa.String(length=100), nullable=True),
        sa.Column('business_type', sa.String(length=50), nullable=True),
        sa.Column('no_of_employees', sa.String(length=20), nullable=True),
        sa.Column('declared_annual_revenue', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('job_title', sa.String(length=100), nullable=True),
        sa.Column('lead_type', sa.String(length=20), nullable=True),

        # Source / attribution
        sa.Column('source', sa.String(length=30), nullable=False, server_default='manual'),
        sa.Column('ca_partner_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('utm_source', sa.String(length=100), nullable=True),
        sa.Column('utm_medium', sa.String(length=100), nullable=True),
        sa.Column('utm_campaign', sa.String(length=100), nullable=True),
        sa.Column('utm_content', sa.String(length=100), nullable=True),

        # Lifecycle / status
        sa.Column('status', sa.String(length=20), nullable=False, server_default='Lead'),
        sa.Column('qualification_status', sa.String(length=20), nullable=False,
                  server_default='Unqualified'),
        sa.Column('qualified_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('qualified_on', sa.Date(), nullable=True),

        # Identity verification
        sa.Column('pan', sa.String(length=10), nullable=True),
        sa.Column('gstin', sa.String(length=15), nullable=True),
        sa.Column('kyc_precheck', postgresql.JSONB(astext_type=sa.Text()), nullable=True),

        # AI Layer: current-value cache
        sa.Column('ai_lead_score', sa.Integer(), nullable=True),
        sa.Column('last_ai_enriched_at', sa.DateTime(timezone=True), nullable=True),

        # Duplicate resolution
        sa.Column('duplicate_of_lead_id', postgresql.UUID(as_uuid=True), nullable=True),

        # Conversion target
        sa.Column('converted_opportunity_id', postgresql.UUID(as_uuid=True), nullable=True),

        # Flags
        sa.Column('unsubscribed', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('disabled', sa.Boolean(), nullable=False, server_default=sa.false()),

        # Denormalized counters
        sa.Column('notes_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('attachment_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('last_activity_at', sa.DateTime(timezone=True), nullable=True),

        # Soft delete
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),

        # Audit
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),

        # Constraints
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['ca_partner_id'], ['ca_partners.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['duplicate_of_lead_id'], ['leads.id'], ondelete='SET NULL'),
        sa.CheckConstraint(
            "lead_type IN ('Client', 'Channel Partner', 'Consultant')",
            name='ck_leads_lead_type',
        ),
        sa.CheckConstraint(
            "source IN ('manual', 'referral', 'cold_outreach', 'website', 'trade_event', "
            "'import', 'existing_customer', 'ca_partner')",
            name='ck_leads_source',
        ),
        sa.CheckConstraint(
            "status IN ('Lead', 'Open', 'Replied', 'Opportunity', 'Quotation', "
            "'Lost Quotation', 'Interested', 'Converted', 'Do Not Contact')",
            name='ck_leads_status',
        ),
        sa.CheckConstraint(
            "qualification_status IN ('Unqualified', 'In Process', 'Qualified')",
            name='ck_leads_qualification_status',
        ),
    )

    # Simple single/FK-column indexes
    op.create_index('ix_leads_business_id', 'leads', ['business_id'])
    op.create_index('ix_leads_lead_owner_id', 'leads', ['lead_owner_id'])
    op.create_index('ix_leads_email', 'leads', ['email'])
    op.create_index('ix_leads_mobile_no', 'leads', ['mobile_no'])
    op.create_index('ix_leads_status', 'leads', ['status'])
    op.create_index('ix_leads_is_deleted', 'leads', ['is_deleted'])

    # Composite + partial indexes, designed around actual API query
    # patterns (GET /v1/leads filters, staleness scan, pipeline summary)
    op.create_index(
        'ix_leads_business_status', 'leads', ['business_id', 'status'],
        postgresql_where=sa.text('is_deleted = false'),
    )
    op.create_index(
        'ix_leads_business_qualification', 'leads', ['business_id', 'qualification_status'],
        postgresql_where=sa.text('is_deleted = false'),
    )
    op.create_index(
        'ix_leads_business_source', 'leads', ['business_id', 'source'],
        postgresql_where=sa.text('is_deleted = false'),
    )
    op.create_index(
        'ix_leads_business_owner', 'leads', ['business_id', 'lead_owner_id'],
        postgresql_where=sa.text('is_deleted = false'),
    )
    op.create_index(
        'ix_leads_business_ca_partner', 'leads', ['business_id', 'ca_partner_id'],
        postgresql_where=sa.text('ca_partner_id IS NOT NULL'),
    )
    op.create_index('ix_leads_business_created', 'leads', ['business_id', 'created_at'])
    op.create_index('ix_leads_business_last_activity', 'leads', ['business_id', 'last_activity_at'])
    op.create_index(
        'ix_leads_business_ai_score', 'leads', ['business_id', 'ai_lead_score'],
        postgresql_where=sa.text('is_deleted = false'),
    )

    # ────────────────────────────────────────────────────────────────
    # lead_activities
    # ────────────────────────────────────────────────────────────────
    op.create_table(
        'lead_activities',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('lead_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('business_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('activity_type', sa.String(length=20), nullable=False),
        sa.Column('actor_type', sa.String(length=20), nullable=False, server_default='human'),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('next_action_due', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),

        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], ondelete='CASCADE'),
        sa.CheckConstraint(
            "activity_type IN ('call', 'note', 'whatsapp', 'email', 'status_change', 'ai_suggestion')",
            name='ck_lead_activities_activity_type',
        ),
        sa.CheckConstraint(
            "actor_type IN ('human', 'ai', 'system')",
            name='ck_lead_activities_actor_type',
        ),
    )

    op.create_index('ix_lead_activities_lead_id', 'lead_activities', ['lead_id'])
    op.create_index('ix_lead_activities_business_id', 'lead_activities', ['business_id'])
    op.create_index('ix_lead_activities_lead_created', 'lead_activities', ['lead_id', 'created_at'])
    op.create_index('ix_lead_activities_business_type', 'lead_activities', ['business_id', 'activity_type'])
    op.create_index('ix_lead_activities_business_actor', 'lead_activities', ['business_id', 'actor_type'])
    op.create_index(
        'ix_lead_activities_business_next_action', 'lead_activities',
        ['business_id', 'next_action_due'],
        postgresql_where=sa.text('next_action_due IS NOT NULL'),
    )

    # ────────────────────────────────────────────────────────────────
    # lead_attachments
    # ────────────────────────────────────────────────────────────────
    op.create_table(
        'lead_attachments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('lead_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('business_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('file_name', sa.String(length=255), nullable=False),
        sa.Column('file_type', sa.String(length=20), nullable=False),
        sa.Column('mime_type', sa.String(length=100), nullable=True),
        sa.Column('file_size_bytes', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(length=30), nullable=True),
        sa.Column('storage_url', sa.String(length=500), nullable=False),
        sa.Column('uploaded_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),

        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], ondelete='CASCADE'),
        sa.CheckConstraint(
            "file_type IN ('image', 'pdf', 'document', 'other')",
            name='ck_lead_attachments_file_type',
        ),
        sa.CheckConstraint(
            'file_size_bytes > 0',
            name='ck_lead_attachments_file_size_positive',
        ),
    )

    op.create_index('ix_lead_attachments_lead_id', 'lead_attachments', ['lead_id'])
    op.create_index('ix_lead_attachments_business_id', 'lead_attachments', ['business_id'])
    op.create_index('ix_lead_attachments_lead_created', 'lead_attachments', ['lead_id', 'created_at'])
    op.create_index('ix_lead_attachments_business_category', 'lead_attachments', ['business_id', 'category'])

    # ────────────────────────────────────────────────────────────────
    # lead_ai_insights
    # ────────────────────────────────────────────────────────────────
    op.create_table(
        'lead_ai_insights',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('lead_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('business_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('insight_type', sa.String(length=40), nullable=False),
        sa.Column('value', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('confidence_score', sa.Numeric(precision=4, scale=3), nullable=True),
        sa.Column('model_version', sa.String(length=50), nullable=True),
        sa.Column('superseded_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),

        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], ondelete='CASCADE'),
        sa.CheckConstraint(
            "insight_type IN ('lead_score', 'business_size_estimate', 'conversation_summary', "
            "'duplicate_suggestion', 'kyc_verification')",
            name='ck_lead_ai_insights_insight_type',
        ),
        sa.CheckConstraint(
            'confidence_score IS NULL OR (confidence_score >= 0 AND confidence_score <= 1)',
            name='ck_lead_ai_insights_confidence_range',
        ),
    )

    op.create_index('ix_lead_ai_insights_lead_id', 'lead_ai_insights', ['lead_id'])
    op.create_index('ix_lead_ai_insights_business_id', 'lead_ai_insights', ['business_id'])
    op.create_index(
        'ix_lead_ai_insights_lead_type_generated', 'lead_ai_insights',
        ['lead_id', 'insight_type', 'generated_at'],
    )
    op.create_index('ix_lead_ai_insights_business_type', 'lead_ai_insights', ['business_id', 'insight_type'])
    op.create_index(
        'ix_lead_ai_insights_current', 'lead_ai_insights',
        ['lead_id', 'insight_type'],
        postgresql_where=sa.text('superseded_at IS NULL'),
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Drop in strict reverse-dependency order.

    # lead_ai_insights
    op.drop_index('ix_lead_ai_insights_current', table_name='lead_ai_insights')
    op.drop_index('ix_lead_ai_insights_business_type', table_name='lead_ai_insights')
    op.drop_index('ix_lead_ai_insights_lead_type_generated', table_name='lead_ai_insights')
    op.drop_index('ix_lead_ai_insights_business_id', table_name='lead_ai_insights')
    op.drop_index('ix_lead_ai_insights_lead_id', table_name='lead_ai_insights')
    op.drop_table('lead_ai_insights')

    # lead_attachments
    op.drop_index('ix_lead_attachments_business_category', table_name='lead_attachments')
    op.drop_index('ix_lead_attachments_lead_created', table_name='lead_attachments')
    op.drop_index('ix_lead_attachments_business_id', table_name='lead_attachments')
    op.drop_index('ix_lead_attachments_lead_id', table_name='lead_attachments')
    op.drop_table('lead_attachments')

    # lead_activities
    op.drop_index('ix_lead_activities_business_next_action', table_name='lead_activities')
    op.drop_index('ix_lead_activities_business_actor', table_name='lead_activities')
    op.drop_index('ix_lead_activities_business_type', table_name='lead_activities')
    op.drop_index('ix_lead_activities_lead_created', table_name='lead_activities')
    op.drop_index('ix_lead_activities_business_id', table_name='lead_activities')
    op.drop_index('ix_lead_activities_lead_id', table_name='lead_activities')
    op.drop_table('lead_activities')

    # leads
    op.drop_index('ix_leads_business_ai_score', table_name='leads')
    op.drop_index('ix_leads_business_last_activity', table_name='leads')
    op.drop_index('ix_leads_business_created', table_name='leads')
    op.drop_index('ix_leads_business_ca_partner', table_name='leads')
    op.drop_index('ix_leads_business_owner', table_name='leads')
    op.drop_index('ix_leads_business_source', table_name='leads')
    op.drop_index('ix_leads_business_qualification', table_name='leads')
    op.drop_index('ix_leads_business_status', table_name='leads')
    op.drop_index('ix_leads_is_deleted', table_name='leads')
    op.drop_index('ix_leads_status', table_name='leads')
    op.drop_index('ix_leads_mobile_no', table_name='leads')
    op.drop_index('ix_leads_email', table_name='leads')
    op.drop_index('ix_leads_lead_owner_id', table_name='leads')
    op.drop_index('ix_leads_business_id', table_name='leads')
    op.drop_table('leads')