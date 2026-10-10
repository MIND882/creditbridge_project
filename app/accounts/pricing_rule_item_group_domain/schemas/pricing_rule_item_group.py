"""Pydantic v2 schemas for PricingRuleItemGroup."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PricingRuleItemGroupCreate",

    "PricingRuleItemGroupRead",

    "PricingRuleItemGroupListResponse",

]





class PricingRuleItemGroupBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    parenttype: Optional[str] = None

    item_group: Optional[str] = None

    uom: Optional[str] = None





class PricingRuleItemGroupCreate(PricingRuleItemGroupBase):

    """Accepted only nested inside the parent payload."""

    pass





class PricingRuleItemGroupRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    parenttype: Optional[str] = None

    item_group: Optional[str] = None

    uom: Optional[str] = None





PricingRuleItemGroupListResponse = Page[PricingRuleItemGroupRead]
