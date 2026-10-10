"""Pydantic v2 schemas for BudgetDistribution."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BudgetDistributionCreate",

    "BudgetDistributionRead",

    "BudgetDistributionListResponse",

]





class BudgetDistributionBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    start_date: dt.date

    end_date: dt.date

    amount: Optional[Decimal] = None

    percent: Optional[Decimal] = None





class BudgetDistributionCreate(BudgetDistributionBase):

    """Accepted only nested inside the parent payload."""

    pass





class BudgetDistributionRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    start_date: dt.date

    end_date: dt.date

    amount: Decimal

    percent: Decimal





BudgetDistributionListResponse = Page[BudgetDistributionRead]
