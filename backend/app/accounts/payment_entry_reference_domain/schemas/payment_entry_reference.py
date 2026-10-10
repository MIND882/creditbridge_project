"""Pydantic v2 schemas for PaymentEntryReference (child table, read-only API)."""



from __future__ import annotations



import datetime as dt

import uuid

from decimal import Decimal

from typing import Annotated, Optional



from pydantic import Field



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = ["PaymentEntryReferenceCreate", "PaymentEntryReferenceRead", "PaymentEntryReferenceListResponse"]





class PaymentEntryReferenceCreate(InputSchema):

    """Accepted only nested inside the parent's create/update payload."""



    reference_doctype: Annotated[str, Field(max_length=140)]

    reference_name: Annotated[str, Field(max_length=140)]

    due_date: Optional[dt.date] = None

    bill_no: Optional[str] = None

    total_amount: Optional[Decimal] = None

    outstanding_amount: Optional[Decimal] = None

    allocated_amount: Optional[Decimal] = None

    exchange_rate: Optional[float] = None

    payment_term: Optional[str] = None

    exchange_gain_loss: Optional[Decimal] = None

    account_id: Optional[uuid.UUID] = None

    account_type: Optional[str] = None

    payment_type: Optional[str] = None

    payment_request: Optional[str] = None





class PaymentEntryReferenceRead(ReadSchema):

    id: uuid.UUID

    idx: int

    reference_doctype: str

    reference_name: str

    due_date: Optional[dt.date] = None

    bill_no: Optional[str] = None

    total_amount: Optional[Decimal] = None

    outstanding_amount: Optional[Decimal] = None

    allocated_amount: Optional[Decimal] = None

    exchange_rate: Optional[float] = None

    payment_term: Optional[str] = None

    exchange_gain_loss: Optional[Decimal] = None

    account_id: Optional[uuid.UUID] = None

    account_type: Optional[str] = None

    payment_type: Optional[str] = None

    payment_request: Optional[str] = None





PaymentEntryReferenceListResponse = Page[PaymentEntryReferenceRead]
