"""Pydantic v2 schemas for ShippingRule."""





from __future__ import annotations

from app.accounts.shipping_rule_domain.models.shipping_rule import (

    ShippingRuleCalculateBasedOn,

    ShippingRuleShippingRuleType,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.shipping_rule_condition_domain.schemas.shipping_rule_condition import (

    ShippingRuleConditionCreate,

    ShippingRuleConditionRead,

)

from app.accounts.shipping_rule_country_domain.schemas.shipping_rule_country import (

    ShippingRuleCountryCreate,

    ShippingRuleCountryRead,

)



__all__ = [

    "ShippingRuleCreate",

    "ShippingRuleUpdate",

    "ShippingRuleRead",

    "ShippingRuleListResponse",

]





class ShippingRuleBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    label: str

    disabled: Optional[bool] = None

    shipping_rule_type: Optional[ShippingRuleShippingRuleType] = None

    account_id: uuid.UUID

    cost_center_id: Optional[uuid.UUID] = None

    calculate_based_on: Optional[ShippingRuleCalculateBasedOn] = None

    shipping_amount: Optional[Decimal] = None

    project: Optional[str] = None



    conditions: list[ShippingRuleConditionCreate] = []



    countries: list[ShippingRuleCountryCreate] = []





class ShippingRuleCreate(ShippingRuleBase):

    pass





class ShippingRuleUpdate(InputSchema):

    """A partial update."""



    label: Optional[str] = None

    disabled: Optional[bool] = None

    shipping_rule_type: Optional[ShippingRuleShippingRuleType] = None

    account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    calculate_based_on: Optional[ShippingRuleCalculateBasedOn] = None

    shipping_amount: Optional[Decimal] = None

    project: Optional[str] = None

    conditions: Optional[list[ShippingRuleConditionCreate]] = None

    countries: Optional[list[ShippingRuleCountryCreate]] = None





class ShippingRuleRead(ReadSchema):

    id: uuid.UUID

    name: str

    label: str

    disabled: bool

    shipping_rule_type: Optional[ShippingRuleShippingRuleType] = None

    account_id: uuid.UUID

    cost_center_id: Optional[uuid.UUID] = None

    calculate_based_on: Optional[ShippingRuleCalculateBasedOn] = None

    shipping_amount: Optional[Decimal] = None

    project: Optional[str] = None

    conditions: list[ShippingRuleConditionRead] = []

    countries: list[ShippingRuleCountryRead] = []





ShippingRuleListResponse = Page[ShippingRuleRead]
