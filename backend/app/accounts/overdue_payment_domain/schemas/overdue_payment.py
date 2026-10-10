"""Pydantic v2 schemas for OverduePayment."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "OverduePaymentCreate",

    "OverduePaymentRead",

    "OverduePaymentListResponse",

]





class OverduePaymentBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    payment_term_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    due_date: Optional[dt.date] = None

    mode_of_payment_id: Optional[uuid.UUID] = None

    invoice_portion: Optional[Decimal] = None

    payment_amount: Optional[Decimal] = None

    outstanding: Optional[Decimal] = None

    paid_amount: Optional[Decimal] = None

    discounted_amount: Optional[Decimal] = None

    sales_invoice: str

    payment_schedule: Optional[str] = None

    overdue_days: Optional[str] = None

    dunning_level: Optional[int] = None

    interest: Optional[Decimal] = None





class OverduePaymentCreate(OverduePaymentBase):

    """Accepted only nested inside the parent payload."""

    pass





class OverduePaymentRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    payment_term_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    due_date: Optional[dt.date] = None

    mode_of_payment_id: Optional[uuid.UUID] = None

    invoice_portion: Optional[Decimal] = None

    payment_amount: Optional[Decimal] = None

    outstanding: Optional[Decimal] = None

    paid_amount: Optional[Decimal] = None

    discounted_amount: Optional[Decimal] = None

    sales_invoice: str

    payment_schedule: Optional[str] = None

    overdue_days: Optional[str] = None

    dunning_level: Optional[int] = None

    interest: Optional[Decimal] = None





OverduePaymentListResponse = Page[OverduePaymentRead]
