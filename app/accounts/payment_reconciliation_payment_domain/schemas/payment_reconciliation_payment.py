"""Pydantic v2 schemas for PaymentReconciliationPayment."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PaymentReconciliationPaymentCreate",

    "PaymentReconciliationPaymentRead",

    "PaymentReconciliationPaymentListResponse",

]





class PaymentReconciliationPaymentBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    reference_type: Optional[str] = None

    reference_name: Optional[str] = None

    posting_date: Optional[dt.date] = None

    is_advance: Optional[str] = None

    reference_row: Optional[str] = None

    amount: Optional[Decimal] = None

    currency: Optional[str] = None

    difference_amount: Optional[Decimal] = None

    exchange_rate: Optional[Decimal] = None

    cost_center_id: Optional[uuid.UUID] = None

    remarks: Optional[str] = None





class PaymentReconciliationPaymentCreate(PaymentReconciliationPaymentBase):

    """Accepted only nested inside the parent payload."""

    pass





class PaymentReconciliationPaymentRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    reference_type: Optional[str] = None

    reference_name: Optional[str] = None

    posting_date: Optional[dt.date] = None

    is_advance: Optional[str] = None

    reference_row: Optional[str] = None

    amount: Optional[Decimal] = None

    currency: Optional[str] = None

    difference_amount: Optional[Decimal] = None

    exchange_rate: Optional[Decimal] = None

    cost_center_id: Optional[uuid.UUID] = None

    remarks: Optional[str] = None





PaymentReconciliationPaymentListResponse = Page[PaymentReconciliationPaymentRead]
