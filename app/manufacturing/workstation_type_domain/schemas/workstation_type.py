"""Pydantic v2 schemas for WorkstationType."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "WorkstationTypeCreate",

    "WorkstationTypeUpdate",

    "WorkstationTypeRead",

    "WorkstationTypeListResponse",

]





class WorkstationTypeBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    workstation_type: Optional[str] = None

    hour_rate: Optional[Decimal] = None

    description: Optional[str] = None





class WorkstationTypeCreate(WorkstationTypeBase):

    pass





class WorkstationTypeUpdate(InputSchema):

    """A partial update."""



    workstation_type: Optional[str] = None

    hour_rate: Optional[Decimal] = None

    description: Optional[str] = None





class WorkstationTypeRead(ReadSchema):

    id: uuid.UUID

    name: str

    workstation_type: Optional[str] = None

    hour_rate: Optional[Decimal] = None

    description: Optional[str] = None





WorkstationTypeListResponse = Page[WorkstationTypeRead]
