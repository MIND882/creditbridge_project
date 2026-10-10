"""Pydantic v2 schemas for LoyaltyPointEntryRedemption."""





from __future__ import annotations

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "LoyaltyPointEntryRedemptionCreate",

    "LoyaltyPointEntryRedemptionRead",

    "LoyaltyPointEntryRedemptionListResponse",

]





class LoyaltyPointEntryRedemptionBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    sales_invoice: Optional[str] = None

    redemption_date: Optional[dt.date] = None

    redeemed_points: Optional[int] = None





class LoyaltyPointEntryRedemptionCreate(LoyaltyPointEntryRedemptionBase):

    """Accepted only nested inside the parent payload."""

    pass





class LoyaltyPointEntryRedemptionRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    sales_invoice: Optional[str] = None

    redemption_date: Optional[dt.date] = None

    redeemed_points: Optional[int] = None





LoyaltyPointEntryRedemptionListResponse = Page[LoyaltyPointEntryRedemptionRead]
