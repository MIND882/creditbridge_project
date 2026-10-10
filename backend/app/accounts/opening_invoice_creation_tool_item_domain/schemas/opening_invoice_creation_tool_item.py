"""Pydantic v2 schemas for OpeningInvoiceCreationToolItem."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "OpeningInvoiceCreationToolItemCreate",

    "OpeningInvoiceCreationToolItemRead",

    "OpeningInvoiceCreationToolItemListResponse",

]





class OpeningInvoiceCreationToolItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    party_type: Optional[str] = None

    party: Optional[str] = None

    temporary_opening_account_id: Optional[uuid.UUID] = None

    posting_date: Optional[dt.date] = None

    due_date: Optional[dt.date] = None

    item_name: Optional[str] = None

    outstanding_amount: Optional[Decimal] = None

    qty: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    invoice_number: Optional[str] = None

    supplier_invoice_date: Optional[dt.date] = None

    party_name: Optional[str] = None

    project: Optional[str] = None





class OpeningInvoiceCreationToolItemCreate(OpeningInvoiceCreationToolItemBase):

    """Accepted only nested inside the parent payload."""

    pass





class OpeningInvoiceCreationToolItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    party_type: Optional[str] = None

    party: Optional[str] = None

    temporary_opening_account_id: Optional[uuid.UUID] = None

    posting_date: Optional[dt.date] = None

    due_date: Optional[dt.date] = None

    item_name: Optional[str] = None

    outstanding_amount: Decimal

    qty: Optional[str] = None

    cost_center_id: Optional[uuid.UUID] = None

    invoice_number: Optional[str] = None

    supplier_invoice_date: Optional[dt.date] = None

    party_name: Optional[str] = None

    project: Optional[str] = None





OpeningInvoiceCreationToolItemListResponse = Page[OpeningInvoiceCreationToolItemRead]
