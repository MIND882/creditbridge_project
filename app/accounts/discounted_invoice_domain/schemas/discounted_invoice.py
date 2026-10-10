"""Pydantic v2 schemas for DiscountedInvoice."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "DiscountedInvoiceCreate",

    "DiscountedInvoiceRead",

    "DiscountedInvoiceListResponse",

]





class DiscountedInvoiceBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    sales_invoice: str

    customer: Optional[str] = None

    posting_date: Optional[dt.date] = None

    outstanding_amount: Optional[Decimal] = None

    debit_to_id: Optional[uuid.UUID] = None





class DiscountedInvoiceCreate(DiscountedInvoiceBase):

    """Accepted only nested inside the parent payload."""

    pass





class DiscountedInvoiceRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    sales_invoice: str

    customer: Optional[str] = None

    posting_date: Optional[dt.date] = None

    outstanding_amount: Optional[Decimal] = None

    debit_to_id: Optional[uuid.UUID] = None





DiscountedInvoiceListResponse = Page[DiscountedInvoiceRead]
