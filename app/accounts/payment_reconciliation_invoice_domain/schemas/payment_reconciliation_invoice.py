"""Pydantic v2 schemas for PaymentReconciliationInvoice."""





from __future__ import annotations

from app.accounts.payment_reconciliation_invoice_domain.models.payment_reconciliation_invoice import (

    PaymentReconciliationInvoiceInvoiceType,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PaymentReconciliationInvoiceCreate",

    "PaymentReconciliationInvoiceRead",

    "PaymentReconciliationInvoiceListResponse",

]





class PaymentReconciliationInvoiceBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    invoice_type: Optional[PaymentReconciliationInvoiceInvoiceType] = None

    invoice_number: Optional[str] = None

    invoice_date: Optional[dt.date] = None

    amount: Optional[Decimal] = None

    outstanding_amount: Optional[Decimal] = None

    currency: Optional[str] = None

    exchange_rate: Optional[Decimal] = None





class PaymentReconciliationInvoiceCreate(PaymentReconciliationInvoiceBase):

    """Accepted only nested inside the parent payload."""

    pass





class PaymentReconciliationInvoiceRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    invoice_type: Optional[PaymentReconciliationInvoiceInvoiceType] = None

    invoice_number: Optional[str] = None

    invoice_date: Optional[dt.date] = None

    amount: Optional[Decimal] = None

    outstanding_amount: Optional[Decimal] = None

    currency: Optional[str] = None

    exchange_rate: Optional[Decimal] = None





PaymentReconciliationInvoiceListResponse = Page[PaymentReconciliationInvoiceRead]
