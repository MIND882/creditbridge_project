"""Pydantic v2 schemas for ProcessPaymentReconciliationLogAllocations."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ProcessPaymentReconciliationLogAllocationsCreate",

    "ProcessPaymentReconciliationLogAllocationsRead",

    "ProcessPaymentReconciliationLogAllocationsListResponse",

]





class ProcessPaymentReconciliationLogAllocationsBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    reference_type: str

    reference_name: Optional[str] = None

    reference_row: Optional[str] = None

    invoice_type: str

    invoice_number: Optional[str] = None

    allocated_amount: Optional[Decimal] = None

    unreconciled_amount: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    is_advance: Optional[str] = None

    difference_amount: Optional[Decimal] = None

    difference_account_id: Optional[uuid.UUID] = None

    exchange_rate: Optional[Decimal] = None

    currency: Optional[str] = None

    reconciled: Optional[bool] = None

    gain_loss_posting_date: Optional[dt.date] = None





class ProcessPaymentReconciliationLogAllocationsCreate(ProcessPaymentReconciliationLogAllocationsBase):

    """Accepted only nested inside the parent payload."""

    pass





class ProcessPaymentReconciliationLogAllocationsRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    reference_type: str

    reference_name: Optional[str] = None

    reference_row: Optional[str] = None

    invoice_type: str

    invoice_number: Optional[str] = None

    allocated_amount: Decimal

    unreconciled_amount: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    is_advance: Optional[str] = None

    difference_amount: Optional[Decimal] = None

    difference_account_id: Optional[uuid.UUID] = None

    exchange_rate: Optional[Decimal] = None

    currency: Optional[str] = None

    reconciled: bool

    gain_loss_posting_date: Optional[dt.date] = None





ProcessPaymentReconciliationLogAllocationsListResponse = Page[ProcessPaymentReconciliationLogAllocationsRead]
