"""
backend/app/model/lead.py

 ye file CreditBridge ka CRM ka lead module define karti hai.

 Isme 4 models hain:
 
 - Lead
 - LeadActivity
 - LeadAttachment
 - LeadAIInsight

 Humne ERPNext ka business workflow follow kiya hai:

    Lead
    ↓
    Opportunity
    ↓
    Quotation
    ↓
    Customer
    ↓
    Sales Order
    ↓
    Invoice
    ↓
    Payment

Lekin implementation Fastapi + SQLALchemy architecture me likha gya hai.

Is file me sirf Database Models Hain.

Isme Repository, Service, Schema ya  API ka CODE nhi hai.

Stage 1 ke baad ye improvement kiya gaye hai:

1. LeadAIInsight add kiya.
 Isme AI saare Historical record save honge
 jaise:
 - LEAD SCORE HISTORY
 - BUSINESS  SIZE ESTIMATE
 - CONVERSATION SUMMARY

 Lead table me sirf current AI data RAHEGA :
 - AI_LEAD_SCORE
 - KYC_PRECHECK
 - LAST_AI_ENRICHED_AT

2. LeadActivity me actor_type add kiya.

   Ab hame pata chalega activity kisne ki:

   - Human
   - AI
   - System

   Aur activity_type alag batayega ki activity kya thi.

3. Database indexes ko real API queries ke hisaab se optimize kiya gaya hai.

   Sirf Foreign Keys ke basis par nahi.

4. lead_score ka naam badal kar ai_lead_score rakha gaya.

   Taaki future me:

   - AI Lead Score
   - Business Health Score
   - Credit Score

   ke beech confusion na ho.

   AI Insight me confidence_score use kiya gaya hai.

"""
import enum
import uuid

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,  
)
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base

class LeadStatus(str, enum.Enum):
    LEAD = "New"
    OPEN = "Contacted"
    REPLIED = "Responded"
    OPPORTUNITY = "In Discussion"
    QUOTATION = "Proposal Sent"
    LOST_QUOTATION = "Proposal Lost"
    INTERESTED = "Warm"
    CONVERTED = "Won"
    DO_NOT_CONTACT = "Opted Out"

class LeadQualificationStatus(str, enum.Enum):
    UNQUALIFIED = "Not Qualified"
    IN_PROCESS = "Reviewing"
    QUALIFIED = "Qualified"

class LeadType(str, enum.Enum):
    CLIENT = "Client"
    CHANNEL_PARTNER = "Channel Partner"
    CONSULTANT = "Consultant"

class LeadSource(str, enum.Enum):
    MANUAL = "manual"
    REFERRAL = "referral"
    COLD_OUTREACH = "cold_outreach"
    WEBSITE = "website"
    TRADE_EVENT = "trade_event"
    IMPORT = "import"
    EXISTING_CUSTOMER = "existing_customer"
    CA_PARTNER = "ca_partner"

class LeadActivityType(str, enum.Enum):
    CALL = "call"
    NOTE = "note"
    WHATSAPP = "whatsapp"
    EMAIL = "email"
    STATUS_CHANGE = "status_change"
    AI_SUGGESTION = "ai_suggestion"


class LeadActivityActorType(str, enum.Enum):
    """
    Orthogonal to LeadActivityType. Answers "who/what generated this
    entry" independent of "what kind of entry it is" -- avoids a
    combinatorial explosion of the activity_type enum (e.g. no need for
    separate ai_status_change / system_status_change / human_status_change
    values).
    """
    HUMAN = "human"
    AI = "ai"
    SYSTEM = "system"


class LeadAttachmentFileType(str, enum.Enum):
    IMAGE = "image"
    PDF = "pdf"
    DOCUMENT = "document"
    OTHER = "other"


class LeadAIInsightType(str, enum.Enum):
    """
    Discriminates the shape of LeadAIInsight.value (JSONB) and which
    recurring agent produced it. See lead_pipeline.py agent set.
    """
    LEAD_SCORE = "lead_score"                    # ai_lead_score snapshot + reasoning
    BUSINESS_SIZE_ESTIMATE = "business_size_estimate"
    CONVERSATION_SUMMARY = "conversation_summary"
    DUPLICATE_SUGGESTION = "duplicate_suggestion"
    KYC_VERIFICATION = "kyc_verification"


# ─────────────────────────────────────────────────────────────────────────────
# Lead
# ─────────────────────────────────────────────────────────────────────────────

class Lead(Base):
    """
    A prospective customer belonging to an MSME's own sales pipeline.

    Tenant-scoped via business_id: this is the MSME's own CRM record
    (e.g. Sharma Textiles' prospective fabric buyer), NOT a CreditBridge
    borrower-acquisition lead. See frozen architecture spec.
    """
    __tablename__ = "leads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # ── Tenancy ──────────────────────────────────────────────────────────
    business_id = Column(
        UUID(as_uuid=True),
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Ownership (staff assignment) ────────────────────────────────────
    # Intentionally NOT a ForeignKey yet. NULL = owned by the business
    # account itself (today's single-owner reality). Becomes an enforced
    # FK once staff-user/RBAC tables exist -- additive migration, no
    # schema break.
    lead_owner_id = Column(UUID(as_uuid=True), nullable=True, index=True)

    # ── Identity ─────────────────────────────────────────────────────────
    first_name = Column(String(100), nullable=True)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    lead_name = Column(String(255), nullable=False)  # server-computed cascade
    company_name = Column(String(255), nullable=True)
    title = Column(String(255), nullable=True)
    gender = Column(String(20), nullable=True)

    # ── Contact channels ─────────────────────────────────────────────────
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(15), nullable=True)
    mobile_no = Column(String(15), nullable=True, index=True)
    whatsapp_no = Column(String(15), nullable=True)
    website = Column(String(255), nullable=True)

    # ── Location ─────────────────────────────────────────────────────────
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True, default="India")

    # ── Organization ─────────────────────────────────────────────────────
    industry = Column(String(100), nullable=True)
    business_type = Column(String(50), nullable=True)  # reuse Business.business_type family
    no_of_employees = Column(String(20), nullable=True)  # 1-10 / 11-50 / ... / 1000+
    declared_annual_revenue = Column(Numeric(15, 2), nullable=True)
    job_title = Column(String(100), nullable=True)
    lead_type = Column(
    SAEnum(
        LeadType,
        name="lead_type",
        native_enum=False,
        values_callable=lambda enum: [e.value for e in enum],
    ),
    nullable=True,
)

    # ── Source / attribution ─────────────────────────────────────────────
    source = Column(
    SAEnum(
        LeadSource,
        name="lead_source",
        native_enum=False,
        values_callable=lambda enum: [e.value for e in enum],
    ),
    nullable=False,
    default=LeadSource.MANUAL,
    )
    ca_partner_id = Column(
        UUID(as_uuid=True), ForeignKey("ca_partners.id", ondelete="SET NULL"), nullable=True
    )
    utm_source = Column(String(100), nullable=True)
    utm_medium = Column(String(100), nullable=True)
    utm_campaign = Column(String(100), nullable=True)
    utm_content = Column(String(100), nullable=True)

    # ── Lifecycle / status ───────────────────────────────────────────────
    status = Column(
    SAEnum(
        LeadStatus,
        name="lead_status",
        native_enum=False,
        values_callable=lambda enum: [e.value for e in enum],
    ),
    nullable=False,
    default=LeadStatus.LEAD,
    index=True,
    )
    qualification_status = Column(
    SAEnum(
        LeadQualificationStatus,
        name="lead_qualification_status",
        native_enum=False,
        values_callable=lambda enum: [e.value for e in enum],
    ),
    nullable=False,
    default=LeadQualificationStatus.UNQUALIFIED,
    )
    qualified_by = Column(UUID(as_uuid=True), nullable=True)
    qualified_on = Column(Date, nullable=True)

    # ── Identity verification (MSME-specific, no ERPNext equivalent) ────
    pan = Column(String(10), nullable=True)
    gstin = Column(String(15), nullable=True)
    # Current/cached precheck result -- needed inline on lead-detail render
    # without a join. Durable history of every precheck run lives in
    # LeadAIInsight (insight_type=KYC_VERIFICATION).
    kyc_precheck = Column(JSONB, nullable=True)

    # ── AI Layer: current-value cache only ────────────────────────────────
    # These are read-hot (list/filter/sort in GET /v1/leads) and therefore
    # cached directly on Lead. Full history of how these values changed
    # over time -- and any AI output that isn't a single scalar -- lives
    # in LeadAIInsight, not here.
    #
    # NOTE: ai_lead_score is a 0-100 CRM sales-readiness score, computed by
    # lead_scorer_node. It is NOT the same scale or purpose as
    # RiskScore.score (300-900 credit score) or the future Business Health
    # Score -- do not conflate these in any downstream consumer.
    ai_lead_score = Column(Integer, nullable=True)
    last_ai_enriched_at = Column(DateTime(timezone=True), nullable=True)

    # ── Duplicate resolution ──────────────────────────────────────────────
    duplicate_of_lead_id = Column(
        UUID(as_uuid=True), ForeignKey("leads.id", ondelete="SET NULL"), nullable=True
    )

    # ── Conversion target (Opportunity table lands in next spec) ─────────
    converted_opportunity_id = Column(UUID(as_uuid=True), nullable=True)

    # ── Flags ──────────────────────────────────────────────────────────────
    unsubscribed = Column(Boolean, nullable=False, default=False)
    disabled = Column(Boolean, nullable=False, default=False)

    # ── Denormalized counters ─────────────────────────────────────────────
    notes_count = Column(Integer, nullable=False, default=0)
    attachment_count = Column(Integer, nullable=False, default=0)
    last_activity_at = Column(DateTime(timezone=True), nullable=True)

    # ── Soft delete ────────────────────────────────────────────────────────
    is_deleted = Column(Boolean, nullable=False, default=False, index=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # ── Audit ──────────────────────────────────────────────────────────────
    created_by = Column(UUID(as_uuid=True), nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # ── Relationships ──────────────────────────────────────────────────────
    activities = relationship(
        "LeadActivity",
        back_populates="lead",
        cascade="all, delete-orphan",
        order_by="LeadActivity.created_at.desc()",
        foreign_keys="LeadActivity.lead_id",
    )
    attachments = relationship(
        "LeadAttachment",
        back_populates="lead",
        cascade="all, delete-orphan",
        order_by="LeadAttachment.created_at.desc()",
        foreign_keys="LeadAttachment.lead_id",
    )
    ai_insights = relationship(
        "LeadAIInsight",
        back_populates="lead",
        cascade="all, delete-orphan",
        order_by="LeadAIInsight.generated_at.desc()",
        foreign_keys="LeadAIInsight.lead_id",
    )
    duplicate_of = relationship("Lead", remote_side=[id], foreign_keys=[duplicate_of_lead_id])

    __table_args__ = (
        # Filter-pattern composites, matching GET /v1/leads query params.
        # Partial (WHERE is_deleted = false) since nearly every real query
        # excludes soft-deleted rows -- keeps the index small and avoids
        # spending the leading column on a near-constant predicate.
        Index(
            "ix_leads_business_status",
            "business_id", "status",
            postgresql_where=(is_deleted == False),  # noqa: E712
        ),
        Index(
            "ix_leads_business_qualification",
            "business_id", "qualification_status",
            postgresql_where=(is_deleted == False),  # noqa: E712
        ),
        Index(
            "ix_leads_business_source",
            "business_id", "source",
            postgresql_where=(is_deleted == False),  # noqa: E712
        ),
        Index(
            "ix_leads_business_owner",
            "business_id", "lead_owner_id",
            postgresql_where=(is_deleted == False),  # noqa: E712
        ),
        Index(
            "ix_leads_business_ca_partner",
            "business_id", "ca_partner_id",
            postgresql_where=(ca_partner_id.isnot(None)),
        ),
        # Pipeline-summary / list default ordering.
        Index("ix_leads_business_created", "business_id", "created_at"),
        # Staleness report: leads with no recent activity.
        Index("ix_leads_business_last_activity", "business_id", "last_activity_at"),
        # AI-prioritized lead lists ("show me my highest-scored open leads").
        Index(
            "ix_leads_business_ai_score",
            "business_id", "ai_lead_score",
            postgresql_where=(is_deleted == False),  # noqa: E712
        ),
    )


# ─────────────────────────────────────────────────────────────────────────────
# LeadActivity
# ─────────────────────────────────────────────────────────────────────────────

class LeadActivity(Base):
    """
    Unified, append-only activity timeline for a Lead.

    Replaces ERPNext's split Notes / Open Activities / All Activities
    HTML widgets with a single queryable table. Also the landing surface
    for AI-generated suggestions (activity_type = ai_suggestion).

    activity_type answers "what kind of entry is this" (call, note,
    status_change, ...). actor_type answers "who/what produced it"
    (human, ai, system) -- kept as two independent axes rather than one
    combinatorial enum.
    """
    __tablename__ = "lead_activities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    lead_id = Column(
        UUID(as_uuid=True), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True
    )
    # Denormalized for tenant-isolation queries without joining through Lead.
    business_id = Column(
        UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )

    activity_type = Column(
    SAEnum(
        LeadActivityType,
        name="lead_activity_type",
        native_enum=False,
        values_callable=lambda enum: [e.value for e in enum],
    ),
    nullable=False,
    )
    actor_type = Column(
    SAEnum(
        LeadActivityActorType,
        name="lead_activity_actor_type",
        native_enum=False,
        values_callable=lambda enum: [e.value for e in enum],
    ),
    nullable=False,
    default=LeadActivityActorType.HUMAN,
    )
    content = Column(Text, nullable=True)

    # e.g. {"old_status": "Lead", "new_status": "Open"} for status_change
    # entries, or {"insight_id": "..."} pointing back into LeadAIInsight
    # for ai_suggestion entries.
    activity_metadata = Column("metadata", JSONB, nullable=True)

    next_action_due = Column(DateTime(timezone=True), nullable=True)

    # ── Audit ──────────────────────────────────────────────────────────────
    # created_by: staff/user UUID when actor_type=human; NULL when
    # actor_type is ai or system.
    created_by = Column(UUID(as_uuid=True), nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # ── Relationships ──────────────────────────────────────────────────────
    lead = relationship("Lead", back_populates="activities", foreign_keys=[lead_id])

    __table_args__ = (
        Index("ix_lead_activities_lead_created", "lead_id", "created_at"),
        Index("ix_lead_activities_business_type", "business_id", "activity_type"),
        Index("ix_lead_activities_business_actor", "business_id", "actor_type"),
        # Cross-lead "follow-ups due" dashboard query -- scans across ALL
        # of a business's leads for due reminders, not within one lead's
        # timeline (that's covered by ix_lead_activities_lead_created).
        Index(
            "ix_lead_activities_business_next_action",
            "business_id", "next_action_due",
            postgresql_where=(next_action_due.isnot(None)),
        ),
    )


# ─────────────────────────────────────────────────────────────────────────────
# LeadAttachment
# ─────────────────────────────────────────────────────────────────────────────

class LeadAttachment(Base):
    """
    File attachments on a Lead -- visiting cards, quotation drafts, ID
    proofs, photos, scanned documents.

    Hard-delete semantics (no soft delete): deletion means storage cleanup
    + row removal, handled transactionally in the Service Layer. No
    ERPNext equivalent as a first-class entity -- Frappe treats file
    attachments generically; CreditBridge models them explicitly per the
    approved amendment.
    """
    __tablename__ = "lead_attachments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    lead_id = Column(
        UUID(as_uuid=True), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True
    )
    business_id = Column(
        UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )

    file_name = Column(String(255), nullable=False)
    file_type = Column(
        SAEnum(LeadAttachmentFileType, name="lead_attachment_file_type", native_enum=False, values_callable=lambda e: [m.value for m in e]),
        nullable=False,
    )
    mime_type = Column(String(100), nullable=True)
    file_size_bytes = Column(Integer, nullable=False)
    category = Column(String(30), nullable=True)  # visiting_card / quotation_draft / id_proof / photo / other

    # Abstracted storage reference -- local path or object-storage URL.
    # Storage backend decision (local disk vs S3-compatible) is a
    # Repository-layer concern, not a schema concern.
    storage_url = Column(String(500), nullable=False)

    uploaded_by = Column(UUID(as_uuid=True), nullable=True)

    # ── Audit ──────────────────────────────────────────────────────────────
    created_by = Column(UUID(as_uuid=True), nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # ── Relationships ──────────────────────────────────────────────────────
    lead = relationship("Lead", back_populates="attachments", foreign_keys=[lead_id])

    __table_args__ = (
        Index("ix_lead_attachments_lead_created", "lead_id", "created_at"),
        Index("ix_lead_attachments_business_category", "business_id", "category"),
    )


# ─────────────────────────────────────────────────────────────────────────────
# LeadAIInsight  (NEW -- Stage 1 review amendment)
# ─────────────────────────────────────────────────────────────────────────────

class LeadAIInsight(Base):
    """
    Append-only, versioned log of AI-generated outputs for a Lead.

    Exists because recurring agents (lead_scorer_node,
    lead_business_size_estimator_node, lead_conversation_summarizer_node)
    each re-run on subsequent events and produce structured, multi-field
    output -- neither of which fits cleanly as mutable scalar columns on
    Lead. Lead retains only a thin "current value" cache
    (ai_lead_score, kyc_precheck, last_ai_enriched_at) for fast,
    join-free reads in list/filter APIs; this table is the durable,
    queryable history behind that cache.

    Never written to by anything other than the lead_pipeline AI agents.
    Never exposed to the Lender Terminal -- see frozen spec, Section 12.
    """
    __tablename__ = "lead_ai_insights"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    lead_id = Column(
        UUID(as_uuid=True), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True
    )
    business_id = Column(
        UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )

    insight_type = Column(
        SAEnum(LeadAIInsightType, name="lead_ai_insight_type", native_enum=False, values_callable=lambda e: [m.value for m in e]), nullable=False
    )

    # Flexible payload, shape determined by insight_type. E.g. for
    # LEAD_SCORE: {"ai_lead_score": 72, "reasoning": [...], "prior_score": 65}.
    # For BUSINESS_SIZE_ESTIMATE: {"bracket": "11-50", "signals": [...]}.
    value = Column(JSONB, nullable=False)

    # 0.000-1.000. Deliberately named confidence_score, never bare "score",
    # to avoid any ambiguity with ai_lead_score / RiskScore.score.
    confidence_score = Column(Numeric(4, 3), nullable=True)

    model_version = Column(String(50), nullable=True)

    # When a recurring agent re-runs and produces a newer insight of the
    # same type, the prior row is marked superseded rather than deleted --
    # preserves full history for trend analysis (e.g. score-over-time).
    superseded_at = Column(DateTime(timezone=True), nullable=True)

    generated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # ── Relationships ──────────────────────────────────────────────────────
    lead = relationship("Lead", back_populates="ai_insights", foreign_keys=[lead_id])

    __table_args__ = (
        # Fetch current/history for one lead's one insight type, newest first.
        Index("ix_lead_ai_insights_lead_type_generated", "lead_id", "insight_type", "generated_at"),
        # Business-wide analytics per insight type (e.g. avg confidence
        # across all duplicate_suggestion insights this month).
        Index("ix_lead_ai_insights_business_type", "business_id", "insight_type"),
        # Fast "give me the current (non-superseded) insight" lookup.
        Index(
            "ix_lead_ai_insights_current",
            "lead_id", "insight_type",
            postgresql_where=(superseded_at.is_(None)),
        ),
    )

