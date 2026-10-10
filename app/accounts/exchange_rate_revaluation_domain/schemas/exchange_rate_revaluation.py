"""Pydantic v2 schemas for ExchangeRateRevaluation."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.exchange_rate_revaluation_account_domain.schemas.exchange_rate_revaluation_account import (

    ExchangeRateRevaluationAccountCreate,

    ExchangeRateRevaluationAccountRead,

)



__all__ = [

    "ExchangeRateRevaluationCreate",

    "ExchangeRateRevaluationUpdate",

    "ExchangeRateRevaluationRead",

    "ExchangeRateRevaluationListResponse",

]





class ExchangeRateRevaluationBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    posting_date: dt.date

    amended_from: Optional[str] = None

    gain_loss_unbooked: Optional[Decimal] = None

    gain_loss_booked: Optional[Decimal] = None

    total_gain_loss: Optional[Decimal] = None

    rounding_loss_allowance: Optional[Decimal] = None



    accounts: list[ExchangeRateRevaluationAccountCreate] = []





class ExchangeRateRevaluationCreate(ExchangeRateRevaluationBase):

    pass





class ExchangeRateRevaluationUpdate(InputSchema):

    """A partial update."""



    posting_date: Optional[dt.date] = None

    amended_from: Optional[str] = None

    gain_loss_unbooked: Optional[Decimal] = None

    gain_loss_booked: Optional[Decimal] = None

    total_gain_loss: Optional[Decimal] = None

    rounding_loss_allowance: Optional[Decimal] = None

    accounts: Optional[list[ExchangeRateRevaluationAccountCreate]] = None





class ExchangeRateRevaluationRead(ReadSchema):

    id: uuid.UUID

    name: str

    posting_date: dt.date

    amended_from: Optional[str] = None

    gain_loss_unbooked: Optional[Decimal] = None

    gain_loss_booked: Optional[Decimal] = None

    total_gain_loss: Optional[Decimal] = None

    rounding_loss_allowance: Optional[Decimal] = None

    accounts: list[ExchangeRateRevaluationAccountRead] = []



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





ExchangeRateRevaluationListResponse = Page[ExchangeRateRevaluationRead]
