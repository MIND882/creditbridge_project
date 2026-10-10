"""Pydantic v2 schemas for SubscriptionPlan."""





from __future__ import annotations

from app.accounts.subscription_plan_domain.models.subscription_plan import (

    SubscriptionPlanBillingInterval,

    SubscriptionPlanPriceDetermination,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SubscriptionPlanCreate",

    "SubscriptionPlanUpdate",

    "SubscriptionPlanRead",

    "SubscriptionPlanListResponse",

]





class SubscriptionPlanBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    plan_name: str

    currency: str

    item: str

    price_determination: SubscriptionPlanPriceDetermination

    cost: Optional[Decimal] = None

    price_list: Optional[str] = None

    billing_interval: SubscriptionPlanBillingInterval

    billing_interval_count: Optional[int] = None

    payment_gateway: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None





class SubscriptionPlanCreate(SubscriptionPlanBase):

    pass





class SubscriptionPlanUpdate(InputSchema):

    """A partial update."""



    plan_name: Optional[str] = None

    currency: Optional[str] = None

    item: Optional[str] = None

    price_determination: Optional[SubscriptionPlanPriceDetermination] = None

    cost: Optional[Decimal] = None

    price_list: Optional[str] = None

    billing_interval: Optional[SubscriptionPlanBillingInterval] = None

    billing_interval_count: Optional[int] = None

    payment_gateway: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None





class SubscriptionPlanRead(ReadSchema):

    id: uuid.UUID

    name: str

    plan_name: str

    currency: str

    item: str

    price_determination: SubscriptionPlanPriceDetermination

    cost: Optional[Decimal] = None

    price_list: Optional[str] = None

    billing_interval: SubscriptionPlanBillingInterval

    billing_interval_count: int

    payment_gateway: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None





SubscriptionPlanListResponse = Page[SubscriptionPlanRead]
