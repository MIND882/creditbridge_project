"""rename_lead_status_and_qualification_values

Revision ID: d7a2c4f8e1b9
Revises: c3f1a9e2b6d4
Create Date: 2026-08-21 00:00:00.000000

Renames LeadStatus / LeadQualificationStatus display values away from the
ERPNext-identical strings to CreditBridge's own vocabulary.

Both columns are VARCHAR + CHECK constraint (native_enum=False), per
CreditBridge's existing convention -- so this migration must do three
things together, in order:

  1. Drop the old CHECK constraints (ck_leads_status,
     ck_leads_qualification_status) -- otherwise step 2's UPDATE would
     violate them, since the new values aren't in the old allow-list yet.
  2. UPDATE existing rows from old values to new values.
  3. Add new CHECK constraints with the new allow-list, and update the
     column server_defaults ('Lead' -> 'New', 'Unqualified' ->
     'Not Qualified') so newly-inserted rows get the right default too.

Enum *member names* (LeadStatus.LEAD, .OPEN, etc.) are unchanged at the
Python/ORM level -- only the stored/displayed string values change, so no
code that references members (e.g. lead_service.py's
_ALLOWED_STATUS_TRANSITIONS) needs touching.

LeadActivity.activity_metadata / content history (e.g. "Status changed
from 'Lead' to 'Open'") is intentionally left as-is -- historical audit
record, not a live reference.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd7a2c4f8e1b9'
down_revision: Union[str, Sequence[str], None] = 'f6c9h3e1g4d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# (old_value, new_value) pairs -- applied to leads.status
_STATUS_RENAMES = [
    ("Lead", "New"),
    ("Open", "Contacted"),
    ("Replied", "Responded"),
    ("Opportunity", "In Discussion"),
    ("Quotation", "Proposal Sent"),
    ("Lost Quotation", "Proposal Lost"),
    ("Interested", "Warm"),
    ("Converted", "Won"),
    ("Do Not Contact", "Opted Out"),
]

# (old_value, new_value) pairs -- applied to leads.qualification_status
# ("Qualified" -> "Qualified" is unchanged, omitted -- no row update needed)
_QUALIFICATION_RENAMES = [
    ("Unqualified", "Not Qualified"),
    ("In Process", "Reviewing"),
]


def upgrade() -> None:
    # 1. Drop old CHECK constraints first -- the UPDATE below would
    #    violate them otherwise, since new values aren't in the old
    #    allow-list.
    op.drop_constraint('ck_leads_status', 'leads', type_='check')
    op.drop_constraint('ck_leads_qualification_status', 'leads', type_='check')

    # 2. Migrate existing row data.
    for old, new in _STATUS_RENAMES:
        op.execute(
            f"UPDATE leads SET status = '{new}' WHERE status = '{old}'"
        )
    for old, new in _QUALIFICATION_RENAMES:
        op.execute(
            f"UPDATE leads SET qualification_status = '{new}' "
            f"WHERE qualification_status = '{old}'"
        )

    # 3. Re-add CHECK constraints with the new allow-list.
    op.create_check_constraint(
        'ck_leads_status',
        'leads',
        "status IN ('New', 'Contacted', 'Responded', 'In Discussion', "
        "'Proposal Sent', 'Proposal Lost', 'Warm', 'Won', 'Opted Out')",
    )
    op.create_check_constraint(
        'ck_leads_qualification_status',
        'leads',
        "qualification_status IN ('Not Qualified', 'Reviewing', 'Qualified')",
    )

    # Update column server_defaults so newly-inserted rows (no explicit
    # status passed) get the new default value, matching
    # LeadStatus.LEAD's new .value in models/lead.py.
    op.alter_column('leads', 'status', server_default='New')
    op.alter_column('leads', 'qualification_status', server_default='Not Qualified')


def downgrade() -> None:
    # Reverse order: drop new constraints, revert defaults, revert data,
    # restore old constraints.
    op.drop_constraint('ck_leads_status', 'leads', type_='check')
    op.drop_constraint('ck_leads_qualification_status', 'leads', type_='check')

    op.alter_column('leads', 'status', server_default='Lead')
    op.alter_column('leads', 'qualification_status', server_default='Unqualified')

    for old, new in _STATUS_RENAMES:
        op.execute(
            f"UPDATE leads SET status = '{old}' WHERE status = '{new}'"
        )
    for old, new in _QUALIFICATION_RENAMES:
        op.execute(
            f"UPDATE leads SET qualification_status = '{old}' "
            f"WHERE qualification_status = '{new}'"
        )

    op.create_check_constraint(
        'ck_leads_status',
        'leads',
        "status IN ('Lead', 'Open', 'Replied', 'Opportunity', 'Quotation', "
        "'Lost Quotation', 'Interested', 'Converted', 'Do Not Contact')",
    )
    op.create_check_constraint(
        'ck_leads_qualification_status',
        'leads',
        "qualification_status IN ('Unqualified', 'In Process', 'Qualified')",
    )