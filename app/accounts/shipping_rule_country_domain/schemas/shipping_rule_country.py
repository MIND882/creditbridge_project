"""Pydantic v2 schemas for ShippingRuleCountry."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ShippingRuleCountryCreate",

    "ShippingRuleCountryRead",

    "ShippingRuleCountryListResponse",

]





class ShippingRuleCountryBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    country: str





class ShippingRuleCountryCreate(ShippingRuleCountryBase):

    """Accepted only nested inside the parent payload."""

    pass





class ShippingRuleCountryRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    country: str





ShippingRuleCountryListResponse = Page[ShippingRuleCountryRead]
