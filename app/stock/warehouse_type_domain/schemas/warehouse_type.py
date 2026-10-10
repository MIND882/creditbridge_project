"""Pydantic v2 schemas for WarehouseType."""





from __future__ import annotations

from typing import Optional

import uuid



from pydantic import Field

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "WarehouseTypeCreate",

    "WarehouseTypeUpdate",

    "WarehouseTypeRead",

    "WarehouseTypeListResponse",

]





class WarehouseTypeBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    name: str = Field(min_length=1)

    description: Optional[str] = None





class WarehouseTypeCreate(WarehouseTypeBase):

    pass





class WarehouseTypeUpdate(InputSchema):

    """A partial update."""



    name: Optional[str] = Field(default=None, min_length=1)

    description: Optional[str] = None





class WarehouseTypeRead(ReadSchema):

    id: uuid.UUID

    name: str

    description: Optional[str] = None





WarehouseTypeListResponse = Page[WarehouseTypeRead]
