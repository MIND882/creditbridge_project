"""

Pydantic v2 schemas for Cost Center Allocation Percentage.



This is a Frappe child table (``istable: 1``): rows are created and edited

through the parent Cost Center Allocation payload, so the Create/Update schemas

here exist for callers that want to validate a row in isolation (and for the

parent service to reuse). There is no standalone write API.

"""



from __future__ import annotations



import uuid

from datetime import datetime

from decimal import Decimal

from typing import Optional



from pydantic import Field



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "CostCenterAllocationPercentageCreate",

    "CostCenterAllocationPercentageUpdate",

    "CostCenterAllocationPercentageRead",

    "CostCenterAllocationPercentageListResponse",

]





class CostCenterAllocationPercentageCreate(InputSchema):

    cost_center_id: uuid.UUID

    percentage: Decimal = Field(gt=0, le=100)





class CostCenterAllocationPercentageUpdate(InputSchema):

    cost_center_id: Optional[uuid.UUID] = None

    percentage: Optional[Decimal] = Field(default=None, gt=0, le=100)





class CostCenterAllocationPercentageRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    parent_id: Optional[uuid.UUID] = None

    idx: int

    cost_center_id: uuid.UUID

    percentage: Decimal

    created_at: datetime

    updated_at: datetime





CostCenterAllocationPercentageListResponse = Page[CostCenterAllocationPercentageRead]
