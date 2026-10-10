"""Pydantic v2 schemas for MonthlyDistributionPercentage."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "MonthlyDistributionPercentageCreate",

    "MonthlyDistributionPercentageRead",

    "MonthlyDistributionPercentageListResponse",

]





class MonthlyDistributionPercentageBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    month: str

    percentage_allocation: Optional[Decimal] = None





class MonthlyDistributionPercentageCreate(MonthlyDistributionPercentageBase):

    """Accepted only nested inside the parent payload."""

    pass





class MonthlyDistributionPercentageRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    month: str

    percentage_allocation: Optional[Decimal] = None





MonthlyDistributionPercentageListResponse = Page[MonthlyDistributionPercentageRead]
