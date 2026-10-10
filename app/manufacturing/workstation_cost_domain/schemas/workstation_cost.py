"""Pydantic v2 schemas for WorkstationCost."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "WorkstationCostCreate",

    "WorkstationCostRead",

    "WorkstationCostListResponse",

]





class WorkstationCostBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    operating_component_id: uuid.UUID

    operating_cost: Decimal





class WorkstationCostCreate(WorkstationCostBase):

    pass





class WorkstationCostUpdate(InputSchema):

    """A partial update."""



    operating_component_id: Optional[uuid.UUID] = None

    operating_cost: Optional[Decimal] = None





class WorkstationCostRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    operating_component_id: Optional[uuid.UUID] = None

    operating_cost: Optional[Decimal] = None





WorkstationCostListResponse = Page[WorkstationCostRead]
