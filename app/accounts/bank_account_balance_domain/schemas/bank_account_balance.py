"""Pydantic v2 schemas for Bank Account Balance (a child table of Bank Account)."""



from __future__ import annotations



import uuid

import datetime as dt

from decimal import Decimal

from typing import Optional



from pydantic import Field



from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import Page



__all__ = ["BankAccountBalanceCreate", "BankAccountBalanceUpdate", "BankAccountBalanceRead", "BankAccountBalanceListResponse"]





class BankAccountBalanceCreate(InputSchema):

    date: dt.date

    balance: Decimal

    currency: Optional[Optional[str]] = None









class BankAccountBalanceUpdate(InputSchema):

    date: Optional[dt.date] = None

    balance: Optional[Decimal] = None

    currency: Optional[Optional[str]] = None









class BankAccountBalanceRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    parent_id: Optional[uuid.UUID] = None

    idx: int

    date: dt.date

    balance: Decimal

    currency: Optional[Optional[str]] = None

    created_at: dt.datetime

    updated_at: dt.datetime





BankAccountBalanceListResponse = Page[BankAccountBalanceRead]
