"""Pydantic v2 schemas for SalesInvoiceAdvance."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SalesInvoiceAdvanceCreate",

    "SalesInvoiceAdvanceRead",

    "SalesInvoiceAdvanceListResponse",

]





class SalesInvoiceAdvanceBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    parenttype: Optional[str] = None

    reference_type: Optional[str] = None

    reference_name: Optional[str] = None

    remarks: Optional[str] = None

    reference_row: Optional[str] = None

    advance_amount: Optional[Decimal] = None

    allocated_amount: Optional[Decimal] = None

    exchange_gain_loss: Optional[Decimal] = None

    ref_exchange_rate: Optional[Decimal] = None

    difference_posting_date: Optional[dt.date] = None





class SalesInvoiceAdvanceCreate(SalesInvoiceAdvanceBase):

    """Accepted only nested inside the parent payload."""

    pass





class SalesInvoiceAdvanceRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    parenttype: Optional[str] = None

    reference_type: Optional[str] = None

    reference_name: Optional[str] = None

    remarks: Optional[str] = None

    reference_row: Optional[str] = None

    advance_amount: Optional[Decimal] = None

    allocated_amount: Optional[Decimal] = None

    exchange_gain_loss: Optional[Decimal] = None

    ref_exchange_rate: Optional[Decimal] = None

    difference_posting_date: Optional[dt.date] = None





SalesInvoiceAdvanceListResponse = Page[SalesInvoiceAdvanceRead]
