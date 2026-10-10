"""Pydantic v2 schemas for ExchangeRateRevaluationAccount."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ExchangeRateRevaluationAccountCreate",

    "ExchangeRateRevaluationAccountRead",

    "ExchangeRateRevaluationAccountListResponse",

]





class ExchangeRateRevaluationAccountBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    account_id: uuid.UUID

    party_type: Optional[str] = None

    party: Optional[str] = None

    account_currency: Optional[str] = None

    balance_in_account_currency: Optional[Decimal] = None

    current_exchange_rate: Optional[Decimal] = None

    balance_in_base_currency: Optional[Decimal] = None

    new_exchange_rate: Optional[Decimal] = None

    new_balance_in_base_currency: Optional[Decimal] = None

    gain_loss: Optional[Decimal] = None

    zero_balance: Optional[bool] = None

    new_balance_in_account_currency: Optional[Decimal] = None





class ExchangeRateRevaluationAccountCreate(ExchangeRateRevaluationAccountBase):

    """Accepted only nested inside the parent payload."""

    pass





class ExchangeRateRevaluationAccountRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    account_id: uuid.UUID

    party_type: Optional[str] = None

    party: Optional[str] = None

    account_currency: Optional[str] = None

    balance_in_account_currency: Optional[Decimal] = None

    current_exchange_rate: Optional[Decimal] = None

    balance_in_base_currency: Optional[Decimal] = None

    new_exchange_rate: Decimal

    new_balance_in_base_currency: Optional[Decimal] = None

    gain_loss: Optional[Decimal] = None

    zero_balance: bool

    new_balance_in_account_currency: Optional[Decimal] = None





ExchangeRateRevaluationAccountListResponse = Page[ExchangeRateRevaluationAccountRead]
