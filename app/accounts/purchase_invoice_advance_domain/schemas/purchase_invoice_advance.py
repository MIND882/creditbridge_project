"""Pydantic v2 schemas for PurchaseInvoiceAdvance."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PurchaseInvoiceAdvanceCreate",

    "PurchaseInvoiceAdvanceRead",

    "PurchaseInvoiceAdvanceListResponse",

]





class PurchaseInvoiceAdvanceBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    reference_type: Optional[str] = None

    reference_name: Optional[str] = None

    remarks: Optional[str] = None

    reference_row: Optional[str] = None

    advance_amount: Optional[Decimal] = None

    allocated_amount: Optional[Decimal] = None

    exchange_gain_loss: Optional[Decimal] = None

    ref_exchange_rate: Optional[Decimal] = None

    difference_posting_date: Optional[dt.date] = None





class PurchaseInvoiceAdvanceCreate(PurchaseInvoiceAdvanceBase):

    """Accepted only nested inside the parent payload."""

    pass





class PurchaseInvoiceAdvanceRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    reference_type: Optional[str] = None

    reference_name: Optional[str] = None

    remarks: Optional[str] = None

    reference_row: Optional[str] = None

    advance_amount: Optional[Decimal] = None

    allocated_amount: Optional[Decimal] = None

    exchange_gain_loss: Optional[Decimal] = None

    ref_exchange_rate: Optional[Decimal] = None

    difference_posting_date: Optional[dt.date] = None





PurchaseInvoiceAdvanceListResponse = Page[PurchaseInvoiceAdvanceRead]
