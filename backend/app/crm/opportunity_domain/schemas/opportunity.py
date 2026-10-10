"""
Pydantic schemas for the Opportunity domain.

Validation mirrors `backend.app.crm.opportunity.models.opportunity.Opportunity`.
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
