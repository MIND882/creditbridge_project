"""Pydantic v2 schemas for SubscriptionPlanDetail."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SubscriptionPlanDetailCreate",

    "SubscriptionPlanDetailRead",

    "SubscriptionPlanDetailListResponse",

]





class SubscriptionPlanDetailBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    parenttype: Optional[str] = None

    qty: Optional[int] = None

    plan: str





class SubscriptionPlanDetailCreate(SubscriptionPlanDetailBase):

    """Accepted only nested inside the parent payload."""

    pass





class SubscriptionPlanDetailRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    parenttype: Optional[str] = None

    qty: int

    plan: str





SubscriptionPlanDetailListResponse = Page[SubscriptionPlanDetailRead]
