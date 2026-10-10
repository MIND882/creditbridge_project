"""Pydantic v2 schemas for BudgetAccount."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BudgetAccountCreate",

    "BudgetAccountRead",

    "BudgetAccountListResponse",

]





class BudgetAccountBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    account_id: uuid.UUID

    budget_amount: Optional[Decimal] = None





class BudgetAccountCreate(BudgetAccountBase):

    """Accepted only nested inside the parent payload."""

    pass





class BudgetAccountRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    account_id: uuid.UUID

    budget_amount: Decimal





BudgetAccountListResponse = Page[BudgetAccountRead]
