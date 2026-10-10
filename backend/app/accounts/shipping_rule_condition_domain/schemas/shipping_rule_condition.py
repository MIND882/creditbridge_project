"""Pydantic v2 schemas for ShippingRuleCondition."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ShippingRuleConditionCreate",

    "ShippingRuleConditionRead",

    "ShippingRuleConditionListResponse",

]





class ShippingRuleConditionBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    from_value: Optional[Decimal] = None

    to_value: Optional[Decimal] = None

    shipping_amount: Optional[Decimal] = None





class ShippingRuleConditionCreate(ShippingRuleConditionBase):

    """Accepted only nested inside the parent payload."""

    pass





class ShippingRuleConditionRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    from_value: Decimal

    to_value: Optional[Decimal] = None

    shipping_amount: Decimal





ShippingRuleConditionListResponse = Page[ShippingRuleConditionRead]
