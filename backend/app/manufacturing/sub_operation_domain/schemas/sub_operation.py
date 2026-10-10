"""Pydantic v2 schemas for SubOperation."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SubOperationCreate",

    "SubOperationRead",

    "SubOperationListResponse",

]





class SubOperationBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    operation_id: uuid.UUID

    time_in_mins: Optional[Decimal] = None

    description: Optional[str] = None





class SubOperationCreate(SubOperationBase):

    pass





class SubOperationUpdate(InputSchema):

    """A partial update."""



    operation_id: Optional[uuid.UUID] = None

    time_in_mins: Optional[Decimal] = None

    description: Optional[str] = None





class SubOperationRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    operation_id: Optional[uuid.UUID] = None

    time_in_mins: Optional[Decimal] = None

    description: Optional[str] = None





SubOperationListResponse = Page[SubOperationRead]
