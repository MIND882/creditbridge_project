"""Pydantic v2 schemas for PaymentEntryDeduction (child table, read-only API)."""



from __future__ import annotations



import datetime as dt

import uuid

from decimal import Decimal

from typing import Annotated, Optional



from pydantic import Field



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = ["PaymentEntryDeductionCreate", "PaymentEntryDeductionRead", "PaymentEntryDeductionListResponse"]





class PaymentEntryDeductionCreate(InputSchema):

    """Accepted only nested inside the parent's create/update payload."""



    account_id: uuid.UUID

    cost_center_id: uuid.UUID

    amount: Decimal

    description: Optional[str] = None

    is_exchange_gain_loss: Optional[bool] = None





class PaymentEntryDeductionRead(ReadSchema):

    id: uuid.UUID

    idx: int

    account_id: uuid.UUID

    cost_center_id: uuid.UUID

    amount: Decimal

    description: Optional[str] = None

    is_exchange_gain_loss: Optional[bool] = None





PaymentEntryDeductionListResponse = Page[PaymentEntryDeductionRead]
