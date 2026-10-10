"""Pydantic v2 schemas for PricingRuleItemCode."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PricingRuleItemCodeCreate",

    "PricingRuleItemCodeRead",

    "PricingRuleItemCodeListResponse",

]





class PricingRuleItemCodeBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    parenttype: Optional[str] = None

    item_code: Optional[str] = None

    uom: Optional[str] = None





class PricingRuleItemCodeCreate(PricingRuleItemCodeBase):

    """Accepted only nested inside the parent payload."""

    pass





class PricingRuleItemCodeRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    parenttype: Optional[str] = None

    item_code: Optional[str] = None

    uom: Optional[str] = None





PricingRuleItemCodeListResponse = Page[PricingRuleItemCodeRead]
