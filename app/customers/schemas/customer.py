"""
Pydantic schemas for the Customer domain.
"""

import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class CustomerStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class CustomerGSTStatus(str, Enum):
    NOT_LINKED = "not_linked"
    PENDING_VERIFICATION = "pending_verification"
    VERIFIED = "verified"


class CustomerBankConnectionStatus(str, Enum):
    NOT_CONNECTED = "not_connected"
    PENDING = "pending"
    CONNECTED = "connected"


class CustomerBase(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=255)
    customer_group: Optional[str] = Field(None, max_length=100)
    territory: Optional[str] = Field(None, max_length=100)
    industry: Optional[str] = Field(None, max_length=100)

    primary_contact_name: Optional[str] = Field(None, max_length=255)
    primary_contact_email: Optional[EmailStr] = None
    primary_contact_phone: Optional[str] = Field(None, max_length=15)

    address_line: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: str = Field("India", max_length=100)
    pincode: Optional[str] = Field(None, max_length=10)

    gstin: Optional[str] = Field(None, max_length=15)
    pan: Optional[str] = Field(None, max_length=10)

    @field_validator("gstin")
    @classmethod
    def validate_gstin_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip().upper()
        if v and len(v) != 15:
            raise ValueError("GSTIN must be exactly 15 characters")
        return v

    @field_validator("pan")
    @classmethod
    def validate_pan_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip().upper()
        if v and len(v) != 10:
            raise ValueError("PAN must be exactly 10 characters")
        return v


class CustomerCreatePayload(CustomerBase):
    converted_from_lead_id: Optional[uuid.UUID] = None
    converted_from_opportunity_id: Optional[uuid.UUID] = None
    converted_from_quotation_id: Optional[uuid.UUID] = None


class CustomerUpdatePayload(BaseModel):
    customer_name: Optional[str] = Field(None, min_length=1, max_length=255)
    customer_group: Optional[str] = Field(None, max_length=100)
    territory: Optional[str] = Field(None, max_length=100)
    industry: Optional[str] = Field(None, max_length=100)

    primary_contact_name: Optional[str] = Field(None, max_length=255)
    primary_contact_email: Optional[EmailStr] = None
    primary_contact_phone: Optional[str] = Field(None, max_length=15)

    address_line: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    pincode: Optional[str] = Field(None, max_length=10)

    gstin: Optional[str] = Field(None, max_length=15)
    pan: Optional[str] = Field(None, max_length=10)

    status: Optional[CustomerStatus] = None


class CustomerIntelligenceUpdatePayload(BaseModel):
    credit_readiness_score: Optional[Decimal] = Field(None, ge=0, le=999.99)
    gst_status: Optional[CustomerGSTStatus] = None
    bank_connection_status: Optional[CustomerBankConnectionStatus] = None
    loan_eligibility_flag: Optional[bool] = None


class CustomerListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    customer_name: str
    customer_group: Optional[str]
    city: Optional[str]
    status: CustomerStatus
    gst_status: Optional[CustomerGSTStatus]
    bank_connection_status: Optional[CustomerBankConnectionStatus]
    credit_readiness_score: Optional[Decimal]
    created_at: datetime


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    business_id: uuid.UUID

    customer_name: str
    customer_group: Optional[str]
    territory: Optional[str]
    industry: Optional[str]

    primary_contact_name: Optional[str]
    primary_contact_email: Optional[str]
    primary_contact_phone: Optional[str]

    address_line: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: str
    pincode: Optional[str]

    gstin: Optional[str]
    pan: Optional[str]

    converted_from_lead_id: Optional[uuid.UUID]
    converted_from_opportunity_id: Optional[uuid.UUID]
    converted_from_quotation_id: Optional[uuid.UUID]

    status: CustomerStatus

    credit_readiness_score: Optional[Decimal]
    gst_status: Optional[CustomerGSTStatus]
    bank_connection_status: Optional[CustomerBankConnectionStatus]
    loan_eligibility_flag: Optional[bool]

    created_at: datetime
    updated_at: Optional[datetime]


class CustomerListResponse(BaseModel):
    items: list[CustomerListItem]
    total: int
    page: int
    page_size: int
