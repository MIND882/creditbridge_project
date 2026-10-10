"""backend/app/crm/schemas/lead.py
Ye file CRM  lead module ke liye Pydanitc Schemas rakhti hai 
iska kaam hai api me aane wale aur api se bahr jane wale data ko validate aur structure me karna.

Reference:
- CRM Lead SQLALchemy Model [frozen]
- Final Lead Engineering Design (Frozen)
- EXPNext ka complete Lead Workflow

Lead
|
Opportunity
|
Customer
|
Sale Order
|
Invoice
|
Payment

Is file me sirf Schemas honge.

Jaise:

- LeadCreate
- LeadUpdate
- LeadResponse
- LeadListResponse
- LeadActivityResponse
- LeadAttachmentResponse
- LeadAIInsightResponse

Is file me:
❌ database queries nahi hongi
❌ Business logic nhi hoga 
❌ api routes nhi. hongi
❌ Repository ya Service code nhi hoga.

Saare Enum direactly CRM Lead model se import honge

Reason:
Valid values sirf ek hi jagah define honi chahiye (Single Source of Truth).
Agar future me koi enum value change hoti hai, to sirf Model update karna
padega. Schema automatically wahi use karega.
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from app.crm.lead_domain.models.lead import (
    LeadActivityActorType,
    LeadActivityType,
    LeadAIInsight,
    LeadAttachmentFileType,
    LeadQualificationStatus,
    LeadSource,
    LeadStatus,
    LeadType,
    Lead,
    LeadActivity,
    LeadAttachment,
    LeadAIInsightType,
)

#--------------------------------------------------------
# Lead - Create
#--------------------------------------------------------

class LeadCreate(BaseModel):
    """
    Payload for POST /v1/leads.

    business_id is deliberately NOT a field here -- it is derived from the
    authenticated caller's JWT (get_current_business_id), never accepted
    from the request body, per the cross-tenant isolation rule in the
    frozen spec.

    lead_name, status, ai_lead_score, kyc_precheck, counters, and audit
    fields are server-computed / server-owned and never accepted on create.
    """
    model_config = ConfigDict(str_strip_whitespace=True)

    # Ownership
    lead_owner_id: Optional[UUID] = None

    # Identity
    first_name: Optional[str] = Field(None, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    company_name: Optional[str] = Field(None, max_length=255)
    gender: Optional[str] = Field(None, max_length=20)

    # Contact channels
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=15)
    mobile_no: Optional[str] = Field(None, max_length=15)
    whatsapp_no: Optional[str] = Field(None, max_length=15)
    website: Optional[str] = Field(None, max_length=255)

    # Location
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field("India", max_length=100)

    # Organization
    industry: Optional[str] = Field(None, max_length=100)
    business_type: Optional[str] = Field(None, max_length=50)
    no_of_employees: Optional[str] = Field(None, max_length=20)
    declared_annual_revenue: Optional[Decimal] = Field(None, ge=0)
    job_title: Optional[str] = Field(None, max_length=100)
    lead_type: Optional[LeadType] = None

    # Source / attribution
    source: LeadSource = LeadSource.MANUAL
    ca_partner_id: Optional[UUID] = None
    utm_source: Optional[str] = Field(None, max_length=100)
    utm_medium: Optional[str] = Field(None, max_length=100)
    utm_campaign: Optional[str] = Field(None, max_length=100)
    utm_content: Optional[str] = Field(None, max_length=100)

    # Identity verification (optional at lead stage)
    pan: Optional[str] = Field(None, min_length=10, max_length=10)
    gstin: Optional[str] = Field(None, min_length=15, max_length=15)

    @model_validator(mode="after")
    def _validate_name_xor(self) -> "LeadCreate":
        """
        Mirrors ERPNext's mandatory_depends_on XOR pattern: at least one of
        first_name / company_name is required. Enforced here as a model
        validator rather than per-field conditional-mandatory, since
        Pydantic has no direct equivalent of Frappe's mandatory_depends_on.
        """
        if not self.first_name and not self.company_name:
            raise ValueError(
                "A Lead requires either a person's first_name or a company_name."
            )
        return self

    @model_validator(mode="after")
    def _validate_contact_channel_present(self) -> "LeadCreate":
        """
        Stricter than ERPNext: a Lead with zero reachability has no
        operational value, per the frozen spec's validation rules.
        """
        if not any([self.email, self.phone, self.mobile_no, self.whatsapp_no]):
            raise ValueError(
                "At least one contact channel is required: "
                "email, phone, mobile_no, or whatsapp_no."
            )
        return self


# ─────────────────────────────────────────────────────────────────────────────
# Lead — Update
# ─────────────────────────────────────────────────────────────────────────────

class LeadUpdate(BaseModel):
    """
    Payload for PATCH /v1/leads/{id}. All fields optional (partial update).

    status, ai_lead_score, kyc_precheck, duplicate_of_lead_id,
    converted_opportunity_id, counters, and audit fields are intentionally
    absent -- these are owned by dedicated endpoints
    (/qualify, /convert, /mark-duplicate) and internal services, not
    general-purpose PATCH, per the frozen spec's status-transition rules.
    """
    model_config = ConfigDict(str_strip_whitespace=True)

    lead_owner_id: Optional[UUID] = None

    first_name: Optional[str] = Field(None, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    company_name: Optional[str] = Field(None, max_length=255)
    gender: Optional[str] = Field(None, max_length=20)

    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=15)
    mobile_no: Optional[str] = Field(None, max_length=15)
    whatsapp_no: Optional[str] = Field(None, max_length=15)
    website: Optional[str] = Field(None, max_length=255)

    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)

    industry: Optional[str] = Field(None, max_length=100)
    business_type: Optional[str] = Field(None, max_length=50)
    no_of_employees: Optional[str] = Field(None, max_length=20)
    declared_annual_revenue: Optional[Decimal] = Field(None, ge=0)
    job_title: Optional[str] = Field(None, max_length=100)
    lead_type: Optional[LeadType] = None

    ca_partner_id: Optional[UUID] = None
    utm_source: Optional[str] = Field(None, max_length=100)
    utm_medium: Optional[str] = Field(None, max_length=100)
    utm_campaign: Optional[str] = Field(None, max_length=100)
    utm_content: Optional[str] = Field(None, max_length=100)

    pan: Optional[str] = Field(None, min_length=10, max_length=10)
    gstin: Optional[str] = Field(None, min_length=15, max_length=15)

    unsubscribed: Optional[bool] = None
    disabled: Optional[bool] = None


# ─────────────────────────────────────────────────────────────────────────────
# Lead — Qualify (dedicated endpoint payload, per frozen API spec)
# ─────────────────────────────────────────────────────────────────────────────

class LeadQualifyRequest(BaseModel):
    """Payload for POST /v1/leads/{id}/qualify."""

    qualification_status: LeadQualificationStatus
    qualified_by: Optional[UUID] = None
    qualified_on: Optional[date] = None

    @model_validator(mode="after")
    def _validate_qualified_pair(self) -> "LeadQualifyRequest":
        """
        qualified_on cannot be set without qualified_by, and vice versa
        -- paired fields per the frozen validation rules.
        """
        if bool(self.qualified_by) != bool(self.qualified_on):
            raise ValueError(
                "qualified_by and qualified_on must be provided together, or not at all."
            )
        return self


class LeadMarkDuplicateRequest(BaseModel):
    """Payload for POST /v1/leads/{id}/mark-duplicate."""

    duplicate_of_lead_id: UUID
    reason: str = Field(..., min_length=1, max_length=500)


# ─────────────────────────────────────────────────────────────────────────────
# Lead — Response
# ─────────────────────────────────────────────────────────────────────────────

class LeadResponse(BaseModel):
    """
    Full detail response for GET /v1/leads/{id}.

    Excludes: is_deleted, deleted_at (internal soft-delete bookkeeping,
    never surfaced to any client).
    """
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    business_id: UUID
    lead_owner_id: Optional[UUID] = None

    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    lead_name: str
    company_name: Optional[str] = None
    title: Optional[str] = None
    gender: Optional[str] = None

    email: Optional[str] = None
    phone: Optional[str] = None
    mobile_no: Optional[str] = None
    whatsapp_no: Optional[str] = None
    website: Optional[str] = None

    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None

    industry: Optional[str] = None
    business_type: Optional[str] = None
    no_of_employees: Optional[str] = None
    declared_annual_revenue: Optional[Decimal] = None
    job_title: Optional[str] = None
    lead_type: Optional[LeadType] = None

    source: LeadSource
    ca_partner_id: Optional[UUID] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_content: Optional[str] = None

    status: LeadStatus
    qualification_status: LeadQualificationStatus
    qualified_by: Optional[UUID] = None
    qualified_on: Optional[date] = None

    pan: Optional[str] = None
    gstin: Optional[str] = None
    kyc_precheck: Optional[dict] = None

    ai_lead_score: Optional[int] = None
    last_ai_enriched_at: Optional[datetime] = None

    duplicate_of_lead_id: Optional[UUID] = None
    converted_opportunity_id: Optional[UUID] = None

    unsubscribed: bool
    disabled: bool

    notes_count: int
    attachment_count: int
    last_activity_at: Optional[datetime] = None

    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class LeadListItem(BaseModel):
    """
    Thin row shape for GET /v1/leads (paginated list).

    Deliberately excludes kyc_precheck (JSONB blob), UTM fields, and the
    full audit quartet -- list views are high-frequency and should not
    ship heavy per-row payloads. Detail lives behind GET /leads/{id}.
    """
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    lead_name: str
    company_name: Optional[str] = None
    email: Optional[str] = None
    mobile_no: Optional[str] = None
    city: Optional[str] = None
    source: LeadSource
    status: LeadStatus
    qualification_status: LeadQualificationStatus
    ai_lead_score: Optional[int] = None
    lead_owner_id: Optional[UUID] = None
    notes_count: int
    attachment_count: int
    last_activity_at: Optional[datetime] = None
    created_at: datetime


class LeadListResponse(BaseModel):
    """Paginated envelope for GET /v1/leads."""
    model_config = ConfigDict(from_attributes=True)

    total: int
    page: int
    page_size: int
    items: list[LeadListItem]


# ─────────────────────────────────────────────────────────────────────────────
# LeadActivity — Create / Response
# ─────────────────────────────────────────────────────────────────────────────

class LeadActivityCreate(BaseModel):
    """
    Payload for POST /v1/leads/{id}/activities.

    lead_id and business_id are path/JWT-derived, not accepted in the
    body. actor_type defaults to HUMAN since this endpoint is the
    human-facing activity-log route; AI/system-generated activities are
    written internally by the Service/Agent layer, not through this schema.
    """
    model_config = ConfigDict(str_strip_whitespace=True)

    activity_type: LeadActivityType
    content: Optional[str] = Field(None, max_length=5000)
    next_action_due: Optional[datetime] = None

    @model_validator(mode="after")
    def _validate_content_required_for_most_types(self) -> "LeadActivityCreate":
        """
        status_change entries are typically system-populated via metadata
        rather than free-text content, so content is optional only for
        that type; all human-authored activity types need content.
        """
        if self.activity_type != LeadActivityType.STATUS_CHANGE and not self.content:
            raise ValueError(
                f"content is required for activity_type '{self.activity_type.value}'."
            )
        return self


class LeadActivityResponse(BaseModel):
    """Response shape for activity timeline entries."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID
    lead_id: UUID
    business_id: UUID
    activity_type: LeadActivityType
    actor_type: LeadActivityActorType
    content: Optional[str] = None
    metadata: Optional[dict] = Field(None, validation_alias="activity_metadata")
    next_action_due: Optional[datetime] = None
    created_by: Optional[UUID] = None
    created_at: datetime


# ─────────────────────────────────────────────────────────────────────────────
# LeadAttachment — Response
# ─────────────────────────────────────────────────────────────────────────────
# No LeadAttachmentCreate here: upload is multipart/form-data
# (file_name, mime_type, file_size_bytes are derived from the uploaded
# file itself, not client-declared JSON), so the create-side contract
# belongs to the Service/API layer's upload handler, not a JSON schema.

class LeadAttachmentResponse(BaseModel):
    """Response shape for GET /v1/leads/{id}/attachments."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    lead_id: UUID
    business_id: UUID
    file_name: str
    file_type: LeadAttachmentFileType
    mime_type: Optional[str] = None
    file_size_bytes: int
    category: Optional[str] = None
    storage_url: str
    uploaded_by: Optional[UUID] = None
    created_at: datetime


# ─────────────────────────────────────────────────────────────────────────────
# LeadAIInsight — Response
# ─────────────────────────────────────────────────────────────────────────────
# No Create schema: LeadAIInsight rows are written exclusively by the
# lead_pipeline AI agents (Service/Agent layer), never accepted as
# client input, per the frozen spec ("Never written to by anything
# other than the lead_pipeline AI agents").

class LeadAIInsightResponse(BaseModel):
    """
    Response shape for AI-generated insight history.

    Never exposed to the Lender Terminal -- MSME-side consumption only,
    per the frozen spec's Section 12 boundary.
    """
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    lead_id: UUID
    insight_type: LeadAIInsightType
    value: dict
    confidence_score: Optional[Decimal] = Field(None, ge=0, le=1)
    model_version: Optional[str] = None
    superseded_at: Optional[datetime] = None
    generated_at: datetime
