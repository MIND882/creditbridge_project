I've generated a new `app/crm/opportunity/` domain package for CreditBridge
(FastAPI + SQLAlchemy 2.0 + Alembic). Before placing these files, VERIFY the
following against the actual repo — do not guess, read the real files.

## Step 1 — Verify these against the real code

1. Run `alembic heads` inside `backend/`. Confirm the current head revision
   is `d4a7f1c9e2b1` (add_customers — this should already be applied since
   the Customer migration succeeded). If the head is different, tell me
   the actual value so I can fix `down_revision` in the new Opportunity
   migration (currently set to `d4a7f1c9e2b1`).

2. Find the actual Lead repository file. I assumed the import path is
   `app.crm.repositories.lead_repository.LeadRepository`, but based on the
   project's folder structure (`crm/lead/repositories/...`), it's more
   likely `app.crm.lead.repositories.lead_repository.LeadRepository`.
   Locate the real file and tell me:
   - the exact import path
   - the exact class name
   - whether it has a `get_by_id(lead_id, business_id)` method with that
     exact signature (or something equivalent) — if the method name/args
     differ, show me the actual signature so I can adjust
     `opportunity_service.py`.

3. Confirm `app/db/session.py` uses a **synchronous** `Session` (not
   `AsyncSession`). I've written the Opportunity repository/service/api as
   synchronous, matching the Customer domain (which was already placed and
   migrated successfully) — if Customer's files ended up async after your
   earlier corrections, Opportunity needs to match that, so check how
   `app/customers/repositories/customer_repository.py` actually looks
   RIGHT NOW in the repo (not what I originally gave you) and match its
   sync/async style exactly.

4. Confirm the exact dependency names and import paths currently used in
   `app/customers/api/customer.py` for `get_current_business_id`,
   `get_current_user_id`, and `get_db` — use the SAME ones in
   `opportunity/api/opportunity.py`, since those were already corrected
   once for the Customer domain and should be consistent.

5. Confirm `app/customers/models/customer.py` and
   `app/customers/services/customer_service.py` exist in the repo exactly
   as placed earlier (table name `customers`, methods `get_customer()` and
   `get_or_create_from_opportunity()`). If `get_or_create_from_opportunity`
   doesn't exist or has a different signature, show me what's actually
   there so I can fix the call in `opportunity_service.py`.

## Step 2 — Fix and place the files

For each of the 6 files I paste below:
- Correct any import paths, dependency names, or method signatures based
  on what you found in Step 1.
- If Customer's actual files turned out to be async, convert Opportunity's
  repository/service/api to async too (`async def`, `await db.execute(...)`,
  etc.) for consistency.
- Place each file at its correct path:
  - `app/crm/opportunity/models/opportunity.py`
  - `app/crm/opportunity/schemas/opportunity.py`
  - `app/crm/opportunity/repositories/opportunity_repository.py`
  - `app/crm/opportunity/services/opportunity_service.py`
  - `app/crm/opportunity/api/opportunity.py`
  - `app/db/migrations/versions/e5b8g2d0f3c2_add_opportunities.py`
- Create empty `__init__.py` files in `app/crm/opportunity/`,
  `app/crm/opportunity/models/`, `app/crm/opportunity/schemas/`,
  `app/crm/opportunity/repositories/`, `app/crm/opportunity/services/`,
  `app/crm/opportunity/api/` if they don't already exist.
- Register the new router in `app/main.py`, the same way the Customer
  router was registered. Show me the diff.

## Step 3 — Do NOT do these things

- Do NOT modify `app/customers/` — treat it as already correct and stable.
  If something there genuinely looks broken relative to what Opportunity
  needs, tell me instead of silently changing it.
- Do NOT create Quotation models — that's a separate future step.
- Do NOT run the migration yet — place the file and give me the exact
  `alembic upgrade head` command to run manually so I can review the SQL
  plan first (`alembic upgrade head --sql` if you want to show me the
  generated SQL without applying it).
- Do NOT change the field list, the `converted_customer_id` vs
  `customer_id` distinction, the CHECK constraint, or business logic in
  these files — only fix things objectively wrong per Step 1 (paths,
  names, signatures, sync/async).
- Pay special attention to the CHECK constraint
  `ck_opportunity_exactly_one_party` on `lead_id` / `customer_id` — do NOT
  let `converted_customer_id` get pulled into that constraint anywhere,
  it's intentionally separate (origin vs outcome, explained in the model's
  docstring).

## Step 4 — Report back

- What assumptions were correct
- What you had to fix, and why (especially the LeadRepository import path
  — that's the one I'm least sure about)
- Whether Customer's files were sync or async, and whether you had to
  convert Opportunity to match
- The exact migration command to run

---

"""add opportunities table

Revision ID: e5b8g2d0f3c2
Revises: d4a7f1c9e2b1
Create Date: 2026-08-04

IMPORTANT: Verify `down_revision` matches your actual current head
(`alembic heads`) before running — this assumes d4a7f1c9e2b1_add_customers
is the latest migration applied (i.e. Customer migration ran successfully,
as confirmed).
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "e5b8g2d0f3c2"
down_revision: Union[str, None] = "d4a7f1c9e2b1"  # <- VERIFY against `alembic heads`
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

# app/crm/opportunity/models/opportunity.py

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

Items/line-items are intentionally NOT modeled here (see whiteboard note:
"Inventory hoga future me, so packed item / product bundle" — deferred).
AI-derived insights (win-probability suggestions, lost-reason clustering)
are NOT stored on this model — they will be versioned in a future
`OpportunityAIInsight` table, following the same pattern as
`LeadAIInsight` and the deferred `CustomerAIInsight`.
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
    probability: Mapped[Optional[int]] = mapped_column(
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

    # ── Notes ─────────────────────────────────────────────────────────────
    # AI-generated insights (win-probability suggestions, lost-reason
    # pattern clustering) are NOT stored directly on this model. They will
    # be versioned in a future `OpportunityAIInsight` table, following the
    # same pattern as `LeadAIInsight`.
    #
    # Line items / product bundles are deliberately out of scope for this
    # MVP model (per whiteboard: "Inventory hoga future me, so packed
    # item / product bundle"). If item-level quoting is needed later, add
    # an `OpportunityItem` child table rather than retrofitting this model.

# app/crm/opportunity/schemas/opportunity.py

"""
Pydantic schemas for the Opportunity domain.

Validation mirrors `app.crm.opportunity.models.opportunity.Opportunity`.
The lead_id/customer_id exactly-one rule is validated here at the API
boundary too (not just relying on the DB CHECK constraint) so that client
requests get a clean 422 instead of a raw DB integrity error.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class OpportunityStatus(str, Enum):
    OPEN = "open"
    QUOTATION_SENT = "quotation_sent"
    WON = "won"
    LOST = "lost"
    CLOSED = "closed"


class OpportunitySalesStage(str, Enum):
    PROSPECTING = "prospecting"
    QUALIFICATION = "qualification"
    NEEDS_ANALYSIS = "needs_analysis"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"


# ── Create payload ───────────────────────────────────────────────────────────
class OpportunityCreatePayload(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)

    lead_id: Optional[uuid.UUID] = None
    customer_id: Optional[uuid.UUID] = None

    opportunity_amount: Optional[Decimal] = Field(None, ge=0)
    currency: str = Field("INR", min_length=3, max_length=3)

    sales_stage: OpportunitySalesStage = OpportunitySalesStage.PROSPECTING
    probability: Optional[Decimal] = Field(None, ge=0, le=100)
    expected_closing_date: Optional[date] = None
    opportunity_owner_id: Optional[uuid.UUID] = None

    @model_validator(mode="after")
    def validate_exactly_one_party(self) -> "OpportunityCreatePayload":
        has_lead = self.lead_id is not None
        has_customer = self.customer_id is not None
        if has_lead == has_customer:  # both True or both False
            raise ValueError(
                "Exactly one of lead_id or customer_id must be provided, not both or neither."
            )
        return self


# ── Update payload ───────────────────────────────────────────────────────────
class OpportunityUpdatePayload(BaseModel):
    """
    Partial update. Note: lead_id / customer_id are intentionally NOT
    editable after creation — an Opportunity's origin shouldn't change
    once set. If that's ever needed, add an explicit
    `reassign_party()` service method rather than allowing it via PATCH.
    """

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    opportunity_amount: Optional[Decimal] = Field(None, ge=0)
    status: Optional[OpportunityStatus] = None
    sales_stage: Optional[OpportunitySalesStage] = None
    probability: Optional[Decimal] = Field(None, ge=0, le=100)
    expected_closing_date: Optional[date] = None
    opportunity_owner_id: Optional[uuid.UUID] = None


# ── Lost payload ─────────────────────────────────────────────────────────────
class OpportunityMarkLostPayload(BaseModel):
    lost_reason: str = Field(..., min_length=1)
    competitor: Optional[str] = Field(None, max_length=255)


# ── Convert-to-Customer payload ───────────────────────────────────────────────
class OpportunityConvertToCustomerPayload(BaseModel):
    """Used by the 'Skip Quotation, Convert to Customer' whiteboard path."""

    company_name: str = Field(..., min_length=1, max_length=255)
    contact_name: Optional[str] = Field(None, max_length=255)
    contact_email: Optional[str] = Field(None, max_length=255)
    contact_phone: Optional[str] = Field(None, max_length=15)


# ── Response schemas ─────────────────────────────────────────────────────────
class OpportunityListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    lead_id: Optional[uuid.UUID]
    customer_id: Optional[uuid.UUID]
    opportunity_amount: Optional[Decimal]
    currency: str
    status: OpportunityStatus
    sales_stage: Optional[OpportunitySalesStage]
    probability: Optional[Decimal]
    expected_closing_date: Optional[date]
    created_at: datetime


class OpportunityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    business_id: uuid.UUID
    lead_id: Optional[uuid.UUID]
    customer_id: Optional[uuid.UUID]
    converted_customer_id: Optional[uuid.UUID]

    title: str
    opportunity_amount: Optional[Decimal]
    currency: str

    status: OpportunityStatus
    sales_stage: Optional[OpportunitySalesStage]
    probability: Optional[Decimal]
    expected_closing_date: Optional[date]
    opportunity_owner_id: Optional[uuid.UUID]

    lost_reason: Optional[str]
    competitor: Optional[str]

    created_at: datetime
    updated_at: Optional[datetime]


class OpportunityListResponse(BaseModel):
    items: list[OpportunityListItem]
    total: int
    page: int
    page_size: int

# app/crm/opportunity/repositories/opportunity_repository.py

"""
Repository for Opportunity data access.

Pure data-access layer — no business logic. ASSUMPTION: synchronous
SQLAlchemy `Session`, matching the convention used in the Customer
repository (verify against `app/db/session.py` before use; convert to
async if the project actually uses `AsyncSession`).
"""

import uuid
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.crm.opportunity.models.opportunity import Opportunity, OpportunityStatus


class OpportunityRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, opportunity: Opportunity) -> Opportunity:
        self.db.add(opportunity)
        self.db.flush()
        return opportunity

    def get_by_id(
        self, opportunity_id: uuid.UUID, business_id: uuid.UUID
    ) -> Optional[Opportunity]:
        stmt = select(Opportunity).where(
            Opportunity.id == opportunity_id,
            Opportunity.business_id == business_id,
            Opportunity.is_deleted.is_(False),
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def list_by_lead(
        self, lead_id: uuid.UUID, business_id: uuid.UUID
    ) -> list[Opportunity]:
        stmt = select(Opportunity).where(
            Opportunity.lead_id == lead_id,
            Opportunity.business_id == business_id,
            Opportunity.is_deleted.is_(False),
        )
        return list(self.db.execute(stmt).scalars().all())

    def list_by_customer(
        self, customer_id: uuid.UUID, business_id: uuid.UUID
    ) -> list[Opportunity]:
        stmt = select(Opportunity).where(
            Opportunity.customer_id == customer_id,
            Opportunity.business_id == business_id,
            Opportunity.is_deleted.is_(False),
        )
        return list(self.db.execute(stmt).scalars().all())

    def list_by_business(
        self,
        business_id: uuid.UUID,
        *,
        status: Optional[OpportunityStatus] = None,
        page: int = 1,
        page_size: int = 25,
    ) -> tuple[list[Opportunity], int]:
        filters = [
            Opportunity.business_id == business_id,
            Opportunity.is_deleted.is_(False),
        ]
        if status is not None:
            filters.append(Opportunity.status == status)

        count_stmt = select(func.count()).select_from(Opportunity).where(*filters)
        total = self.db.execute(count_stmt).scalar_one()

        stmt = (
            select(Opportunity)
            .where(*filters)
            .order_by(Opportunity.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        items = list(self.db.execute(stmt).scalars().all())
        return items, total

    def list_open_stale(
        self, business_id: uuid.UUID, stale_since
    ) -> list[Opportunity]:
        """
        Used by the auto-close scheduled job (service layer) — returns
        Opportunities in a non-terminal status that haven't been updated
        since `stale_since`. Mirrors ERPNext's `auto_close_opportunity`.
        """
        stmt = select(Opportunity).where(
            Opportunity.business_id == business_id,
            Opportunity.status == OpportunityStatus.OPEN,
            Opportunity.updated_at < stale_since,
            Opportunity.is_deleted.is_(False),
        )
        return list(self.db.execute(stmt).scalars().all())

    def update(self, opportunity: Opportunity) -> Opportunity:
        self.db.add(opportunity)
        self.db.flush()
        return opportunity

    def soft_delete(self, opportunity: Opportunity) -> Opportunity:
        opportunity.is_deleted = True
        opportunity.deleted_at = func.now()
        self.db.add(opportunity)
        self.db.flush()
        return opportunity

# app/crm/opportunity/services/opportunity_service.py

"""
Business logic for the Opportunity domain.

Dependency direction: this service MAY import from `app.customers`
(Customer is a core entity that CRM depends on) and from other `app.crm`
submodules (e.g. Lead repository, to validate lead_id on creation). It
must NEVER be imported BY `app.customers` — that would invert the
dependency direction we established.
"""

import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, status

from app.crm.opportunity.models.opportunity import Opportunity, OpportunityStatus
from app.crm.opportunity.repositories.opportunity_repository import OpportunityRepository
from app.crm.opportunity.schemas.opportunity import (
    OpportunityCreatePayload,
    OpportunityMarkLostPayload,
    OpportunityUpdatePayload,
)
from app.customers.models.customer import Customer
from app.customers.services.customer_service import CustomerService

# ASSUMPTION: adjust this import to match the actual Lead repository path/name.
from app.crm.repositories.lead_repository import LeadRepository


class OpportunityService:
    def __init__(
        self,
        repository: OpportunityRepository,
        customer_service: CustomerService,
        lead_repository: LeadRepository,
    ):
        self.repository = repository
        self.customer_service = customer_service
        self.lead_repository = lead_repository

    # ── Standard CRUD ────────────────────────────────────────────────────

    def create_opportunity(
        self,
        payload: OpportunityCreatePayload,
        business_id: uuid.UUID,
        created_by: uuid.UUID,
    ) -> Opportunity:
        # Validate the referenced party actually exists in this tenant
        # before insert — gives a clean 404 instead of a raw FK violation.
        if payload.lead_id is not None:
            lead = self.lead_repository.get_by_id(payload.lead_id, business_id)
            if lead is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Referenced lead not found.",
                )
        if payload.customer_id is not None:
            self.customer_service.get_customer(payload.customer_id, business_id)
            # raises 404 internally if not found

        opportunity = Opportunity(
            business_id=business_id,
            lead_id=payload.lead_id,
            customer_id=payload.customer_id,
            title=payload.title,
            opportunity_amount=payload.opportunity_amount,
            currency=payload.currency,
            status=OpportunityStatus.OPEN,
            sales_stage=payload.sales_stage,
            probability=payload.probability,
            expected_closing_date=payload.expected_closing_date,
            opportunity_owner_id=payload.opportunity_owner_id,
            created_by=created_by,
        )
        return self.repository.create(opportunity)

    def get_opportunity(
        self, opportunity_id: uuid.UUID, business_id: uuid.UUID
    ) -> Opportunity:
        opportunity = self.repository.get_by_id(opportunity_id, business_id)
        if opportunity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Opportunity not found."
            )
        return opportunity

    def list_opportunities(
        self,
        business_id: uuid.UUID,
        *,
        status_filter: Optional[OpportunityStatus] = None,
        page: int = 1,
        page_size: int = 25,
    ) -> tuple[list[Opportunity], int]:
        return self.repository.list_by_business(
            business_id, status=status_filter, page=page, page_size=page_size
        )

    def update_opportunity(
        self,
        opportunity_id: uuid.UUID,
        business_id: uuid.UUID,
        payload: OpportunityUpdatePayload,
        updated_by: uuid.UUID,
    ) -> Opportunity:
        opportunity = self.get_opportunity(opportunity_id, business_id)

        if opportunity.status == OpportunityStatus.LOST:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot update a Lost opportunity. Reopen it first if needed.",
            )

        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(opportunity, field, value)
        opportunity.updated_by = updated_by

        return self.repository.update(opportunity)

    def delete_opportunity(self, opportunity_id: uuid.UUID, business_id: uuid.UUID) -> None:
        opportunity = self.get_opportunity(opportunity_id, business_id)
        self.repository.soft_delete(opportunity)

    # ── Lost tracking ─────────────────────────────────────────────────────

    def mark_lost(
        self,
        opportunity_id: uuid.UUID,
        business_id: uuid.UUID,
        payload: OpportunityMarkLostPayload,
        updated_by: uuid.UUID,
    ) -> Opportunity:
        """
        Mirrors ERPNext's `declare_enquiry_lost`. ERPNext blocks this if an
        active Quotation exists (`has_active_quotation()`) — that gate is
        NOT implemented yet because the Quotation table doesn't exist in
        this codebase yet. TODO: once Quotation is built, add the same
        guard here before allowing status = LOST.
        """
        opportunity = self.get_opportunity(opportunity_id, business_id)

        # TODO(quotation-dependency): block this if an active Quotation
        # exists for this opportunity, once app.crm.quotation exists.

        opportunity.status = OpportunityStatus.LOST
        opportunity.lost_reason = payload.lost_reason
        opportunity.competitor = payload.competitor
        opportunity.updated_by = updated_by

        return self.repository.update(opportunity)

    def reopen(self, opportunity_id: uuid.UUID, business_id: uuid.UUID) -> Opportunity:
        opportunity = self.get_opportunity(opportunity_id, business_id)
        opportunity.status = OpportunityStatus.OPEN
        opportunity.lost_reason = None
        opportunity.competitor = None
        return self.repository.update(opportunity)

    # ── Auto-close scheduled job ────────────────────────────────────────
    # Mirrors ERPNext's auto_close_opportunity() background job. Wire this
    # up to your existing scheduler (Redis/Celery/APScheduler — whichever
    # this project already uses for the AI agent pipeline) rather than
    # calling it inline anywhere in request-handling code.

    def auto_close_stale_opportunities(
        self, business_id: uuid.UUID, stale_after_days: int = 15
    ) -> int:
        stale_since = datetime.now(timezone.utc) - timedelta(days=stale_after_days)
        stale_opportunities = self.repository.list_open_stale(business_id, stale_since)
        for opp in stale_opportunities:
            opp.status = OpportunityStatus.CLOSED
            self.repository.update(opp)
        return len(stale_opportunities)

    # ── Conversion to Customer ──────────────────────────────────────────
    # Skip-Quotation path: "Opportunity -> Skip Quotation, Convert to
    # Customer" from the whiteboard flow. The full Lead -> Opportunity ->
    # Quotation -> Customer path will call CustomerService.
    # get_or_create_from_quotation() instead, once Quotation exists.

    def convert_to_customer(
        self,
        opportunity_id: uuid.UUID,
        business_id: uuid.UUID,
        *,
        company_name: str,
        contact_name: Optional[str],
        contact_email: Optional[str],
        contact_phone: Optional[str],
        created_by: uuid.UUID,
    ) -> Customer:
        opportunity = self.get_opportunity(opportunity_id, business_id)

        if opportunity.customer_id is not None:
            # This Opportunity originated FROM an existing Customer already
            # — nothing to convert, it's already tied to a Customer.
            return self.customer_service.get_customer(opportunity.customer_id, business_id)

        if opportunity.converted_customer_id is not None:
            # Already converted previously — idempotent return.
            return self.customer_service.get_customer(
                opportunity.converted_customer_id, business_id
            )

        customer = self.customer_service.get_or_create_from_opportunity(
            business_id=business_id,
            opportunity_id=opportunity.id,
            lead_id=opportunity.lead_id,
            company_name=company_name,
            contact_name=contact_name,
            contact_email=contact_email,
            contact_phone=contact_phone,
            created_by=created_by,
        )

        opportunity.status = OpportunityStatus.WON
        # IMPORTANT: set converted_customer_id (outcome), NOT customer_id
        # (origin) — setting customer_id here would violate the
        # ck_opportunity_exactly_one_party CHECK constraint whenever this
        # Opportunity originated from a Lead (lead_id already set).
        opportunity.converted_customer_id = customer.id
        self.repository.update(opportunity)

        return customer

# app/crm/opportunity/api/opportunity.py

"""
Opportunity API routes.

Same assumptions as the Customer API file — verify `get_current_business_id`,
`get_current_user_id`, and `get_db` import paths against the actual
`app/utils/auth_dependency.py` and `app/db/session.py` before running.
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.crm.opportunity.models.opportunity import OpportunityStatus
from app.crm.opportunity.repositories.opportunity_repository import OpportunityRepository
from app.crm.opportunity.schemas.opportunity import (
    OpportunityConvertToCustomerPayload,
    OpportunityCreatePayload,
    OpportunityListResponse,
    OpportunityMarkLostPayload,
    OpportunityResponse,
    OpportunityUpdatePayload,
)
from app.crm.opportunity.services.opportunity_service import OpportunityService
from app.crm.repositories.lead_repository import LeadRepository  # ASSUMPTION: verify path
from app.customers.repositories.customer_repository import CustomerRepository
from app.customers.schemas.customer import CustomerResponse
from app.customers.services.customer_service import CustomerService
from app.db.session import get_db
from app.utils.auth_dependency import get_current_business_id, get_current_user_id

router = APIRouter(prefix="/api/v1/opportunities", tags=["opportunities"])


def get_opportunity_service(db: Session = Depends(get_db)) -> OpportunityService:
    customer_service = CustomerService(CustomerRepository(db))
    lead_repository = LeadRepository(db)
    return OpportunityService(
        OpportunityRepository(db), customer_service, lead_repository
    )


@router.post("", response_model=OpportunityResponse, status_code=status.HTTP_201_CREATED)
def create_opportunity(
    payload: OpportunityCreatePayload,
    business_id: uuid.UUID = Depends(get_current_business_id),
    user_id: uuid.UUID = Depends(get_current_user_id),
    service: OpportunityService = Depends(get_opportunity_service),
):
    return service.create_opportunity(payload, business_id, created_by=user_id)


@router.get("", response_model=OpportunityListResponse)
def list_opportunities(
    status_filter: Optional[OpportunityStatus] = Query(None, alias="status"),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    business_id: uuid.UUID = Depends(get_current_business_id),
    service: OpportunityService = Depends(get_opportunity_service),
):
    items, total = service.list_opportunities(
        business_id, status_filter=status_filter, page=page, page_size=page_size
    )
    return OpportunityListResponse(items=items, total=total, page=page, page_size=page_size)


@router.get("/{opportunity_id}", response_model=OpportunityResponse)
def get_opportunity(
    opportunity_id: uuid.UUID,
    business_id: uuid.UUID = Depends(get_current_business_id),
    service: OpportunityService = Depends(get_opportunity_service),
):
    return service.get_opportunity(opportunity_id, business_id)


@router.patch("/{opportunity_id}", response_model=OpportunityResponse)
def update_opportunity(
    opportunity_id: uuid.UUID,
    payload: OpportunityUpdatePayload,
    business_id: uuid.UUID = Depends(get_current_business_id),
    user_id: uuid.UUID = Depends(get_current_user_id),
    service: OpportunityService = Depends(get_opportunity_service),
):
    return service.update_opportunity(opportunity_id, business_id, payload, updated_by=user_id)


@router.post("/{opportunity_id}/mark-lost", response_model=OpportunityResponse)
def mark_opportunity_lost(
    opportunity_id: uuid.UUID,
    payload: OpportunityMarkLostPayload,
    business_id: uuid.UUID = Depends(get_current_business_id),
    user_id: uuid.UUID = Depends(get_current_user_id),
    service: OpportunityService = Depends(get_opportunity_service),
):
    return service.mark_lost(opportunity_id, business_id, payload, updated_by=user_id)


@router.post("/{opportunity_id}/reopen", response_model=OpportunityResponse)
def reopen_opportunity(
    opportunity_id: uuid.UUID,
    business_id: uuid.UUID = Depends(get_current_business_id),
    service: OpportunityService = Depends(get_opportunity_service),
):
    return service.reopen(opportunity_id, business_id)


@router.post(
    "/{opportunity_id}/convert-to-customer",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def convert_opportunity_to_customer(
    opportunity_id: uuid.UUID,
    payload: OpportunityConvertToCustomerPayload,
    business_id: uuid.UUID = Depends(get_current_business_id),
    user_id: uuid.UUID = Depends(get_current_user_id),
    service: OpportunityService = Depends(get_opportunity_service),
):
    """Implements the whiteboard's "Skip Quotation, Convert to Customer" path."""
    return service.convert_to_customer(
        opportunity_id,
        business_id,
        company_name=payload.company_name,
        contact_name=payload.contact_name,
        contact_email=payload.contact_email,
        contact_phone=payload.contact_phone,
        created_by=user_id,
    )


@router.delete("/{opportunity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_opportunity(
    opportunity_id: uuid.UUID,
    business_id: uuid.UUID = Depends(get_current_business_id),
    service: OpportunityService = Depends(get_opportunity_service),
):
    service.delete_opportunity(opportunity_id, business_id)
