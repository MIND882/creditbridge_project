"""Pydantic v2 schemas for SubscriptionInvoice."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SubscriptionInvoiceCreate",

    "SubscriptionInvoiceRead",

    "SubscriptionInvoiceListResponse",

]





class SubscriptionInvoiceBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    document_type: Optional[str] = None

    invoice: Optional[str] = None





class SubscriptionInvoiceCreate(SubscriptionInvoiceBase):

    """Accepted only nested inside the parent payload."""

    pass





class SubscriptionInvoiceRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    document_type: Optional[str] = None

    invoice: Optional[str] = None





SubscriptionInvoiceListResponse = Page[SubscriptionInvoiceRead]
