"""Pydantic v2 schemas for AccountClosingBalance."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "AccountClosingBalanceCreate",

    "AccountClosingBalanceUpdate",

    "AccountClosingBalanceRead",

    "AccountClosingBalanceListResponse",

]





class AccountClosingBalanceBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    closing_date: Optional[dt.date] = None

    account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    debit: Optional[Decimal] = None

    credit: Optional[Decimal] = None

    account_currency: Optional[str] = None

    debit_in_account_currency: Optional[Decimal] = None

    credit_in_account_currency: Optional[Decimal] = None

    project: Optional[str] = None

    finance_book_id: Optional[uuid.UUID] = None

    period_closing_voucher: Optional[str] = None

    is_period_closing_voucher_entry: Optional[bool] = None

    debit_in_reporting_currency: Optional[Decimal] = None

    credit_in_reporting_currency: Optional[Decimal] = None

    reporting_currency_exchange_rate: Optional[Decimal] = None





class AccountClosingBalanceCreate(AccountClosingBalanceBase):

    pass





class AccountClosingBalanceUpdate(InputSchema):

    """A partial update."""



    closing_date: Optional[dt.date] = None

    account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    debit: Optional[Decimal] = None

    credit: Optional[Decimal] = None

    account_currency: Optional[str] = None

    debit_in_account_currency: Optional[Decimal] = None

    credit_in_account_currency: Optional[Decimal] = None

    project: Optional[str] = None

    finance_book_id: Optional[uuid.UUID] = None

    period_closing_voucher: Optional[str] = None

    is_period_closing_voucher_entry: Optional[bool] = None

    debit_in_reporting_currency: Optional[Decimal] = None

    credit_in_reporting_currency: Optional[Decimal] = None

    reporting_currency_exchange_rate: Optional[Decimal] = None





class AccountClosingBalanceRead(ReadSchema):

    id: uuid.UUID

    name: str

    closing_date: Optional[dt.date] = None

    account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    debit: Optional[Decimal] = None

    credit: Optional[Decimal] = None

    account_currency: Optional[str] = None

    debit_in_account_currency: Optional[Decimal] = None

    credit_in_account_currency: Optional[Decimal] = None

    project: Optional[str] = None

    finance_book_id: Optional[uuid.UUID] = None

    period_closing_voucher: Optional[str] = None

    is_period_closing_voucher_entry: bool

    debit_in_reporting_currency: Optional[Decimal] = None

    credit_in_reporting_currency: Optional[Decimal] = None

    reporting_currency_exchange_rate: Optional[Decimal] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





AccountClosingBalanceListResponse = Page[AccountClosingBalanceRead]
