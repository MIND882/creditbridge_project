"""Pydantic v2 schemas for POSPaymentMethod."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "POSPaymentMethodCreate",

    "POSPaymentMethodRead",

    "POSPaymentMethodListResponse",

]





class POSPaymentMethodBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    default: Optional[bool] = None

    mode_of_payment_id: uuid.UUID

    allow_in_returns: Optional[bool] = None





class POSPaymentMethodCreate(POSPaymentMethodBase):

    """Accepted only nested inside the parent payload."""

    pass





class POSPaymentMethodRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    default: bool

    mode_of_payment_id: uuid.UUID

    allow_in_returns: bool





POSPaymentMethodListResponse = Page[POSPaymentMethodRead]
