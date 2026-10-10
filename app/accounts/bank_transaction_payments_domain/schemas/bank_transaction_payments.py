"""Pydantic v2 schemas for BankTransactionPayment (child table, read-only API)."""



from __future__ import annotations



import uuid

from datetime import date

from decimal import Decimal

from typing import Annotated, Optional



from pydantic import Field



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = ["BankTransactionPaymentCreate", "BankTransactionPaymentRead", "BankTransactionPaymentListResponse"]





class BankTransactionPaymentCreate(InputSchema):

    """Accepted only nested inside the parent's create/update payload."""



    payment_document: Annotated[str, Field(max_length=140)]

    payment_entry: Annotated[str, Field(max_length=140)]

    allocated_amount: Decimal

    clearance_date: Optional[date] = None

    reconciliation_type: Optional[str] = None





class BankTransactionPaymentRead(ReadSchema):

    id: uuid.UUID

    idx: int

    payment_document: str

    payment_entry: str

    allocated_amount: Decimal

    clearance_date: Optional[date] = None

    reconciliation_type: Optional[str] = None





BankTransactionPaymentListResponse = Page[BankTransactionPaymentRead]
