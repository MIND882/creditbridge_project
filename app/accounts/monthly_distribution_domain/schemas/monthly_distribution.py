"""Pydantic v2 schemas for MonthlyDistribution."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.monthly_distribution_percentage_domain.schemas.monthly_distribution_percentage import (

    MonthlyDistributionPercentageCreate,

    MonthlyDistributionPercentageRead,

)



__all__ = [

    "MonthlyDistributionCreate",

    "MonthlyDistributionUpdate",

    "MonthlyDistributionRead",

    "MonthlyDistributionListResponse",

]





class MonthlyDistributionBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    fiscal_year_id: Optional[uuid.UUID] = None



    percentages: list[MonthlyDistributionPercentageCreate] = []





class MonthlyDistributionCreate(MonthlyDistributionBase):

    pass





class MonthlyDistributionUpdate(InputSchema):

    """A partial update."""



    fiscal_year_id: Optional[uuid.UUID] = None

    percentages: Optional[list[MonthlyDistributionPercentageCreate]] = None





class MonthlyDistributionRead(ReadSchema):

    id: uuid.UUID

    name: str

    fiscal_year_id: Optional[uuid.UUID] = None

    percentages: list[MonthlyDistributionPercentageRead] = []





MonthlyDistributionListResponse = Page[MonthlyDistributionRead]
