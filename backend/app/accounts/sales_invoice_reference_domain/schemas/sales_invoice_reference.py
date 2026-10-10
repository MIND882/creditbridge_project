"""Pydantic v2 schemas for SalesInvoiceReference."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SalesInvoiceReferenceCreate",

    "SalesInvoiceReferenceRead",

    "SalesInvoiceReferenceListResponse",

]





class SalesInvoiceReferenceBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    sales_invoice: str

    posting_date: dt.date

    customer: str

    is_return: Optional[bool] = None

    return_against: Optional[str] = None

    grand_total: Optional[Decimal] = None





class SalesInvoiceReferenceCreate(SalesInvoiceReferenceBase):

    """Accepted only nested inside the parent payload."""

    pass





class SalesInvoiceReferenceRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    sales_invoice: str

    posting_date: dt.date

    customer: str

    is_return: bool

    return_against: Optional[str] = None

    grand_total: Decimal





SalesInvoiceReferenceListResponse = Page[SalesInvoiceReferenceRead]
