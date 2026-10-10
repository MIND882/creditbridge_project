"""Pydantic v2 schemas for CashierClosing."""





from __future__ import annotations

from app.accounts.cashier_closing_domain.models.cashier_closing import (

    CashierClosingNamingSeries,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.cashier_closing_payments_domain.schemas.cashier_closing_payments import (

    CashierClosingPaymentsCreate,

    CashierClosingPaymentsRead,

)



__all__ = [

    "CashierClosingCreate",

    "CashierClosingUpdate",

    "CashierClosingRead",

    "CashierClosingListResponse",

]





class CashierClosingBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: Optional[CashierClosingNamingSeries] = None

    user: str

    date: Optional[dt.date] = None

    from_time: Optional[dt.time] = None

    time: Optional[dt.time] = None

    expense: Optional[Decimal] = None

    custody: Optional[Decimal] = None

    returns: Optional[Decimal] = None

    outstanding_amount: Optional[Decimal] = None

    net_amount: Optional[Decimal] = None

    amended_from: Optional[str] = None



    payments: list[CashierClosingPaymentsCreate] = []





class CashierClosingCreate(CashierClosingBase):

    pass





class CashierClosingUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[CashierClosingNamingSeries] = None

    user: Optional[str] = None

    date: Optional[dt.date] = None

    from_time: Optional[dt.time] = None

    time: Optional[dt.time] = None

    expense: Optional[Decimal] = None

    custody: Optional[Decimal] = None

    returns: Optional[Decimal] = None

    outstanding_amount: Optional[Decimal] = None

    net_amount: Optional[Decimal] = None

    amended_from: Optional[str] = None

    payments: Optional[list[CashierClosingPaymentsCreate]] = None





class CashierClosingRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[CashierClosingNamingSeries] = None

    user: str

    date: Optional[dt.date] = None

    from_time: Optional[dt.time] = None

    time: Optional[dt.time] = None

    expense: Optional[Decimal] = None

    custody: Optional[Decimal] = None

    returns: Optional[Decimal] = None

    outstanding_amount: Optional[Decimal] = None

    net_amount: Optional[Decimal] = None

    amended_from: Optional[str] = None

    payments: list[CashierClosingPaymentsRead] = []



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





CashierClosingListResponse = Page[CashierClosingRead]
