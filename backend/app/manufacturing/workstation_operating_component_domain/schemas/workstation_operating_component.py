"""Pydantic v2 schemas for WorkstationOperatingComponent."""





from __future__ import annotations

from typing import Optional

import uuid



from app.manufacturing.workstation_operating_component_account_domain.schemas.workstation_operating_component_account import (

    WorkstationOperatingComponentAccountCreate,

    WorkstationOperatingComponentAccountRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "WorkstationOperatingComponentCreate",

    "WorkstationOperatingComponentUpdate",

    "WorkstationOperatingComponentRead",

    "WorkstationOperatingComponentListResponse",

]





class WorkstationOperatingComponentBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    component_name: Optional[str] = None

    accounts: list[WorkstationOperatingComponentAccountCreate] = []





class WorkstationOperatingComponentCreate(WorkstationOperatingComponentBase):

    pass





class WorkstationOperatingComponentUpdate(InputSchema):

    """A partial update."""



    component_name: Optional[str] = None

    accounts: Optional[list[WorkstationOperatingComponentAccountCreate]] = None





class WorkstationOperatingComponentRead(ReadSchema):

    id: uuid.UUID

    name: str

    component_name: Optional[str] = None

    accounts: list[WorkstationOperatingComponentAccountRead] = []





WorkstationOperatingComponentListResponse = Page[WorkstationOperatingComponentRead]
