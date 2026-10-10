"""Pydantic v2 schemas for BankReconciliationTool."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BankReconciliationToolCreate",

    "BankReconciliationToolUpdate",

    "BankReconciliationToolRead",

    "BankReconciliationToolListResponse",

]





class BankReconciliationToolBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    bank_account_id: Optional[uuid.UUID] = None

    bank_statement_from_date: Optional[dt.date] = None

    bank_statement_to_date: Optional[dt.date] = None

    account_opening_balance: Optional[Decimal] = None

    bank_statement_closing_balance: Optional[Decimal] = None

    from_reference_date: Optional[dt.date] = None

    to_reference_date: Optional[dt.date] = None

    filter_by_reference_date: Optional[bool] = None

    account_currency: Optional[str] = None





class BankReconciliationToolCreate(BankReconciliationToolBase):

    pass





class BankReconciliationToolUpdate(InputSchema):

    """A partial update."""



    bank_account_id: Optional[uuid.UUID] = None

    bank_statement_from_date: Optional[dt.date] = None

    bank_statement_to_date: Optional[dt.date] = None

    account_opening_balance: Optional[Decimal] = None

    bank_statement_closing_balance: Optional[Decimal] = None

    from_reference_date: Optional[dt.date] = None

    to_reference_date: Optional[dt.date] = None

    filter_by_reference_date: Optional[bool] = None

    account_currency: Optional[str] = None





class BankReconciliationToolRead(ReadSchema):

    id: uuid.UUID

    name: str

    bank_account_id: Optional[uuid.UUID] = None

    bank_statement_from_date: Optional[dt.date] = None

    bank_statement_to_date: Optional[dt.date] = None

    account_opening_balance: Optional[Decimal] = None

    bank_statement_closing_balance: Optional[Decimal] = None

    from_reference_date: Optional[dt.date] = None

    to_reference_date: Optional[dt.date] = None

    filter_by_reference_date: bool

    account_currency: Optional[str] = None





BankReconciliationToolListResponse = Page[BankReconciliationToolRead]
