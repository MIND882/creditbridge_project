"""Pydantic v2 schemas for SubscriptionSettings."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SubscriptionSettingsCreate",

    "SubscriptionSettingsUpdate",

    "SubscriptionSettingsRead",

    "SubscriptionSettingsListResponse",

]





class SubscriptionSettingsBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    grace_period: Optional[int] = None

    cancel_after_grace: Optional[bool] = None

    prorate: Optional[bool] = None





class SubscriptionSettingsCreate(SubscriptionSettingsBase):

    pass





class SubscriptionSettingsUpdate(InputSchema):

    """A partial update."""



    grace_period: Optional[int] = None

    cancel_after_grace: Optional[bool] = None

    prorate: Optional[bool] = None





class SubscriptionSettingsRead(ReadSchema):

    id: uuid.UUID

    name: str

    grace_period: Optional[int] = None

    cancel_after_grace: bool

    prorate: bool





SubscriptionSettingsListResponse = Page[SubscriptionSettingsRead]
