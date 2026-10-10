"""Pydantic v2 schemas for PaymentReconciliationAllocation."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PaymentReconciliationAllocationCreate",

    "PaymentReconciliationAllocationRead",

    "PaymentReconciliationAllocationListResponse",

]





class PaymentReconciliationAllocationBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    invoice_number: Optional[str] = None

    allocated_amount: Optional[Decimal] = None

    difference_account_id: Optional[uuid.UUID] = None

    difference_amount: Optional[Decimal] = None

    reference_name: Optional[str] = None

    is_advance: Optional[str] = None

    reference_type: str

    invoice_type: str

    unreconciled_amount: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    reference_row: Optional[str] = None

    currency: Optional[str] = None

    exchange_rate: Optional[Decimal] = None

    cost_center_id: Optional[uuid.UUID] = None

    gain_loss_posting_date: Optional[dt.date] = None

    debit_or_credit_note_posting_date: Optional[dt.date] = None





class PaymentReconciliationAllocationCreate(PaymentReconciliationAllocationBase):

    """Accepted only nested inside the parent payload."""

    pass





class PaymentReconciliationAllocationRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    invoice_number: Optional[str] = None

    allocated_amount: Decimal

    difference_account_id: Optional[uuid.UUID] = None

    difference_amount: Optional[Decimal] = None

    reference_name: Optional[str] = None

    is_advance: Optional[str] = None

    reference_type: str

    invoice_type: str

    unreconciled_amount: Optional[Decimal] = None

    amount: Optional[Decimal] = None

    reference_row: Optional[str] = None

    currency: Optional[str] = None

    exchange_rate: Optional[Decimal] = None

    cost_center_id: Optional[uuid.UUID] = None

    gain_loss_posting_date: Optional[dt.date] = None

    debit_or_credit_note_posting_date: Optional[dt.date] = None





PaymentReconciliationAllocationListResponse = Page[PaymentReconciliationAllocationRead]
