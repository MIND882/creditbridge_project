"""Pydantic v2 schemas for LoyaltyPointEntry."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "LoyaltyPointEntryCreate",

    "LoyaltyPointEntryUpdate",

    "LoyaltyPointEntryRead",

    "LoyaltyPointEntryListResponse",

]





class LoyaltyPointEntryBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    loyalty_program: str

    loyalty_program_tier: Optional[str] = None

    customer: str

    redeem_against: Optional[str] = None

    loyalty_points: Optional[int] = None

    purchase_amount: Optional[Decimal] = None

    expiry_date: dt.date

    posting_date: dt.date

    invoice_type: str

    invoice: Optional[str] = None

    discretionary_reason: Optional[str] = None





class LoyaltyPointEntryCreate(LoyaltyPointEntryBase):

    pass





class LoyaltyPointEntryUpdate(InputSchema):

    """A partial update."""



    loyalty_program: Optional[str] = None

    loyalty_program_tier: Optional[str] = None

    customer: Optional[str] = None

    redeem_against: Optional[str] = None

    loyalty_points: Optional[int] = None

    purchase_amount: Optional[Decimal] = None

    expiry_date: Optional[dt.date] = None

    posting_date: Optional[dt.date] = None

    invoice_type: Optional[str] = None

    invoice: Optional[str] = None

    discretionary_reason: Optional[str] = None





class LoyaltyPointEntryRead(ReadSchema):

    id: uuid.UUID

    name: str

    loyalty_program: str

    loyalty_program_tier: Optional[str] = None

    customer: str

    redeem_against: Optional[str] = None

    loyalty_points: int

    purchase_amount: Optional[Decimal] = None

    expiry_date: dt.date

    posting_date: dt.date

    invoice_type: str

    invoice: Optional[str] = None

    discretionary_reason: Optional[str] = None





LoyaltyPointEntryListResponse = Page[LoyaltyPointEntryRead]
