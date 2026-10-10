"""Pydantic v2 schemas for PaymentReference."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PaymentReferenceCreate",

    "PaymentReferenceRead",

    "PaymentReferenceListResponse",

]





class PaymentReferenceBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    payment_term_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    due_date: Optional[dt.date] = None

    amount: Optional[Decimal] = None

    currency: Optional[str] = None

    payment_schedule_id: Optional[uuid.UUID] = None





class PaymentReferenceCreate(PaymentReferenceBase):

    """Accepted only nested inside the parent payload."""

    pass





class PaymentReferenceRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    payment_term_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    due_date: Optional[dt.date] = None

    amount: Optional[Decimal] = None

    currency: Optional[str] = None

    payment_schedule_id: Optional[uuid.UUID] = None





PaymentReferenceListResponse = Page[PaymentReferenceRead]
