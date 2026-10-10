"""

Pydantic v2 schemas for Cost Center Allocation and its child table.



The child table is nested inside the parent payload, matching how ERPNext

submits a document with its rows. ``docstatus`` is absent from every input

schema: the lifecycle moves through the submit / cancel / amend endpoints, not

through a field a client can set.

"""



from __future__ import annotations



import uuid

from datetime import date, datetime

from decimal import Decimal

from typing import Annotated, Optional



from pydantic import Field, field_validator



from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import Page



__all__ = [

    "AllocationPercentageCreate",

    "AllocationPercentageRead",

    "CostCenterAllocationCreate",

    "CostCenterAllocationUpdate",

    "CostCenterAllocationRead",

    "CostCenterAllocationListResponse",

    "DocStatusResult",

]





class AllocationPercentageCreate(InputSchema):

    """One row of the split. ``idx`` is assigned by the service from list order."""



    cost_center_id: uuid.UUID

    percentage: Decimal = Field(gt=0, le=100)





class AllocationPercentageRead(ReadSchema):

    id: uuid.UUID

    idx: int

    cost_center_id: uuid.UUID

    percentage: Decimal





class CostCenterAllocationCreate(InputSchema):

    main_cost_center_id: uuid.UUID

    valid_from: date

    allocation_percentages: Annotated[

        list[AllocationPercentageCreate], Field(min_length=1)

    ] = Field(description="Must total exactly 100")

    amended_from_id: Optional[uuid.UUID] = None





class CostCenterAllocationUpdate(InputSchema):

    """

    Only a draft is editable; the service enforces that.



    ``main_cost_center_id`` is deliberately absent -- moving the main cost

    centre of an existing allocation would invalidate the GL-entry date check

    that was run against the original. Cancel and amend instead.

    """



    valid_from: Optional[date] = None

    allocation_percentages: Optional[

        Annotated[list[AllocationPercentageCreate], Field(min_length=1)]

    ] = None





class CostCenterAllocationRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    name: str

    main_cost_center_id: uuid.UUID

    valid_from: date

    docstatus: int

    amended_from_id: Optional[uuid.UUID] = None

    allocation_percentages: list[AllocationPercentageRead] = Field(default_factory=list)

    created_at: datetime

    updated_at: datetime





CostCenterAllocationListResponse = Page[CostCenterAllocationRead]





class DocStatusResult(ReadSchema):

    """Returned by submit / cancel / amend."""



    id: uuid.UUID

    name: str

    docstatus: int
