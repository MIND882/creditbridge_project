"""Pydantic v2 schemas for PricingRuleBrand."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PricingRuleBrandCreate",

    "PricingRuleBrandRead",

    "PricingRuleBrandListResponse",

]





class PricingRuleBrandBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    parenttype: Optional[str] = None

    brand: Optional[str] = None

    uom: Optional[str] = None





class PricingRuleBrandCreate(PricingRuleBrandBase):

    """Accepted only nested inside the parent payload."""

    pass





class PricingRuleBrandRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    parenttype: Optional[str] = None

    brand: Optional[str] = None

    uom: Optional[str] = None





PricingRuleBrandListResponse = Page[PricingRuleBrandRead]
