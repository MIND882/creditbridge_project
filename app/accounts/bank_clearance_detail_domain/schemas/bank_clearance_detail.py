"""Pydantic v2 schemas for BankClearanceDetail (child table, read-only API)."""



from __future__ import annotations



import uuid

from datetime import date

from decimal import Decimal

from typing import Annotated, Optional



from pydantic import Field



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = ["BankClearanceDetailCreate", "BankClearanceDetailRead", "BankClearanceDetailListResponse"]





class BankClearanceDetailCreate(InputSchema):

    """Accepted only nested inside the parent's create/update payload."""



    payment_document: Optional[str] = None

    payment_entry: Optional[str] = None

    against_account: Optional[str] = None

    amount: Optional[str] = None

    posting_date: Optional[date] = None

    cheque_number: Optional[str] = None

    cheque_date: Optional[date] = None

    clearance_date: Optional[date] = None





class BankClearanceDetailRead(ReadSchema):

    id: uuid.UUID

    idx: int

    payment_document: Optional[str] = None

    payment_entry: Optional[str] = None

    against_account: Optional[str] = None

    amount: Optional[str] = None

    posting_date: Optional[date] = None

    cheque_number: Optional[str] = None

    cheque_date: Optional[date] = None

    clearance_date: Optional[date] = None





BankClearanceDetailListResponse = Page[BankClearanceDetailRead]
