"""Pydantic v2 schemas for Uom."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "UomCreate",

    "UomUpdate",

    "UomRead",

    "UomListResponse",

]





class UomBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    uom_name: str

    must_be_whole_number: Optional[bool] = None

    enabled: Optional[bool] = None

    symbol: Optional[str] = None

    common_code: Optional[str] = None

    description: Optional[str] = None

    category_id: Optional[uuid.UUID] = None





class UomCreate(UomBase):

    pass





class UomUpdate(InputSchema):

    """A partial update."""



    uom_name: Optional[str] = None

    must_be_whole_number: Optional[bool] = None

    enabled: Optional[bool] = None

    symbol: Optional[str] = None

    common_code: Optional[str] = None

    description: Optional[str] = None

    category_id: Optional[uuid.UUID] = None





class UomRead(ReadSchema):

    id: uuid.UUID

    name: str

    uom_name: str

    must_be_whole_number: Optional[bool] = None

    enabled: Optional[bool] = None

    symbol: Optional[str] = None

    common_code: Optional[str] = None

    description: Optional[str] = None

    category_id: Optional[uuid.UUID] = None





UomListResponse = Page[UomRead]
