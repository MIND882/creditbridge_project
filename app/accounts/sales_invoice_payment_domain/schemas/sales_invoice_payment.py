"""Pydantic v2 schemas for SalesInvoicePayment."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SalesInvoicePaymentCreate",

    "SalesInvoicePaymentRead",

    "SalesInvoicePaymentListResponse",

]





class SalesInvoicePaymentBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    parenttype: Optional[str] = None

    mode_of_payment_id: uuid.UUID

    amount: Optional[Decimal] = None

    account_id: Optional[uuid.UUID] = None

    type: Optional[str] = None

    base_amount: Optional[Decimal] = None

    clearance_date: Optional[dt.date] = None

    default: Optional[bool] = None

    reference_no: Optional[str] = None





class SalesInvoicePaymentCreate(SalesInvoicePaymentBase):

    """Accepted only nested inside the parent payload."""

    pass





class SalesInvoicePaymentRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    parenttype: Optional[str] = None

    mode_of_payment_id: uuid.UUID

    amount: Decimal

    account_id: Optional[uuid.UUID] = None

    type: Optional[str] = None

    base_amount: Optional[Decimal] = None

    clearance_date: Optional[dt.date] = None

    default: bool

    reference_no: Optional[str] = None





SalesInvoicePaymentListResponse = Page[SalesInvoicePaymentRead]
