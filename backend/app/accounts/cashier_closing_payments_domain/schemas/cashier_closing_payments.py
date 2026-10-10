"""Pydantic v2 schemas for CashierClosingPayments."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "CashierClosingPaymentsCreate",

    "CashierClosingPaymentsRead",

    "CashierClosingPaymentsListResponse",

]





class CashierClosingPaymentsBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    mode_of_payment_id: uuid.UUID

    amount: Optional[Decimal] = None





class CashierClosingPaymentsCreate(CashierClosingPaymentsBase):

    """Accepted only nested inside the parent payload."""

    pass





class CashierClosingPaymentsRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    mode_of_payment_id: uuid.UUID

    amount: Optional[Decimal] = None





CashierClosingPaymentsListResponse = Page[CashierClosingPaymentsRead]
