"""Pydantic v2 schemas for WorkstationOperatingComponentAccount."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "WorkstationOperatingComponentAccountCreate",

    "WorkstationOperatingComponentAccountRead",

    "WorkstationOperatingComponentAccountListResponse",

]





class WorkstationOperatingComponentAccountBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    company: str

    expense_account_id: Optional[uuid.UUID] = None





class WorkstationOperatingComponentAccountCreate(WorkstationOperatingComponentAccountBase):

    pass





class WorkstationOperatingComponentAccountUpdate(InputSchema):

    """A partial update."""



    company: Optional[str] = None

    expense_account_id: Optional[uuid.UUID] = None





class WorkstationOperatingComponentAccountRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    company: str

    expense_account_id: Optional[uuid.UUID] = None





WorkstationOperatingComponentAccountListResponse = Page[WorkstationOperatingComponentAccountRead]
