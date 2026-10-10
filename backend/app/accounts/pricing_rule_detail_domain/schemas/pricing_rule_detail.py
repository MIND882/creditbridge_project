"""Pydantic v2 schemas for PricingRuleDetail."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PricingRuleDetailCreate",

    "PricingRuleDetailRead",

    "PricingRuleDetailListResponse",

]





class PricingRuleDetailBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    parenttype: Optional[str] = None

    pricing_rule: Optional[str] = None

    item_code: Optional[str] = None

    margin_type: Optional[str] = None

    rate_or_discount: Optional[str] = None

    child_docname: Optional[str] = None

    rule_applied: Optional[bool] = None





class PricingRuleDetailCreate(PricingRuleDetailBase):

    """Accepted only nested inside the parent payload."""

    pass





class PricingRuleDetailRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    parenttype: Optional[str] = None

    pricing_rule: Optional[str] = None

    item_code: Optional[str] = None

    margin_type: Optional[str] = None

    rate_or_discount: Optional[str] = None

    child_docname: Optional[str] = None

    rule_applied: bool





PricingRuleDetailListResponse = Page[PricingRuleDetailRead]
