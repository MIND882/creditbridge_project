"""Pydantic v2 schemas for UomConversionDetail."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "UomConversionDetailCreate",

    "UomConversionDetailRead",

    "UomConversionDetailListResponse",

]





class UomConversionDetailBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    uom_id: uuid.UUID

    conversion_factor: Optional[Decimal] = None





class UomConversionDetailCreate(UomConversionDetailBase):

    pass





class UomConversionDetailUpdate(InputSchema):

    """A partial update."""



    uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None





class UomConversionDetailRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    uom_id: Optional[uuid.UUID] = None

    conversion_factor: Optional[Decimal] = None





UomConversionDetailListResponse = Page[UomConversionDetailRead]
