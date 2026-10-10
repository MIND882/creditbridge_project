"""Pydantic v2 schemas for POSInvoiceReference."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "POSInvoiceReferenceCreate",

    "POSInvoiceReferenceRead",

    "POSInvoiceReferenceListResponse",

]





class POSInvoiceReferenceBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    parenttype: Optional[str] = None

    pos_invoice: str

    customer: str

    posting_date: dt.date

    grand_total: Optional[Decimal] = None

    is_return: Optional[bool] = None

    return_against: Optional[str] = None





class POSInvoiceReferenceCreate(POSInvoiceReferenceBase):

    """Accepted only nested inside the parent payload."""

    pass





class POSInvoiceReferenceRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    parenttype: Optional[str] = None

    pos_invoice: str

    customer: str

    posting_date: dt.date

    grand_total: Decimal

    is_return: bool

    return_against: Optional[str] = None





POSInvoiceReferenceListResponse = Page[POSInvoiceReferenceRead]
