"""Pydantic v2 schemas for LedgerHealth."""





from __future__ import annotations

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "LedgerHealthCreate",

    "LedgerHealthUpdate",

    "LedgerHealthRead",

    "LedgerHealthListResponse",

]





class LedgerHealthBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    voucher_type: Optional[str] = None

    voucher_no: Optional[str] = None

    debit_credit_mismatch: Optional[bool] = None

    checked_on: Optional[dt.datetime] = None

    general_and_payment_ledger_mismatch: Optional[bool] = None





class LedgerHealthCreate(LedgerHealthBase):

    pass





class LedgerHealthUpdate(InputSchema):

    """A partial update."""



    voucher_type: Optional[str] = None

    voucher_no: Optional[str] = None

    debit_credit_mismatch: Optional[bool] = None

    checked_on: Optional[dt.datetime] = None

    general_and_payment_ledger_mismatch: Optional[bool] = None





class LedgerHealthRead(ReadSchema):

    id: uuid.UUID

    name: str

    voucher_type: Optional[str] = None

    voucher_no: Optional[str] = None

    debit_credit_mismatch: bool

    checked_on: Optional[dt.datetime] = None

    general_and_payment_ledger_mismatch: bool





LedgerHealthListResponse = Page[LedgerHealthRead]
